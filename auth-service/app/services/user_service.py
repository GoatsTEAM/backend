import bcrypt
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import UserCredential, UserProfile, RoleEnum


async def get_user(db: AsyncSession, user_id: int) -> dict | None:
    q1 = await db.execute(select(UserCredential).filter_by(user_id=user_id))
    user_credentials = q1.scalars().first()
    q2 = await db.execute(select(UserProfile).filter_by(user_id=user_id))
    user_profile = q2.scalars().first()
    if not user_credentials or not user_profile:
        return None

    return {
        "user_id": user_credentials.user_id,
        "email": user_credentials.email,
        "first_name": user_profile.first_name,
        "last_name": user_profile.last_name,
        "gender": user_profile.gender.value if user_profile.gender else None,
        "phone": user_profile.phone,
        "avatar": user_profile.avatar,
        "passport_number": user_profile.passport_number,
        "birth_date": user_profile.birth_date,
        "tax_id": user_profile.tax_id,
        "role": user_credentials.role.value,
        "is_banned": user_credentials.is_banned,
    }


async def ban_user(db: AsyncSession, user_id: int) -> bool:
    stmt = (
        update(UserCredential).
        where(UserCredential.user_id == user_id).
        values(is_banned=True)
    )
    res = await db.execute(stmt)
    if res.rowcount == 0:
        return False
    await db.commit()
    return True


async def register_user(db: AsyncSession, payload: dict) -> int:
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(payload["password"].encode(), salt).decode()

    user_credentials = UserCredential(
        email=payload["email"],
        hash_password=hash_pw,
        role=RoleEnum(payload["role"]),
    )
    db.add(user_credentials)
    await db.flush()

    user_profile = UserProfile(
        user_id=user_credentials.user_id,
        first_name=payload["first_name"],
        last_name=payload["last_name"],
    )
    db.add(user_profile)
    await db.commit()

    return user_credentials.user_id


async def authenticate(db: AsyncSession, email: str, password: str) -> tuple[int, bool] | tuple[None, None]:
    q = await db.execute(select(UserCredential).filter_by(email=email))
    user_credentials = q.scalars().first()
    if not user_credentials:
        return None, None
    if not bcrypt.checkpw(password.encode(), user_credentials.hash_password.encode()):
        return None, None
    return user_credentials.user_id, user_credentials.is_banned


async def update_user(db: AsyncSession, payload: dict) -> bool:
    q = await db.execute(select(UserProfile).filter_by(user_id=payload["user_id"]))
    user_profile = q.scalars().first()
    if not user_profile:
        return False

    for field, value in payload.items():
        if field != "user_id" and value is not None:
            setattr(user_profile, field, value)

    await db.commit()
    return True


async def delete_user(db: AsyncSession, requester_id: int, target_id: int, role: str) -> bool:
    if requester_id != target_id and role != RoleEnum.admin.value:
        return False
    await db.execute(delete(UserProfile).filter_by(user_id=target_id))
    await db.execute(delete(UserCredential).filter_by(user_id=target_id))
    await db.commit()
    return True


async def change_role(db: AsyncSession, user_id: int, new_role: RoleEnum) -> bool:
    stmt = (
        update(UserCredential).
        where(UserCredential.user_id == user_id).
        values(role=new_role)
    )
    res = await db.execute(stmt)
    if res.rowcount == 0:
        return False
    await db.commit()
    return True

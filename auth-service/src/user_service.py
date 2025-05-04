import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import bcrypt
import jwt
from .models import UserCredential, UserProfile, RoleEnum

# Secret for JWT signing
SECRET = os.getenv('JWT_SECRET', 'secret')

async def get_user(db: AsyncSession, user_id: int) -> dict | None:
    q1 = await db.execute(select(UserCredential).filter_by(user_id=user_id))
    cred = q1.scalars().first()
    q2 = await db.execute(select(UserProfile).filter_by(user_id=user_id))
    prof = q2.scalars().first()
    if not cred or not prof:
        return None
    return {
        'user_id': cred.user_id,
        'first_name': prof.first_name,
        'last_name': prof.last_name,
        'role': cred.role.value,
        'phone': prof.phone,
        'avatar': prof.avatar,
        'passport_number': prof.passport_number,
        'birth_date': prof.birth_date.isoformat() if prof.birth_date else None,
        'tax_id': prof.tax_id,
    }

async def ban_user(db: AsyncSession, user_id: int) -> bool:
    q = await db.execute(select(UserCredential).filter_by(user_id=user_id))
    cred = q.scalars().first()
    if not cred:
        return False
    cred.role = RoleEnum('operator') if cred.role != RoleEnum.admin else RoleEnum.admin
    await db.commit()
    return True

async def is_banned(db: AsyncSession, user_id: int) -> bool:
    q = await db.execute(select(UserCredential).filter_by(user_id=user_id))
    cred = q.scalars().first()
    if not cred:
        return False
    return cred.role == RoleEnum('guest')

async def register_user(db: AsyncSession, payload: dict) -> int:
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(payload['password'].encode(), salt).decode()
    cred = UserCredential(hash_password=hash_pw, role=RoleEnum(payload['role']))
    db.add(cred)
    await db.flush()
    prof = UserProfile(
        user_id=cred.user_id,
        first_name=payload['first_name'],
        last_name=payload['last_name']
    )
    db.add(prof)
    await db.commit()
    return cred.user_id

async def authenticate(db: AsyncSession, user_id: int, password: str) -> str | None:
    q = await db.execute(select(UserCredential).filter_by(user_id=user_id))
    cred = q.scalars().first()
    if not cred or not bcrypt.checkpw(password.encode(), cred.hash_password.encode()):
        return None
    return jwt.encode({'user_id': user_id, 'role': cred.role.value}, SECRET, algorithm='HS256')

async def update_user(db: AsyncSession, payload: dict) -> bool:
    q = await db.execute(select(UserProfile).filter_by(user_id=payload['user_id']))
    prof = q.scalars().first()
    if not prof:
        return False
    for field in ['first_name', 'last_name', 'phone', 'avatar']:
        if payload.get(field) is not None:
            setattr(prof, field, payload[field])
    await db.commit()
    return True

async def delete_user(db: AsyncSession, requester_id: int, target_id: int, role: str) -> bool:
    if requester_id != target_id and role != 'admin':
        return False
    await db.execute(delete(UserProfile).filter_by(user_id=target_id))
    await db.execute(delete(UserCredential).filter_by(user_id=target_id))
    await db.commit()
    return True
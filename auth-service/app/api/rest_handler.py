import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from db.database import AsyncSessionLocal
from models.models import RoleEnum
from services.user_service import (
    register_user as svc_register_user,
    authenticate as svc_authenticate,
    ban_user as svc_ban_user,
    get_user as svc_get_user,
    update_user as svc_update_user,
    delete_user as svc_delete_user,
    change_role as svc_change_role,
)
from models.schemas import (
    RegisterRequest,
    LoginRequest,
    UpdateUserRequest,
    RoleUpdateRequest,
    UserOut,
    Token,
    CurrentUser,
)

router = APIRouter(prefix="/users", tags=["users"])
JWT_SECRET = os.getenv("JWT_SECRET")
bearer_scheme = HTTPBearer()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db),
) -> CurrentUser:
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id: int = payload["user_id"]
    except (JWTError, KeyError):
        raise HTTPException(401, "Could not validate credentials")

    user_data = await svc_get_user(db, user_id)
    if not user_data:
        raise HTTPException(401, "User not found")
    if user_data["is_banned"]:
        raise HTTPException(403, "User is banned")

    return CurrentUser(
        user_id=user_data["user_id"],
        email=user_data["email"],
        role=user_data["role"],
        is_banned=user_data["is_banned"],
    )


def require_role(*allowed: str):
    def checker(current: CurrentUser = Depends(get_current_user)):
        if current.role not in allowed:
            raise HTTPException(403, "Operation not permitted")
        return current

    return checker


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    if req.role not in (RoleEnum.buyer.value, RoleEnum.seller.value):
        raise HTTPException(400, "Only the buyer or seller can register")
    user_id = await svc_register_user(db, req.dict())
    user_data = await svc_get_user(db, user_id)
    return user_data


@router.post("/login", response_model=Token)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_id, is_banned = await svc_authenticate(db, str(req.email), req.password)
    if not user_id:
        raise HTTPException(401, "Invalid credentials")
    if is_banned:
        raise HTTPException(403, "User is banned")
    token = jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm="HS256")
    return Token(access_token=token)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, current: CurrentUser = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current.user_id != user_id and current.role != RoleEnum.admin.value:
        raise HTTPException(403, "Forbidden")
    user_data = await svc_get_user(db, user_id)
    if not user_data:
        raise HTTPException(404, "User not found")
    return user_data


@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: int, req: UpdateUserRequest, current: CurrentUser = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    if current.user_id != user_id and current.role != RoleEnum.admin.value:
        raise HTTPException(403, "Forbidden")
    payload = {**req.dict(exclude_none=True), "user_id": user_id}
    update_result = await svc_update_user(db, payload)
    if not update_result:
        raise HTTPException(404, "User not found")
    user_data = await svc_get_user(db, user_id)
    return user_data


@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, current: CurrentUser = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    ok = await svc_delete_user(db, requester_id=current.user_id, target_id=user_id, role=str(current.role))
    if not ok:
        raise HTTPException(403, "Forbidden")
    return {"ok": True}


@router.post("/{user_id}/ban", dependencies=[Depends(require_role("admin"))], response_model=dict)
async def ban_user(user_id: int, db: AsyncSession = Depends(get_db)):
    ok = await svc_ban_user(db, user_id)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"ok": True}


@router.put("/{user_id}/role", dependencies=[Depends(require_role("admin"))], response_model=dict)
async def set_operator(user_id: int, req: RoleUpdateRequest, db: AsyncSession = Depends(get_db)):
    if req.role == RoleEnum.admin.value:
        raise HTTPException(400, "Can't assign an admin")
    ok = await svc_change_role(db, user_id, req.role)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"ok": True}

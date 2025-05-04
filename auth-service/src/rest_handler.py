from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
import jwt
import os
from .database import AsyncSessionLocal
from .user_service import register_user, authenticate, get_user, update_user, delete_user

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
JWT_SECRET = os.getenv('JWT_SECRET', 'secret')

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    password: str
    role: str = Field(..., pattern='^(admin|buyer|seller|operator)$')

class LoginRequest(BaseModel):
    user_id: int
    password: str

class UserOut(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    role: str
    phone: str | None = None
    avatar: str | None = None
    passport_number: str | None = None
    birth_date: str | None = None
    tax_id: str | None = None
    locale: str | None = None

class UpdateUserRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    phone: str | None
    avatar: str | None

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

async def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

@router.post('/register', status_code=201)
async def register(req: RegisterRequest, db: AsyncSessionLocal = Depends(get_db)):
    user_id = await register_user(db, req.dict())
    token = jwt.encode({'user_id': user_id, 'role': req.role}, JWT_SECRET, algorithm='HS256')
    return {'access_token': token}

@router.post('/login')
async def login(req: LoginRequest, db: AsyncSessionLocal = Depends(get_db)):
    token = await authenticate(db, req.user_id, req.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return {'access_token': token}

@router.get('/{user_id}', response_model=UserOut)
async def read_user(user_id: int, token_data: dict = Depends(verify_token), db: AsyncSessionLocal = Depends(get_db)):
    usr = await get_user(db, user_id)
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return usr

@router.put('/{user_id}')
async def update(user_id: int, req: UpdateUserRequest, token_data: dict = Depends(verify_token), db: AsyncSessionLocal = Depends(get_db)):
    if token_data['user_id'] != user_id and token_data['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    ok = await update_user(db, {**req.dict(), 'user_id': user_id})
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'ok': True}

@router.delete('/{user_id}')
async def delete(user_id: int, token_data: dict = Depends(verify_token), db: AsyncSessionLocal = Depends(get_db)):
    ok = await delete_user(db, requester_id=token_data['user_id'], target_id=user_id, role=token_data['role'])
    if not ok:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {'ok': True}
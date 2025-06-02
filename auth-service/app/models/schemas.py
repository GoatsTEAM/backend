from datetime import date
from pydantic import BaseModel, EmailStr, Field
from models.models import RoleEnum, GenderEnum


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: RoleEnum = Field(..., description="buyer or seller")

    class Config:
        use_enum_values = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: GenderEnum | None = None
    phone: str | None = None
    avatar: str | None = None
    passport_number: str | None = None
    birth_date: date | None = None
    tax_id: str | None = None

    class Config:
        use_enum_values = True


class RoleUpdateRequest(BaseModel):
    role: RoleEnum

    class Config:
        use_enum_values = True


class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    first_name: str
    last_name: str
    gender: GenderEnum | None
    phone: str | None
    avatar: str | None
    passport_number: str | None
    birth_date: date | None
    tax_id: str | None
    role: RoleEnum
    is_banned: bool

    class Config:
        use_enum_values = True


class CurrentUser(BaseModel):
    user_id: int
    email: EmailStr
    role: RoleEnum
    is_banned: bool

    class Config:
        use_enum_values = True

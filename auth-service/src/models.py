from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey,
    TIMESTAMP, func, Date, JSON
)
import enum
from .database import Base


class RoleEnum(enum.Enum):
    admin = 'admin'
    buyer = 'buyer'
    seller = 'seller'
    operator = 'operator'


class GenderEnum(enum.Enum):
    male = 'male'
    female = 'female'


class UserCredential(Base):
    __tablename__ = 'users_credentials'
    user_id = Column(Integer, primary_key=True, index=True)
    hash_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)


class UserProfile(Base):
    __tablename__ = 'users_profile'
    user_id = Column(Integer, ForeignKey('users_credentials.user_id'), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    phone = Column(String)
    avatar = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    passport_number = Column(String)
    birth_date = Column(Date)
    tax_id = Column(String)

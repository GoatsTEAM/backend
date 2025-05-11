from sqlalchemy import (
    Column, Integer, String, Enum, Boolean,
    ForeignKey, TIMESTAMP, func, Date
)
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()


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
    email = Column(String, nullable=False, unique=True)
    hash_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum, name='role_enum'), nullable=False)
    is_banned = Column(Boolean, nullable=False, server_default='false')


class UserProfile(Base):
    __tablename__ = 'users_profile'

    user_id = Column(Integer, ForeignKey('users_credentials.user_id'), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(GenderEnum, name='gender_enum'), nullable=True)
    phone = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    passport_number = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    tax_id = Column(String, nullable=True)

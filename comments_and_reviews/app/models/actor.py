from enum import Enum
from pydantic import BaseModel


class Role(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    OPERATOR = "operator"
    ADMIN = "admin"


class Actor(BaseModel):
    id: str
    role: Role

    def is_moderator(self) -> bool:
        return self.role in (Role.OPERATOR, Role.ADMIN)

    def is_seller(self) -> bool:
        return self.role == Role.SELLER

    def is_buyer(self) -> bool:
        return self.role == Role.BUYER

    @classmethod
    def from_jwt(cls, payload: dict) -> "Actor":
        user_id = str(payload["user_id"])
        role: Role = payload["role"]
        return cls(id=user_id, role=role)

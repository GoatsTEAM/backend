from abc import ABC, abstractmethod
from typing import Any

from app.models.base import BaseModel


class User(BaseModel, ABC):
    @abstractmethod
    def is_moderator(self) -> bool: ...


class Buyer(User):
    def __init__(self, id: int, name: str, banned: bool, avatar: str):
        self.id = id
        self.name = name
        self.banned = banned
        self.avatar = avatar

    def is_moderator(self) -> bool:
        return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "banned": self.banned,
            "avatar": self.avatar,
        }

    def is_banned(self) -> bool:
        return self.banned

    def ban(self):
        self.banned = True

    def unban(self):
        self.banned = False


class Seller(User):
    def __init__(self, id: int, name: str, banned: bool):
        self.id = id
        self.name = name
        self.banned = banned

    def is_moderator(self) -> bool:
        return False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "banned": self.banned,
        }


class Moderator(User):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def is_moderator(self) -> bool:
        return True

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name}

    def ban_user(self, user: Buyer):
        user.ban()

    def unban_user(self, user: Buyer):
        user.unban()

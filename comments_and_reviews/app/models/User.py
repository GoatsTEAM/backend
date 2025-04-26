from abc import ABC, abstractmethod
from typing import Any
from bson.objectid import ObjectId

from app.models.Base import BaseModel


class User(BaseModel):
    @abstractmethod
    def is_moderator(self) -> bool: ...


class Bannable(ABC):
    @abstractmethod
    def is_banned(self) -> bool: ...

    @abstractmethod
    def ban(self): ...

    @abstractmethod
    def unban(self): ...


class Buyer(User, Bannable):
    def __init__(self, id: ObjectId, name: str, banned: bool, avatar: str):
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


class Seller(User, Bannable):
    def __init__(self, id: ObjectId, name: str, banned: bool):
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

    def is_banned(self) -> bool:
        return self.banned

    def ban(self):
        self.banned = True

    def unban(self):
        self.banned = False


class Moderator(User):
    def __init__(self, id: ObjectId, name: str):
        self.id = id
        self.name = name

    def is_moderator(self) -> bool:
        return True

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name}

    def ban_user(self, user: Bannable):
        user.ban()

    def unban_user(self, user: Bannable):
        user.unban()

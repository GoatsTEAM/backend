from abc import ABC, abstractmethod

from bson.objectid import ObjectId

from app.models.user import User, Buyer


class UsersRepository(ABC):
    @abstractmethod
    async def get_buyer_by_id(self, id: ObjectId) -> Buyer | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

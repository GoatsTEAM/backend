from abc import ABC, abstractmethod

from app.models.user import User


class UsersRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def save(self, user: User): ...

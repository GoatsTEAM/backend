from abc import ABC, abstractmethod

from app.models.moderation_request import ModerationRequest


class ModerationRequestsRepository(ABC):
    @abstractmethod
    async def create_moderation_request(
        self, review_id: str, description: str
    ) -> ModerationRequest: ...

    @abstractmethod
    async def get_opened_moderation_requests(
        self,
    ) -> list[ModerationRequest]: ...

    @abstractmethod
    async def get_moderation_request_by_id(
        self, request_id: str
    ) -> ModerationRequest | None: ...

    @abstractmethod
    async def save(self, request: ModerationRequest): ...

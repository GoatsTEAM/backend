from app.db.mongo.models.moderation_request_document import (
    ModerationRequestDocument,
)
from app.models.moderation_request import ModerationRequest
from app.repositories.moderation_requests_repository import (
    ModerationRequestsRepository,
)


class ModerationRequestsRepositoryBeanie(ModerationRequestsRepository):
    async def create_moderation_request(
        self, review_id: str, description: str
    ) -> ModerationRequest:
        new_request = ModerationRequestDocument(
            review_id=review_id, description=description
        )
        new_request = await new_request.insert()
        return new_request.to_moderation_request()

    async def get_opened_moderation_requests(self) -> list[ModerationRequest]:
        result = await ModerationRequestDocument.find_many(
            ModerationRequestDocument.decision == None  # noqa: E711
        ).to_list()
        return [request.to_moderation_request() for request in result]

    async def get_moderation_request_by_id(
        self, request_id: str
    ) -> ModerationRequest | None:
        result = await ModerationRequestDocument.get(request_id)
        if result is None:
            return None
        else:
            return result.to_moderation_request()

    async def save(self, request: ModerationRequest):
        document = ModerationRequestDocument.from_moderation_request(request)
        await document.save()

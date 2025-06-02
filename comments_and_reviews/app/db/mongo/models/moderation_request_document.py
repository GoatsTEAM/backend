from datetime import datetime
from beanie import Document, PydanticObjectId
from pymongo import IndexModel, ASCENDING, DESCENDING

from app.models.moderation_request import ModerationRequest, Decision


class ModerationRequestDocument(Document):
    review_id: str
    description: str
    created_at: datetime = datetime.now()
    decision: Decision | None = None

    class Settings:
        name = "moderation_requests"
        indexes = [
            IndexModel(
                [
                    ("review_id", ASCENDING),
                    ("created_at", DESCENDING),
                ],
                name="review_id_created_at_idx",
            ),
            IndexModel([("created_at", DESCENDING)], name="created_at_idx"),
        ]

    def to_moderation_request(self) -> ModerationRequest:
        return ModerationRequest(
            id=str(self.id),
            review_id=self.review_id,
            description=self.description,
            created_at=self.created_at,
            decision=self.decision,
        )

    @classmethod
    def from_moderation_request(
        cls, moderation_request: ModerationRequest
    ) -> "ModerationRequestDocument":
        return cls(
            id=PydanticObjectId(moderation_request.id),
            review_id=moderation_request.review_id,
            description=moderation_request.description,
            created_at=moderation_request.created_at,
            decision=moderation_request.decision,
        )

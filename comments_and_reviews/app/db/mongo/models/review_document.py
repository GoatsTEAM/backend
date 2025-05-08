from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel, ASCENDING, DESCENDING

from app.models.review import (
    Review,
    ReviewContent,
    ReviewMetadata,
    ReviewStatus,
)


class ReviewDocument(Document):
    author_id: str
    content: ReviewContent
    metadata: ReviewMetadata
    answer: str | None = None
    likes: int = Field(default=0, ge=0)
    status: ReviewStatus = ReviewStatus.PENDING

    class Settings:
        name = "reviews"
        indexes = [
            IndexModel(
                [
                    ("metadata.product_id", ASCENDING),
                    ("author_id", ASCENDING),
                ],
                name="unique_product_author",
                unique=True,
            ),
            IndexModel(
                [
                    ("author_id", ASCENDING),
                    ("metadata.created_at", DESCENDING),
                ],
                name="author_id_created_at_idx",
            ),
            IndexModel(
                [
                    ("metadata.product_id", ASCENDING),
                    ("metadata.created_at", DESCENDING),
                ],
                name="product_id_created_at_idx",
            ),
        ]

    def to_review(self) -> Review:
        return Review(
            id=str(self.id),
            author_id=self.author_id,
            content=self.content,
            metadata=self.metadata,
            answer=self.answer,
            likes=self.likes,
            status=self.status,
        )

    @classmethod
    def from_review(cls, review: Review) -> "ReviewDocument":
        return cls(
            id=PydanticObjectId(review.id),
            author_id=review.author_id,
            content=review.content,
            metadata=review.metadata,
            answer=review.answer,
            likes=review.likes,
            status=review.status,
        )

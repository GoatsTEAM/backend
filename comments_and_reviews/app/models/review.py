from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ReviewContent(BaseModel):
    rating: int = Field(ge=1, le=5)
    text: str | None
    media: list[str] = []


class ReviewMetadata(BaseModel):
    product_id: str
    edited_at: datetime = datetime.now()
    created_at: datetime = datetime.now()

    def touch(self) -> "ReviewMetadata":
        return self.model_copy(update={"edited_at": datetime.now()})


class ReviewStatus(str, Enum):
    PUBLISHED = "published"
    PENDING = "pending"
    HIDDEN = "hidden"


class Review(BaseModel):
    id: str
    author_id: str
    content: ReviewContent
    metadata: ReviewMetadata
    answer: str | None = None
    likes: int = Field(default=0, ge=0)
    status: ReviewStatus = ReviewStatus.PENDING

    def update_content(self, new_content: ReviewContent) -> "Review":
        if not self.is_editable():
            raise ValueError("Can't update hidden review")
        return self.model_copy(
            update={
                "content": new_content,
                "metadata": self.metadata.touch(),
                "status": ReviewStatus.PENDING,
            }
        )

    def is_editable(self) -> bool:
        return self.status in (ReviewStatus.PUBLISHED, ReviewStatus.PENDING)

    def publish(self) -> "Review":
        if not self.is_on_moderation():
            raise ValueError("Only pending review can be published")
        return self.model_copy(update={"status": ReviewStatus.PUBLISHED})

    def hide(self) -> "Review":
        if not self.is_on_moderation():
            raise ValueError("Can't hide hidden review")
        return self.model_copy(update={"status": ReviewStatus.HIDDEN})

    def is_on_moderation(self) -> bool:
        return self.status == ReviewStatus.PENDING

    def to_moderation(self) -> "Review":
        if not self.is_published():
            raise ValueError("Only published review can be sent to moderation")
        return self.model_copy(update={"status": ReviewStatus.PENDING})

    def is_published(self) -> bool:
        return self.status == ReviewStatus.PUBLISHED

    def add_answer(self, answer: str) -> "Review":
        return self.model_copy(update={"answer": answer})

    def has_answer(self) -> bool:
        return self.answer is not None

    def check_author(self, author_id: str) -> bool:
        return self.author_id == author_id

    def get_product(self) -> str:
        return self.metadata.product_id

    def get_rating(self) -> int:
        return self.content.rating

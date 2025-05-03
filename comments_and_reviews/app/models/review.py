from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


from app.models.base import BaseModel
from app.models.user import Buyer


class ReviewStatus(str, Enum):
    PUBLISHED = "published"
    PENDING = "pending"
    HIDDEN = "hidden"


@dataclass
class ReviewContent:
    rating: int
    text: str | None
    media: list[str] | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReviewMetadata:
    product_id: int
    returned_order: bool
    edited_at: datetime
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def touch(self):
        self.edited_at = datetime.now()


class Review(BaseModel, ABC):
    pass


class ReviewForAuthor(Review, ABC):
    @abstractmethod
    def update(self, content: ReviewContent): ...


class ReviewForModerator(Review, ABC):
    @abstractmethod
    def get_author(self) -> Buyer: ...

    @abstractmethod
    def publish(self): ...

    @abstractmethod
    def hide(self): ...


class ReviewForSeller(Review, ABC):
    @abstractmethod
    def to_moderation(self): ...

    @abstractmethod
    def add_answer(self, answer: str): ...


class ReviewImpl(
    ReviewForAuthor,
    ReviewForModerator,
    ReviewForSeller,
):
    def __init__(
        self,
        id: ObjectId,
        author: Buyer,
        status: ReviewStatus,
        content: ReviewContent,
        answer: str | None,
        likes: int,
        metadata: ReviewMetadata,
    ):
        self.id = id
        self.author = author
        self.status = status
        self.content = content
        self.answer = answer
        self.likes = likes
        self.metadata = metadata

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "author": self.author.to_dict(),
            "status": self.status,
            "content": self.content.to_dict(),
            "answer": self.answer,
            "likes": self.likes,
            "metadata": self.metadata.to_dict(),
        }

    def update(self, content: ReviewContent):
        self.content = content
        self.metadata.touch()
        self.to_moderation()

    def publish(self):
        self.status = ReviewStatus.PUBLISHED

    def hide(self):
        self.status = ReviewStatus.HIDDEN

    def to_moderation(self):
        self.status = ReviewStatus.PENDING

    def add_answer(self, answer: str):
        self.answer = answer

    def get_author(self) -> Buyer:
        return self.author

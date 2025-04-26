from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any


from app.models.Base import BaseModel
from app.models.User import Buyer


class Status(str, Enum):
    PUBLISHED = "published"
    PENDING = "pending"
    HIDDEN = "hidden"


@dataclass
class ReviewContent:
    rating: int
    text: str | None
    media: list[str] | None


@dataclass
class ReviewMetadata:
    product_id: ObjectId
    returned_order: bool
    edited_at: datetime
    created_at: datetime

    def touch(self):
        self.edited_at = datetime.now()


class ReviewForAuthor(ABC):
    @abstractmethod
    def update(self, content: ReviewContent): ...


class ReviewForBuyers(ABC):
    @abstractmethod
    def like(self): ...

    @abstractmethod
    def unlike(self): ...


class ReviewForModerator(ABC):
    @abstractmethod
    def publish(self): ...

    @abstractmethod
    def hide(self): ...


class ReviewForSeller(ABC):
    @abstractmethod
    def to_moderation(self): ...

    @abstractmethod
    def add_answer(self, answer: str): ...


class Review(
    BaseModel,
    ReviewForAuthor,
    ReviewForBuyers,
    ReviewForModerator,
    ReviewForSeller,
):
    def __init__(
        self,
        id: ObjectId,
        author: Buyer,
        status: Status,
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
            "content": asdict(self.content),
            "answer": self.answer,
            "likes": self.likes,
            "metadata": asdict(self.metadata),
        }

    def update(self, content: ReviewContent):
        self.content = content
        self.metadata.touch()
        self.to_moderation()

    def like(self):
        self.likes += 1

    def unlike(self):
        if self.likes > 0:
            self.likes -= 1

    def publish(self):
        self.status = Status.PUBLISHED

    def hide(self):
        self.status = Status.HIDDEN

    def to_moderation(self):
        self.status = Status.PENDING

    def add_answer(self, answer: str):
        self.answer = answer

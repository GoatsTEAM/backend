from abc import ABC, abstractmethod
from bson.objectid import ObjectId

from app.models.review import (
    Review,
    ReviewForAuthor,
    ReviewForModerator,
    ReviewForSeller,
    ReviewMetadata,
    ReviewContent,
)
from app.models.user import Buyer


class ReviewsRepository(ABC):
    @abstractmethod
    async def get_reviews_by_product_id(
        self, product_id: int
    ) -> list[Review]: ...

    @abstractmethod
    async def save(self, review: Review): ...


class ReviewsRepositoryForAuthor(ReviewsRepository, ABC):
    @abstractmethod
    async def get_review_for_author_by_id(
        self, id: ObjectId
    ) -> ReviewForAuthor | None: ...

    @abstractmethod
    async def create(
        self, author: Buyer, content: ReviewContent, metadata: ReviewMetadata
    ) -> Review: ...

    @abstractmethod
    async def delete(self, author_id: int, review_id: ObjectId): ...


class ReviewsRepositoryForBuyers(ReviewsRepository, ABC):
    @abstractmethod
    async def like(self, user_id: int, review_id: ObjectId): ...

    @abstractmethod
    async def dislike(self, user_id: int, review_id: ObjectId): ...


class ReviewsRepositoryForSellers(ReviewsRepository, ABC):
    @abstractmethod
    async def get_review_for_seller_by_id(
        self, id: ObjectId
    ) -> ReviewForSeller: ...


class ReviewsRepositoryForModerators(ReviewsRepository, ABC):
    @abstractmethod
    async def get_review_for_moderator_by_id(
        self, id: ObjectId
    ) -> ReviewForModerator: ...

from abc import ABC, abstractmethod
from app.models.review import Review, ReviewContent, ReviewMetadata
from app.models.reviews_statistics import ReviewsStatistics


class ReviewsRepository(ABC):
    @abstractmethod
    async def create_review(
        self, author_id: str, content: ReviewContent, metadata: ReviewMetadata
    ) -> Review: ...

    @abstractmethod
    async def get_review_by_id(self, review_id: str) -> Review | None: ...

    @abstractmethod
    async def save(self, review: Review): ...

    @abstractmethod
    async def get_reviews_by_product_id(
        self, product_id: str
    ) -> list[Review]: ...

    @abstractmethod
    async def get_reviews_by_author_id(
        self, author_id: str
    ) -> list[Review]: ...

    @abstractmethod
    async def calculate_stats(self, product_id: str) -> ReviewsStatistics: ...

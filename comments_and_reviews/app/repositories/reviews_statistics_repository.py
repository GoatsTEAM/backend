from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from app.models.reviews_statistics import ReviewsStatistics


class ReviewsStatisticsRepository(ABC):
    @abstractmethod
    async def get_stats(self, product_id: str) -> ReviewsStatistics | None: ...

    @abstractmethod
    async def save(self, stats: ReviewsStatistics): ...

    @abstractmethod
    async def lock(
        self, product_id: str
    ) -> AbstractAsyncContextManager[None]: ...

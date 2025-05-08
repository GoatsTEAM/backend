from app.models.reviews_statistics import ReviewsStatistics
from app.repositories.reviews_repository import ReviewsRepository
from app.repositories.reviews_statistics_repository import (
    ReviewsStatisticsRepository,
)


class ReviewsStatisticsService:
    def __init__(
        self,
        stats_repository: ReviewsStatisticsRepository,
        reviews_repository: ReviewsRepository,
    ):
        self.stats = stats_repository
        self.reviews = reviews_repository

    async def update_stats_if_exists(
        self,
        product_id: str,
        new_rating: int | None = None,
        old_rating: int | None = None,
    ) -> None:
        if (new_rating is None and old_rating is None) or (
            new_rating == old_rating
        ):
            return

        statistics = await self.stats.get_stats(product_id)
        if statistics is None:
            return

        if old_rating is not None:
            statistics.remove_review(old_rating)

        if new_rating is not None:
            statistics.add_review(new_rating)

        await self.stats.save(statistics)

    async def get_stats(self, product_id: str) -> ReviewsStatistics:
        stats = await self.stats.get_stats(product_id)
        if stats is None:
            stats = await self.reviews.calculate_stats(product_id)
        return stats

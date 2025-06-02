from redis.asyncio import Redis

from app.db import (
    ModerationRequestsRepositoryBeanie,
    ReviewsRepositoryBeanie,
    ReviewsStatisticsRepositoryRedis,
)

from app.services import (
    ReviewsModerationService,
    ReviewsService,
    ReviewsStatisticsService,
    ServicesFactory,
)


class ServicesFactoryImpl(ServicesFactory):
    def __init__(self, redis: Redis):
        self.moderation_repo = ModerationRequestsRepositoryBeanie()
        self.reviews_repo = ReviewsRepositoryBeanie()
        self.stats_repo = ReviewsStatisticsRepositoryRedis(redis)

    def get_reviews_moderation_service(self) -> ReviewsModerationService:
        return ReviewsModerationService(self.moderation_repo, self.reviews_repo)

    def get_reviews_service(self) -> ReviewsService:
        return ReviewsService(self.reviews_repo, self.stats_repo)

    def get_reviews_statistics_service(self) -> ReviewsStatisticsService:
        return ReviewsStatisticsService(self.stats_repo, self.reviews_repo)


def get_services_factory() -> ServicesFactory:
    from app.db import init_redis

    redis = init_redis()
    return ServicesFactoryImpl(redis)

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from redis.asyncio import Redis
from pottery import AIORedlock


from app.models.reviews_statistics import ReviewsStatistics
from app.repositories.reviews_statistics_repository import (
    ReviewsStatisticsRepository,
)


class ReviewsStatisticsRepositoryRedis(ReviewsStatisticsRepository):
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.lock_ttl = 5
        self.default_ttl = 60 * 60 * 24

    def _key(self, product_id: str):
        return f"stats:{product_id}"

    def _lock_key(self, product_id: str) -> str:
        return f"stats_lock:{product_id}"

    async def get_stats(self, product_id: str) -> ReviewsStatistics | None:
        key = self._key(product_id)
        value = await self.redis.get(key)
        if value is None:
            return None

        await self.redis.expire(key, self.default_ttl)
        return ReviewsStatistics.model_validate_json(value)

    async def save(self, stats: ReviewsStatistics):
        key = self._key(stats.id)
        value = stats.model_dump_json()
        await self.redis.set(key, value, ex=self.default_ttl)

    @asynccontextmanager
    async def lock(self, product_id: str) -> AsyncGenerator[None, None]:
        key = self._lock_key(product_id)
        lock = AIORedlock(
            key=key, masters={self.redis}, auto_release_time=self.lock_ttl
        )
        await lock.acquire(raise_on_redis_errors=True, timeout=self.lock_ttl)
        try:
            yield
        finally:
            await lock.release()

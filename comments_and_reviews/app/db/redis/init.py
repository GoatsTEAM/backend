from redis.asyncio import Redis
from app.core.config import settings


def init_redis(url: str = settings.REDIS_URL) -> Redis:
    return Redis.from_url(url)

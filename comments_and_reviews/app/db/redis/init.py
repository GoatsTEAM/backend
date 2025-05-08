from redis.asyncio import Redis


def init_redis(url: str) -> Redis:
    return Redis.from_url(url)

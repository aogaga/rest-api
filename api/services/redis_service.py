import json
from common import  logger, Optional
import redis.asyncio as redis
from config import REDIS_URL  # make sure REDIS_URL is defined in your config


class RedisService:
    def __init__(self):
        self.redis = redis.from_url(REDIS_URL)

    async def get(self, key: str) -> Optional[dict]:
        try:
            cached = await self.redis.get(key)
            if cached:
                logger.info("Cache hit for key: %s", key)
                return json.loads(cached)
            logger.info("Cache miss for key: %s", key)
            return None
        except Exception as e:
            logger.exception("Redis get error for key: %s", key)
            return None

    async def set(self, key: str, value: dict, ex: int = 3600):
        try:
            await self.redis.set(key, json.dumps(value), ex=ex)
            logger.info("Cached key: %s with expiry: %d seconds", key, ex)
        except Exception as e:
            logger.exception("Redis set error for key: %s", key)
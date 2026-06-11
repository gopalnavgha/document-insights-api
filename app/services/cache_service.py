from app.db.redis import redis_client

from app.core.config import settings

import json


class CacheService:

    @staticmethod
    def get_cache_key(
            user_id: str,
            content_hash: str
    ):
        return (
            f"summary:"
            f"{user_id}:"
            f"{content_hash}"
        )

    @staticmethod
    def get_summary(
            user_id: str,
            content_hash: str
    ):

        key = (
            CacheService
            .get_cache_key(
                user_id,
                content_hash
            )
        )

        data = redis_client.get(key)

        if not data:
            return None

        return json.loads(data)

    @staticmethod
    def set_summary(
            user_id: str,
            content_hash: str,
            summary: str
    ):

        key = (
            CacheService
            .get_cache_key(
                user_id,
                content_hash
            )
        )

        redis_client.setex(
            key,
            settings.CACHE_TTL,
            json.dumps(
                {
                    "summary": summary
                }
            )
        )
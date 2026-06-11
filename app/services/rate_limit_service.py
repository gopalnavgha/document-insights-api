from app.db.redis import redis_client

from app.core.config import settings


class RateLimitService:

    @staticmethod
    def get_active_jobs_key(
        user_id: str
    ):
        return f"active_jobs:{user_id}"

    @staticmethod
    def get_active_jobs_count(
        user_id: str
    ):

        key = (
            RateLimitService
            .get_active_jobs_key(
                user_id
            )
        )

        value = redis_client.get(
            key
        )

        return int(value or 0)

    @staticmethod
    def can_submit_job(
        user_id: str
    ):

        count = (
            RateLimitService
            .get_active_jobs_count(
                user_id
            )
        )

        return (
            count <
            settings.MAX_ACTIVE_JOBS
        )

    @staticmethod
    def increment_job(
        user_id: str
    ):

        key = (
            RateLimitService
            .get_active_jobs_key(
                user_id
            )
        )

        redis_client.incr(key)

    @staticmethod
    def decrement_job(
        user_id: str
    ):

        key = (
            RateLimitService
            .get_active_jobs_key(
                user_id
            )
        )

        value = redis_client.get(
            key
        )

        if value:

            redis_client.decr(key)
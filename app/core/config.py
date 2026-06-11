from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MONGO_URI: str

    DB_NAME: str

    REDIS_HOST: str

    REDIS_PORT: int

    MAX_ACTIVE_JOBS: int

    CACHE_TTL: int

    class Config:
        env_file = ".env"


settings = Settings()
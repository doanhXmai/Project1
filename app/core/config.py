from functools import lru_cache

from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Play Music - FastAPI"
    API_VERSION: str = "/api/v1"

    DATABASE_URL: str | None = None

    STORAGE_PUBLIC_PATH: str = "/storage/v1/object/public"
    DEFAULT_IMAGE_BUCKET: str = "images"
    DEFAULT_AUDIO_BUCKET: str = "audios"

    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    SUPABASE_SERVICE_ROLE: str | None = None
    SUPABASE_JWT_SECRET: str | None = None

    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
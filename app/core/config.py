from datetime import datetime, timezone
from functools import lru_cache

from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Play Music - FastAPI"
    API_VERSION: str = "/api/v1"

    DATABASE_URL: str | None = None

    STORAGE_PUBLIC_PATH: str = "/storage/v1/object/public"

    IMAGE_BUCKET: str = "images"
    AUDIO_BUCKET: str = "audios"
    LYRIC_BUCKET: str = "lyrics"

    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    SUPABASE_SERVICE_ROLE: str | None = None
    SUPABASE_JWT_SECRET: str | None = None

    SECRET_KEY: str | None = None
    ALGORITHM: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM: str | None = None


    DATE_NOW: datetime = datetime.now(timezone.utc).isoformat()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
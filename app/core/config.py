from functools import lru_cache

from pydantic import computed_field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    """
    Application settings loaded from .env
    """

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    MINIO_HOST: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET_NAME: str

    class Config:
        env_file = ".env"

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the database URL from environment variables.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" \
               f"{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"


    @computed_field
    @property
    def MINIO_URL(self) -> str:
        """
        Constructs the MinIO URL from environment variables.
        """
        return f"http://{self.MINIO_HOST}:9000"


@lru_cache()
def get_settings():
    return _Settings()


settings = get_settings()

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE = 5 * 1024 * 1024

from functools import lru_cache
from typing import Tuple

from pydantic import BaseSettings, ConfigDict, Field, field_validator


class Settings(BaseSettings):
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    google_cse_id: str = Field(..., env="GOOGLE_CSE_ID")

    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")

    max_image_size: Tuple[int, int] = Field(default=(800, 600), env="MAX_IMAGE_SIZE")

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("postgres_port", mode="before")
    def parse_postgres_port(cls, v):
        if isinstance(v, str):
            try:
                port = int(v)
                if port <= 0 or port > 65535:
                    raise ValueError
                return port
            except Exception:
                raise ValueError(
                    "POSTGRES_PORT must be a valid port number between 1 and 65535"
                )
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()

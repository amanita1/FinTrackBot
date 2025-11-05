from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, PostgresDsn


def _split_origins(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    bot_token: str = Field("", alias="BOT_TOKEN")
    database_url: PostgresDsn = Field(
        "postgresql+psycopg://postgres:postgres@localhost:5432/fintrack",
        alias="DATABASE_URL",
    )
    timezone: str = Field("Asia/Almaty", alias="TZ")
    allowed_origins_raw: str = Field("http://localhost:5173", alias="ALLOWED_ORIGINS")
    webapp_host: str = Field("0.0.0.0", alias="WEBAPP_HOST")
    webapp_port: int = Field(8080, alias="WEBAPP_PORT")
    webhook_base: str = Field("", alias="WEBHOOK_BASE")
    digest_hour: int = Field(9, alias="DIGEST_HOUR")
    reminder_hour: int = Field(22, alias="REMINDER_HOUR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def allowed_origins(self) -> List[str]:
        return _split_origins(self.allowed_origins_raw)


@lru_cache()
def get_settings() -> Settings:
    return Settings()


__all__ = ["Settings", "get_settings"]

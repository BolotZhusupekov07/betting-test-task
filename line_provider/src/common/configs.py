import os

from pydantic_settings import BaseSettings

from src.common.enums import EnvironmentEnum


class DBSettings(BaseSettings):
    db_title: str = "line_provider"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_port: int = 5432
    db_host: str = "127.0.0.1"

    pool_pre_ping: bool = False
    pool_size: int = 5
    pool_recycle: int = -1
    max_overflow: int = 10
    echo: bool = False
    expire_on_commit: bool = False
    autocommit: bool = False

    def _get_url(self) -> str:
        return f"{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_title}"

    def get_url(self) -> str:
        url = self._get_url()
        return f"postgresql://{url}"

    def get_async_url(self) -> str:
        url = self._get_url()
        return f"postgresql+asyncpg://{url}"


class Settings(BaseSettings):
    project_name: str = "betting"

    backend_cors_origins: list[str] = ["*"]

    db: DBSettings = DBSettings()

    environment: EnvironmentEnum = EnvironmentEnum.dev

    domain_name: str = "http://localhost"

    api_path: str = "/api/"

    bet_maker_service_domain: str = 'http://bet_maker:5000'


async def get_settings() -> Settings:
    return Settings()


settings = Settings()


logging_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": (
                "{name} {levelname} {asctime} {module} "
                "{process:d} {thread:d} {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "handlers": [
                "console",
            ],
            "propagate": True,
        }
    },
}

from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    # Postgres credentials
    POSTGRES_DB_NAME: str
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_POOL_MIN_SIZE: int = 3
    POSTGRES_POOL_MAX_SIZE: int = 5
    POSTGRES_DSN: str | None = None

    # Redis
    REDIS_URL: str = ""
    REDIS_POOL_MAX_SIZE: int = 15

    # TG BOT
    TG_TOKEN: str

    tz: ZoneInfo = ZoneInfo("Asia/Yekaterinburg")

    @model_validator(mode="after")
    def fill_optional_fields(self):
        self.POSTGRES_DSN = str(
            PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=self.POSTGRES_DB_USER,
                password=self.POSTGRES_DB_PASSWORD,
                host=self.POSTGRES_DB_HOST,
                path=self.POSTGRES_DB_NAME,
                port=self.POSTGRES_DB_PORT,
            )
        )
        return self

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=True,
        env_file=BASE_DIR / ".env",
    )


class LoggingSettings(BaseSettings):
    # main
    IS_NEED_LOG_SQL_QUERIES: bool = False

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=True,
        env_file=BASE_DIR / ".env",
    )


settings = Settings()  # type: ignore
logging_settings = LoggingSettings()

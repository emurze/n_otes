import logging
import sys
from pathlib import Path
from typing import Literal

from colorlog import ColoredFormatter
from pydantic import Field, BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).parent


class AuthJWTConfig(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    token_type_key: str = "type"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"


class ApiConfig(BaseModel):
    v1_prefix: str = "/api/v1"
    title: str = "App"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    secret_key: SecretStr
    allowed_origins: list[str] = []
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]
    allow_credentials: bool = True
    gzip_minimum_size: int = 1000
    gzip_compress_level: int = 7


class DatabaseConfig(BaseModel):
    pool_size: int = 20
    pool_max_overflow: int = 0
    echo: bool = False
    dsn: str


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "DEBUG"
    log_format: str = (
        "%(log_color)s%(asctime)s %(name)-12s %(levelname)s%(reset)s:   "
        "%(message)s"
    )
    log_date_format: str = "%Y-%m-%d %H:%M:%S"
    log_colors: dict = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }

    def configure(self, log_level: str | None = None) -> None:
        handler = logging.StreamHandler(sys.stdout)
        formatter = ColoredFormatter(
            self.log_format,
            datefmt=self.log_date_format,
            log_colors=self.log_colors,
        )
        handler.setFormatter(formatter)
        logging.basicConfig(
            level=log_level or self.log_level,
            handlers=[handler],
        )


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        extra="allow",
    )
    api: ApiConfig = Field(default_factory=ApiConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    jwt: AuthJWTConfig = Field(default_factory=AuthJWTConfig)
    debug: bool = True

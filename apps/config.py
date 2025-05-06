from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class BaseConfiguration(BaseModel):
    class Config:
        extra = "allow"

class Celery(BaseConfiguration):
    """
    Переменные окружения Celery.
    """

    broker_url: str
    result_backend: str


class PostgreSQL(BaseConfiguration):
    """
    Переменные окружения PgSQL
    """

    name: str
    user: str
    password: str
    host: str
    port: str


class Redis(BaseConfiguration):
    """
    Переменные окружения Redis.
    """
    url: str


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    celery: Celery
    postgresql: PostgreSQL
    redis: Redis

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = False


CONFIG = Settings()

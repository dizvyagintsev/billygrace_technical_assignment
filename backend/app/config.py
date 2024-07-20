from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_dsn: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_ttl_minutes: int

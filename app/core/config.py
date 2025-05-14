import logging
from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class StripeConfig(BaseModel):
    secret_key: str
    public_key: str

class JwtConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_expire_min: int
    refresh_expire_days: int

class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

class DatabaseConfig(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )

    @property
    def sync_url(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )

class LoggingConfig(BaseModel):
    level: str = "info"

    @property
    def level_value(self) -> int:
        return logging.getLevelNamesMapping().get(self.level.upper(), logging.INFO)

class ApiConfig(BaseModel):
    prefix: str = "/api/v1"

class Settings(BaseSettings):
    db: DatabaseConfig
    jwt: JwtConfig
    redis: RedisConfig = RedisConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiConfig = ApiConfig()
    stripe: StripeConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

def get_attr(name: str):
    return getattr(get_settings(), name)




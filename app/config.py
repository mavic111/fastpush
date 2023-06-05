from pydantic import BaseSettings


class Settings(BaseSettings):
    VAPID_PRIVATE_KEY: str
    EMAIL_ADDRESS: str
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str
    REGEX_ORIGINS: str

    class Config:
        env_file = "./app/.env"


settings = Settings()

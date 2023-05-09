from pydantic import BaseSettings

class Settings(BaseSettings):
    VAPID_PRIVATE_KEY: str
    EMAIL_ADDRESS: str
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOSTNAME: str
    CORS_HOSTNAME: str

    class Config:
        env_file = './.env'

settings = Settings()
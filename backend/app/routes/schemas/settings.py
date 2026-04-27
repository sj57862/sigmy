from pydantic_settings import BaseSettings
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL:str
    APP_URL:str
    REDIS_BROKER_URL:str
    REDIS_BACKEND_URL:str

    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRES_DAYS:int
    REGISTER_TOKEN_EXPIRES_MINUTES:int
    SECRET_KEY:str
    ALGORITHM:str

    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM_NAME:str
    MAIL_STARTTLS:bool
    MAIL_SSL_TLS:bool
    USE_CREDENTIALS:bool
    VALIDATE_CERTS:bool

    class Config:
        env_file = BASE_PATH/".env"
        env_file_encoding = "utf-8"

SETTINGS = Settings()
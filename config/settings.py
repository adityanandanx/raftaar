from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    RAZORPAY_API_KEY: str
    RAZORPAY_API_SECRET: str
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1025
    SMTP_USER: str = "test@example.com"
    SMTP_PASSWORD: str = "test"
    SENDER_EMAIL: str = "noreply@raftaar.com"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 15 * 24  # 15 days
    
    class Config:
        env_file = ".env"

settings = Settings()

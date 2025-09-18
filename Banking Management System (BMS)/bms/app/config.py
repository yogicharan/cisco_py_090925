import os
from dataclasses import dataclass


@dataclass
class Config:
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 1025))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@example.com")
    OWNER_EMAIL: str = os.getenv("OWNER_EMAIL", "owner@example.com")
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", 10))
    LOG_JSON: bool = bool(os.getenv("LOG_JSON", False))

    @classmethod
    def from_env(cls):
        return cls()

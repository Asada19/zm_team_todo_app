import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DB_NAME = os.getenv("PG_DB_NAME")
DB_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")


class Settings(BaseSettings):
    sqlalchemy_string: str = (
        f"postgresql+asyncpg://{DB_USER}:{PG_PASSWORD}@db:5432/{DB_NAME}"
    )


settings = Settings()

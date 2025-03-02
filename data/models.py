# mypy: ignore-errors

from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Tuple

class AssetSchema(BaseModel):
    name: str = Field(..., max_length=255)
    value: float
    acquisition_date: date
    history: List[Tuple[date, float]] = []


class DatabaseSettings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    class Config:
        env_file = ".env"  # Load settings from a .env file

db_settings = DatabaseSettings()
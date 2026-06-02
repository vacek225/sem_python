from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    secret_key: str
    database_url: str
    fastapi_url: str
    model_path: str
    log_level: str


def get_settings() -> AppSettings:
    return AppSettings(
        secret_key=os.getenv("SECRET_KEY", "dev-secret-key"),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://sem_user:sem_password@localhost:5432/sem_db",
        ),
        fastapi_url=os.getenv("FASTAPI_URL", "http://localhost:8000"),
        model_path=os.getenv("MODEL_PATH", "models/iris_model.joblib"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )

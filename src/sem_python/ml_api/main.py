from __future__ import annotations

import logging

from fastapi import FastAPI

from sem_python.infrastructure.logging import configure_logging
from sem_python.infrastructure.settings import get_settings
from sem_python.ml_api.model import IrisModelService
from sem_python.ml_api.schemas import (
    HealthResponse,
    IrisFeatures,
    ModelInfoResponse,
    PredictionResponse,
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    model_service = IrisModelService(settings.model_path)

    app = FastAPI(title="Semester ML API", version="0.1.0")

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        logger.info("Health check requested")
        return HealthResponse(status="ok")

    @app.get("/model-info", response_model=ModelInfoResponse)
    def model_info() -> ModelInfoResponse:
        logger.info("Model info requested")
        return model_service.info()

    @app.post("/predict", response_model=PredictionResponse)
    def predict(features: IrisFeatures) -> PredictionResponse:
        logger.info("Prediction requested")
        return model_service.predict(features)

    return app


app = create_app()

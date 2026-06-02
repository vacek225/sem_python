from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


class MlApiClient:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    def predict(self, features: dict[str, float]) -> dict[str, Any]:
        response = requests.post(
            f"{self._base_url}/predict",
            json=features,
            timeout=self._timeout_seconds,
        )
        response.raise_for_status()
        logger.info("Received prediction from ML API")
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("ML API returned an invalid prediction payload")
        return data

    def model_info(self) -> dict[str, Any]:
        response = requests.get(f"{self._base_url}/model-info", timeout=self._timeout_seconds)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("ML API returned an invalid model-info payload")
        return data

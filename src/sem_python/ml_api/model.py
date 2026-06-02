from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sem_python.ml_api.schemas import IrisFeatures, ModelInfoResponse, PredictionResponse

logger = logging.getLogger(__name__)

FEATURE_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
CLASS_NAMES = ["setosa", "versicolor", "virginica"]
MODEL_VERSION = "1.0.0"


def train_and_save_model(model_path: Path) -> None:
    iris = load_iris()
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ],
    )
    pipeline.fit(iris.data, iris.target)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)
    logger.info("Trained and saved Iris model to %s", model_path)


class IrisModelService:
    def __init__(self, model_path: str) -> None:
        self._model_path = Path(model_path)
        if not self._model_path.exists():
            logger.info("Model file does not exist; training a new model")
            train_and_save_model(self._model_path)
        self._model: Any = joblib.load(self._model_path)
        logger.info("Loaded Iris model from %s", self._model_path)

    def predict(self, features: IrisFeatures) -> PredictionResponse:
        values = [
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ],
        ]
        class_id = int(self._model.predict(values)[0])
        return PredictionResponse(class_id=class_id, species=CLASS_NAMES[class_id])

    def info(self) -> ModelInfoResponse:
        return ModelInfoResponse(
            name="Iris Random Forest Classifier",
            version=MODEL_VERSION,
            feature_types={feature: "float > 0" for feature in FEATURE_NAMES},
            classes=CLASS_NAMES,
        )

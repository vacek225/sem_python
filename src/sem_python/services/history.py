from __future__ import annotations

from typing import Any

from sem_python.domain.entities import NewPredictionRecord, PredictionRecord
from sem_python.domain.repositories import PredictionRepository


class PredictionHistoryService:
    def __init__(self, predictions: PredictionRepository) -> None:
        self._predictions = predictions

    def save(
        self,
        *,
        user_id: int,
        input_data: dict[str, Any],
        prediction: dict[str, Any],
    ) -> PredictionRecord:
        return self._predictions.add(
            NewPredictionRecord(
                user_id=user_id,
                input_data=input_data,
                prediction=prediction,
            ),
        )

    def list_for_user(self, user_id: int) -> list[PredictionRecord]:
        return self._predictions.list_for_user(user_id)

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

from sem_python.domain.entities import NewPredictionRecord, PredictionRecord
from sem_python.services.history import PredictionHistoryService


class FakePredictionRepository:
    def __init__(self) -> None:
        self._records: list[PredictionRecord] = []
        self._next_id = 1

    def add(self, prediction: NewPredictionRecord) -> PredictionRecord:
        record = PredictionRecord(
            id=self._next_id,
            user_id=prediction.user_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
            created_at=datetime.now(UTC),
        )
        self._next_id += 1
        self._records.append(record)
        return replace(record)

    def list_for_user(self, user_id: int) -> list[PredictionRecord]:
        return [record for record in self._records if record.user_id == user_id]


def test_history_service_saves_prediction() -> None:
    repository = FakePredictionRepository()
    service = PredictionHistoryService(repository)
    input_data: dict[str, Any] = {"sepal_length": 5.1}
    prediction: dict[str, Any] = {"species": "setosa", "class_id": 0}

    saved = service.save(user_id=1, input_data=input_data, prediction=prediction)

    assert saved.user_id == 1
    assert service.list_for_user(1) == [saved]

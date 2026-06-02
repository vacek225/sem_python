from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from sem_python.ml_api.main import create_app


def test_health_endpoint(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "iris_model.joblib"))
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint(monkeypatch: MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "iris_model.joblib"))
    client = TestClient(create_app())

    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )

    assert response.status_code == 200
    assert response.json()["species"] == "setosa"

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class User:
    id: int
    username: str
    hashed_password: str
    created_at: datetime


@dataclass(frozen=True)
class NewUser:
    username: str
    hashed_password: str


@dataclass(frozen=True)
class PredictionRecord:
    id: int
    user_id: int
    input_data: dict[str, Any]
    prediction: dict[str, Any]
    created_at: datetime


@dataclass(frozen=True)
class NewPredictionRecord:
    user_id: int
    input_data: dict[str, Any]
    prediction: dict[str, Any]

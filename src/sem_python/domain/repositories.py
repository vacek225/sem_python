from __future__ import annotations

from typing import Protocol

from sem_python.domain.entities import NewPredictionRecord, NewUser, PredictionRecord, User


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    def add(self, user: NewUser) -> User:
        raise NotImplementedError


class PredictionRepository(Protocol):
    def add(self, prediction: NewPredictionRecord) -> PredictionRecord:
        raise NotImplementedError

    def list_for_user(self, user_id: int) -> list[PredictionRecord]:
        raise NotImplementedError

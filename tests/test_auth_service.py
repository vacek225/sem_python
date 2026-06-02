from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from sem_python.domain.entities import NewUser, User
from sem_python.domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from sem_python.services.auth import AuthService, PasswordHasher


class FakeUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._next_id = 1

    def get_by_id(self, user_id: int) -> User | None:
        return next((user for user in self._users.values() if user.id == user_id), None)

    def get_by_username(self, username: str) -> User | None:
        return self._users.get(username)

    def add(self, user: NewUser) -> User:
        created = User(
            id=self._next_id,
            username=user.username,
            hashed_password=user.hashed_password,
            created_at=datetime.now(UTC),
        )
        self._next_id += 1
        self._users[user.username] = created
        return replace(created)


class FakePasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, password: str, hashed_password: str) -> bool:
        return hashed_password == self.hash(password)


def test_register_creates_user_with_hashed_password() -> None:
    service = AuthService(FakeUserRepository(), FakePasswordHasher())

    user = service.register(" alice ", "secret123")

    assert user.username == "alice"
    assert user.hashed_password == "hashed:secret123"


def test_register_rejects_duplicate_username() -> None:
    service = AuthService(FakeUserRepository(), FakePasswordHasher())
    service.register("alice", "secret123")

    with pytest.raises(UserAlreadyExistsError):
        service.register("alice", "another-secret")


def test_authenticate_rejects_wrong_password() -> None:
    service = AuthService(FakeUserRepository(), FakePasswordHasher())
    service.register("alice", "secret123")

    with pytest.raises(InvalidCredentialsError):
        service.authenticate("alice", "wrong")

from __future__ import annotations

from typing import Protocol

from sem_python.domain.entities import NewUser, User
from sem_python.domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from sem_python.domain.repositories import UserRepository


class PasswordHasher(Protocol):
    def hash(self, password: str) -> str:
        raise NotImplementedError

    def verify(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class AuthService:
    def __init__(self, users: UserRepository, password_hasher: PasswordHasher) -> None:
        self._users = users
        self._password_hasher = password_hasher

    def register(self, username: str, password: str) -> User:
        normalized_username = username.strip()
        if not normalized_username or not password:
            raise InvalidCredentialsError("Username and password are required.")

        existing_user = self._users.get_by_username(normalized_username)
        if existing_user is not None:
            raise UserAlreadyExistsError("User with this username already exists.")

        hashed_password = self._password_hasher.hash(password)
        return self._users.add(
            NewUser(username=normalized_username, hashed_password=hashed_password)
        )

    def authenticate(self, username: str, password: str) -> User:
        user = self._users.get_by_username(username.strip())
        if user is None:
            raise InvalidCredentialsError("Invalid username or password.")

        if not self._password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid username or password.")

        return user

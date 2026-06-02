from __future__ import annotations

from werkzeug.security import check_password_hash, generate_password_hash

from sem_python.services.auth import PasswordHasher


class WerkzeugPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return generate_password_hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, password)

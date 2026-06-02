class DomainError(Exception):
    """Base class for domain-level errors."""


class UserAlreadyExistsError(DomainError):
    """Raised when a username is already registered."""


class InvalidCredentialsError(DomainError):
    """Raised when username or password is invalid."""

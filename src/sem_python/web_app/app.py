from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from flask import Flask
from sqlalchemy.orm import Session, sessionmaker

from sem_python.infrastructure.db import create_session_factory
from sem_python.infrastructure.logging import configure_logging
from sem_python.infrastructure.settings import get_settings
from sem_python.web_app.http_client import MlApiClient
from sem_python.web_app.routes import register_routes


@contextmanager
def get_db_session(app: Flask) -> Iterator[Session]:
    session_factory = app.extensions["session_factory"]
    if not isinstance(session_factory, sessionmaker):
        raise RuntimeError("Database session factory is not configured")
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=settings.secret_key,
        DATABASE_URL=settings.database_url,
        FASTAPI_URL=settings.fastapi_url,
    )
    if test_config is not None:
        app.config.update(test_config)

    database_url = str(app.config["DATABASE_URL"])
    fastapi_url = str(app.config["FASTAPI_URL"])
    app.extensions["session_factory"] = create_session_factory(database_url)
    app.extensions["ml_api_client"] = MlApiClient(fastapi_url)

    register_routes(app)
    return app

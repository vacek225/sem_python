from __future__ import annotations

from pathlib import Path

from sem_python.infrastructure.settings import get_settings
from sem_python.ml_api.model import train_and_save_model


def main() -> None:
    settings = get_settings()
    train_and_save_model(model_path=Path(settings.model_path))


if __name__ == "__main__":
    main()

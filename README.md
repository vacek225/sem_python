# Semester ML Service

ML-сервис с веб-интерфейсом для семестровой работы. Пользователь работает с Flask-приложением, Flask отправляет признаки в FastAPI ML API по HTTP, а PostgreSQL хранит пользователей и историю предсказаний.

## Архитектура

```text
Browser -> Flask Web App :5000 -> FastAPI ML API :8000 -> ML model
                         -> PostgreSQL :5432
```

Код разделён на слои:

- `domain` — бизнес-сущности, исключения и протоколы репозиториев.
- `services` — сценарии регистрации, авторизации и сохранения истории.
- `infrastructure` — SQLAlchemy, настройки окружения, хэширование паролей.
- `web_app` — Flask-роуты, формы и шаблоны.
- `ml_api` — FastAPI endpoint'ы и загрузка модели.

## Стек

- Python 3.11+
- Flask, Flask-WTF, Bootstrap
- FastAPI, Uvicorn
- PostgreSQL, SQLAlchemy, Alembic
- scikit-learn, joblib
- Docker Compose
- uv, ruff, mypy, pytest, pre-commit, commitizen

## Переменные окружения

Скопируйте `.env.example` в `.env` и измените значения при необходимости.

```bash
SECRET_KEY=change-me
DATABASE_URL=postgresql+psycopg://sem_user:sem_password@db:5432/sem_db
FASTAPI_URL=http://fastapi:8000
MODEL_PATH=/app/models/iris_model.joblib
LOG_LEVEL=INFO
POSTGRES_DB=sem_db
POSTGRES_USER=sem_user
POSTGRES_PASSWORD=sem_password
```

## Запуск через Docker

```bash
docker compose up --build
```

После запуска:

- Web UI: http://localhost:5000
- ML API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Flask-контейнер автоматически применяет миграции Alembic перед стартом Gunicorn.

## Локальная разработка

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn sem_python.ml_api.main:app --reload
uv run flask --app sem_python.web_app.app:create_app run --debug --port 5000
```

## Проверки

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv run pytest
```

## Основные сценарии

1. Зарегистрировать пользователя.
2. Войти в систему.
3. Открыть страницу `Predict`.
4. Ввести четыре признака цветка Iris.
5. Получить предсказанный класс и вид.
6. Проверить сохранённую запись на странице `History`.

## Git

Для истории коммитов используйте Conventional Commits:

```bash
feat: add flask authentication
fix: handle ml api timeout
chore: update docker compose
```

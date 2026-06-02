FROM python:3.11-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md alembic.ini ./
COPY migrations ./migrations
COPY src ./src

RUN pip install --no-cache-dir uv && uv pip install --system .

EXPOSE 5000

CMD ["sh", "-c", "alembic upgrade head && gunicorn 'sem_python.web_app.app:create_app()' --bind 0.0.0.0:5000 --workers 2"]

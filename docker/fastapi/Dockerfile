FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts

RUN uv pip install --system .

EXPOSE 8000

CMD ["uvicorn", "sem_python.ml_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

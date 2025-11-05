.PHONY: install dev test lint format run-api migrate set-webhook

install:
pip install --upgrade pip
pip install .[dev]

dev:
uvicorn app.api.main:app --host 0.0.0.0 --port 8080

migrate:
alembic upgrade head

set-webhook:
python -m app.bot.loader set-webhook $$WEBHOOK_BASE

run-api:
uvicorn app.api.main:app --host 0.0.0.0 --port 8080

test:
pytest -q

lint:
ruff check .

format:
black .

# FinTrack Telegram Bot

FinTrack is a Telegram bot and FastAPI service that helps users track expenses and income, compute daily spending limits, and manage savings goals "как Тяжеловато". The project ships with Docker support, asynchronous workers, and ready-to-run Alembic migrations.

## Features

- Telegram bot powered by **aiogram 3** with commands for onboarding, budgeting, tracking expenses/income, and savings goals.
- FastAPI backend for webhook processing and lightweight read-only endpoints.
- PostgreSQL persistence with SQLAlchemy 2 models and Alembic migrations.
- APScheduler jobs for daily digests and automatic period rollovers.
- Savings goal engine with percent/fixed reserving and rollover strategies.
- Basic CSV export and server-rendered HTML template for reports preview.
- Docker Compose stack (API, worker, Postgres, Nginx reverse proxy, migrations).

## Getting Started

### Requirements

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Telegram bot token

### Local Development

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   make install
   ```

2. Create `.env` based on `.env.example` and fill in secrets:

   ```bash
   cp .env.example .env
   ```

3. Run database migrations:

   ```bash
   make migrate
   ```

4. Start the API locally:

   ```bash
   make run-api
   ```

5. (Optional) Register the Telegram webhook:

   ```bash
   WEBHOOK_BASE=https://your-domain make set-webhook
   ```

### Docker Deployment

Build and run the full stack (Postgres, migrations, API, worker, Nginx):

```bash
docker compose up -d --build
```

The API will be available on `http://localhost:80` (proxied via Nginx) and directly on `http://localhost:8080` if you expose the `api` service port.

### Running Tests & Quality Tools

```bash
make test
make lint
make format
```

## Project Structure

```
fintrack-tgbot/
  app/
    api/            # FastAPI application and webhook endpoint
    bot/            # aiogram bot loader, handlers, keyboards, middlewares
    repositories/   # Database access layer
    scheduler/      # APScheduler jobs
    services/       # Core business logic (periods, limits, goals, parsing)
    templates/      # Jinja2 templates for mini reports
    config.py       # Settings management
    db.py           # Async SQLAlchemy session helpers
    models.py       # ORM models & enums
    schemas.py      # Pydantic schemas
  alembic/          # Migrations (env + versions)
  docker/           # Nginx config
  tests/            # Pytest unit tests for key business logic
  Dockerfile.api    # API + webhook image
  Dockerfile.worker # Worker image
  docker-compose.yml
  Makefile
  README.md
  pyproject.toml
```

## Key Commands

- `/start` — onboarding flow: currency, pay period, reminders.
- `/budget set <amount>` — configure period budget.
- `/add <amount> <note>` — log expense with smart category detection.
- `/income <amount> <note>` — record extra income (with savings auto-reserve).
- `/today` — daily limit summary with adjustments.
- `/left` — remaining budget till period end.
- `/report [week|month]` — aggregated categories with CSV export button.
- `/goal ...` — manage savings goal (percent/fixed reserve, rollover rules, status).
- `/settings` — adjust timezone, currency, reminders.

> This repository provides a production-ready baseline. Extend handlers, repositories, and templates to fully integrate business rules or connect to external notification channels as needed.

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

### Render Deployment

> Render Blueprints automatically create both the web service and the managed PostgreSQL instance defined in [`render.yaml`](render.yaml).

1. Push your fork of this repository to GitHub.
2. In the [Render dashboard](https://dashboard.render.com/), click **New ➜ Blueprint** and supply the repo URL.
3. Accept the defaults from `render.yaml` or customize the service name/plan. Render will provision:
   - A Docker-based web service that builds the supplied `Dockerfile`. The image now runs `render-entrypoint.sh`, which applies Alembic migrations before starting Uvicorn, so every deploy stays in sync with the database schema.
   - A managed PostgreSQL instance named `fintrack-db` whose connection string is injected into `DATABASE_URL`.
4. Supply required secrets under **Environment ➜ Environment Variables**:
   - `BOT_TOKEN`: Telegram bot token.
   - `WEBHOOK_BASE`: Your Render hostname such as `https://fintrack-tgbot.onrender.com` (used for webhook registration).
   - (Optional) override `TZ`, `DIGEST_HOUR`, `REMINDER_HOUR`, `ALLOWED_ORIGINS`, etc.
5. Deploy the blueprint. Render will build the container, run migrations, and start FastAPI on port `8080` (mapped to `https://<service>.onrender.com`).
6. After the first deploy succeeds, register the Telegram webhook from your local machine:
   ```bash
   export BOT_TOKEN=...  # same token as Render
   python -m app.bot.loader set-webhook "https://fintrack-tgbot.onrender.com"
   ```
   Alternatively, run the same command from a one-off Render shell.

Render will now auto-deploy on every push to the configured branch. Update secrets or schedules directly in the Render dashboard without rebuilding the image.

#### Running FinTrack inside another Render project

If you already have a Docker-based service on Render and you want FinTrack to live inside the same container (so you only pay for that single service), treat this repository as a subdirectory of your existing project and reuse the provided entrypoint:

1. Add the bot as a submodule or subtree, e.g. `git subtree add --prefix services/fintrack https://github.com/<you>/FinTrackBot main`.
2. Make sure your Docker image copies that directory and installs its dependencies:

   ```dockerfile
   COPY services/fintrack /app/services/fintrack
   RUN pip install --no-cache-dir -r /app/services/fintrack/requirements.txt
   ```

3. In your service command (or `CMD`), point the entrypoint at the FinTrack folder and optionally run your original app alongside it:

   ```dockerfile
   ENV FINTRACK_ROOT=/app/services/fintrack \
       EXTRA_PROC_CMD="python -m myproject.api --port 5000"
   CMD ["/app/services/fintrack/render-entrypoint.sh"]
   ```

   `render-entrypoint.sh` now supports `FINTRACK_ROOT` (location of the bot) and `EXTRA_PROC_CMD` (any shell command that should run in parallel, such as your existing FastAPI or worker). Render bills only for the combined container because everything runs inside the same service.

4. Share the same environment variables/secret group with both apps. FinTrack still needs `BOT_TOKEN`, `WEBHOOK_BASE`, `DIGEST_HOUR`, etc., while your original project can keep its existing configuration.

5. Re-deploy the service. The container will launch your `EXTRA_PROC_CMD` in the background, execute FinTrack migrations, and finally expose FinTrack on the configured `WEBAPP_PORT` (keep your other app on a different port or behind a background worker if it does not need HTTP access).

This approach lets both projects run in the same Render plan. If you prefer to keep them in separate services but within a single repository, you can also create multiple entries inside your root `render.yaml` and set `rootDir` to `services/fintrack` for the bot-specific service.

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

#!/bin/bash
set -euo pipefail

alembic upgrade head
exec uvicorn app.main:app --host "${WEBAPP_HOST:-0.0.0.0}" --port "${WEBAPP_PORT:-8080}"

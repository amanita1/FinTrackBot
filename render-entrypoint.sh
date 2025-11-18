#!/bin/bash
set -euo pipefail

APP_DIR="${FINTRACK_ROOT:-/app}"
cd "$APP_DIR"

if [[ -n "${EXTRA_PROC_CMD:-}" ]]; then
  echo "Starting extra process: $EXTRA_PROC_CMD" >&2
  bash -c "$EXTRA_PROC_CMD" &
fi

alembic upgrade head
exec uvicorn app.main:app --host "${WEBAPP_HOST:-0.0.0.0}" --port "${WEBAPP_PORT:-8080}"

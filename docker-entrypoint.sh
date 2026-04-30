#!/bin/sh
set -e

echo "Running database migrations..."
python -m alembic upgrade head

echo "Starting API server..."
exec uvicorn src.api:app --host 0.0.0.0 --port 8000 --workers 1

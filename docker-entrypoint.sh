#!/bin/sh
set -e

echo "Running database migrations..."
python -m alembic upgrade head

echo "Starting API server..."
exec fastapi run --host 0.0.0.0 src/main.py

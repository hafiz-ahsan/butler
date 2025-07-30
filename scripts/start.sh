#!/bin/bash

# Start script for Butler service

set -e

echo "🚀 Starting Butler service..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies with uv..."
    uv sync
fi

# Activate virtual environment
source .venv/bin/activate

# Run database migrations (if any)
# alembic upgrade head

# Start the service
echo "🌟 Butler service is starting..."
exec uvicorn butler.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-8000}" \
    --workers "${WORKERS:-1}" \
    --log-level "${LOG_LEVEL:-info}"
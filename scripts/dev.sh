#!/bin/bash

# Development start script for Butler service

set -e

echo "🔧 Starting Butler service in development mode..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Installing dependencies with uv..."
    uv sync --all-extras --dev
fi

# Activate virtual environment
source .venv/bin/activate

# Install pre-commit hooks
if [ ! -f ".git/hooks/pre-commit" ]; then
    echo "🔗 Installing pre-commit hooks..."
    pre-commit install
fi

# Run database migrations (if any)
# alembic upgrade head

# Start the service with reload
echo "🌟 Butler service is starting in development mode..."
exec uvicorn butler.main:app \
    --host "${HOST:-127.0.0.1}" \
    --port "${PORT:-8000}" \
    --reload \
    --log-level "${LOG_LEVEL:-debug}"
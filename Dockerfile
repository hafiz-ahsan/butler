# Multi-stage Dockerfile for Butler service
FROM python:3.11-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock* ./
COPY src/ ./src/

# Install dependencies and build the project
RUN uv sync --frozen --no-cache

# Production stage
FROM python:3.11-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r butler && useradd -r -g butler butler

# Set working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

# Make sure we use the virtualenv
ENV PATH="/app/.venv/bin:$PATH"

# Copy additional files
COPY scripts/ ./scripts/
RUN chmod +x scripts/*

# Change ownership to butler user
RUN chown -R butler:butler /app

# Switch to non-root user
USER butler

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "butler.main:app", "--host", "0.0.0.0", "--port", "8000"]
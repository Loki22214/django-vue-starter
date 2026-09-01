# Base stage for common dependencies
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/tmp/uv-cache \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    HOME=/home/appuser

WORKDIR /app

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/



FROM base AS development

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base AS production

# Install Python dependencies into /opt/venv
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

# Copy application
COPY . .

# Collect static files
RUN uv run python manage.py collectstatic --noinput

# Create non-root user with a real home directory
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system \
        --uid 1001 \
        --gid 1001 \
        --home /home/appuser \
        --shell /bin/sh \
        appuser && \
    mkdir -p /home/appuser /tmp/uv-cache && \
    chown -R appuser:appgroup \
        /app \
        /opt/venv \
        /home/appuser \
        /tmp/uv-cache && \
    chmod 755 /home/appuser /tmp/uv-cache

# Run as non-root user
USER appuser

EXPOSE 8000

CMD ["uv", "run", "gunicorn", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "4", \
    "--threads", "2", \
    "config.wsgi:application"]
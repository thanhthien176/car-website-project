# =============================================================================
# Stage 1: Builder
# Install Poetry and all dependencies into an isolated virtualenv.
# This stage is discarded after build — only /venv is carried forward.
# =============================================================================

FROM python:3.12-slim AS builder

# Install system dependencies required to compile Python packages
# (psycopg2 needs libpq-dev, Pillow needs libjpeg/zlib)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry — version pinned for reproducibility
RUN pip install --no-cache-dir poetry

WORKDIR /build

# Copy dependency files first — Docker layer cache will skip re-installing
# packages if only source code changed (not pyproject.toml / poetry.lock)
COPY pyproject.toml poetry.lock ./

# Configure Poetry to install into /venv instead of a .venv subfolder
# --only=main excludes dev dependencies (pytest, coverage, etc.)
RUN python -m venv /venv && \
    . /venv/bin/activate && \
    poetry install --only=main --no-root --no-interaction



# =============================================================================
# Stage 2: Final image
# Lean runtime image — no Poetry, no build tools, no cache.
# =============================================================================
FROM python:3.12-slim AS final

# Install only runtime system libraries (not -dev headers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Security: never run app as root
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /home/appuser/app

# Bring in the installed packages from builder stage
COPY --from=builder /venv /venv

# Copy project source code
COPY --chown=appuser:appuser . .

# Make venv binaries available without activating it explicitly
ENV PATH="/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create required directories and give appuser ownership
# Must be done as root before switching user
RUN mkdir -p /home/appuser/app/logs \
             /home/appuser/app/staticfiles \
             /home/appuser/app/media && \
    chown -R appuser:appuser /home/appuser/app

# Switch to non-root user before any further commands
USER appuser

# Collect static files at build time so the image is self-contained.
# Requires DJANGO_SETTINGS_MODULE to point at a settings file that has
# STATIC_ROOT defined but does NOT require a live DB connection.
RUN python manage.py collectstatic --noinput \
    --settings=config.settings.build

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "config.wsgi:application", "--config", "gunicorn.conf.py"]
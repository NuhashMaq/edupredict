# Root Dockerfile for deploying the FastAPI backend to Docker platforms (e.g., Hugging Face Spaces)
# Monorepo note: backend sources live under apps/backend.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Hugging Face Spaces sets PORT; default to 7860 for Docker Spaces.
ENV PORT=7860

WORKDIR /app

# System deps for lightgbm/shap can be non-trivial; keep base minimal and extend as needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy backend project metadata + sources
COPY apps/backend/pyproject.toml apps/backend/README.md /app/apps/backend/
COPY apps/backend/app /app/apps/backend/app

# Install backend
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir /app/apps/backend

EXPOSE 7860

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]

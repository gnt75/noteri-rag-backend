FROM python:3.10-slim

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system deps (optional but useful for some models)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy backend code
COPY backend /app/backend

# Expose port Railway will forward
EXPOSE 8000

# Default envs for Chroma (can be overridden in Railway Variables)
ENV CHROMA_PATH=/app/chroma_db
ENV CHROMA_COLLECTION=noteri_docs
ENV EMBEDDING_MODEL=all-MiniLM-L6-v2

# Start FastAPI with uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

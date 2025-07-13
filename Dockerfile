FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies for psycopg2-binary
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend/app

COPY . /app

RUN pip install --no-cache-dir -r /app/requirements.txt

# Set PYTHONPATH to ensure imports work correctly
ENV PYTHONPATH=/app/backend/app

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4

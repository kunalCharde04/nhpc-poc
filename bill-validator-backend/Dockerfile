FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_HOST=0.0.0.0 \
    APP_PORT=8000 \
    AI_SERVICE_URL=http://ai-service:8001

EXPOSE 8000

CMD ["python", "start.py"]


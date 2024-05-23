FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN poetry install --with lint,test

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "fastapi_user_management.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

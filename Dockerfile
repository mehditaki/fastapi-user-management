FROM python:3.11-slim

# Prevent writing .pyc files to disk and stderr are unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry
RUN poetry install

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "fastapi_user_management.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

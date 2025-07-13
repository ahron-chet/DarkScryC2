FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy dependency files for Management and c2server
RUN mkdir -p /app/Management /app/c2server
COPY Management/pyproject.toml Management/poetry.lock* /app/Management/
COPY c2server/pyproject.toml c2server/poetry.lock* /app/c2server/

WORKDIR /app/Management
RUN poetry install --only main --no-interaction --no-ansi

WORKDIR /app
COPY Management /app/Management
COPY c2server /app/c2server

WORKDIR /app/Management
CMD ["poetry", "run", "arq", "arq_worker.WorkerSettings"]

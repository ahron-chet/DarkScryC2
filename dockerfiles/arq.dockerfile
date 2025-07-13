FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY Management/pyproject.toml Management/poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi --only main

COPY Management /app

CMD ["poetry", "run", "arq", "arq_worker.WorkerSettings"]

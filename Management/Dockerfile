FROM python:3.11.9-slim

RUN apt-get update \
  && apt-get install -y gcc libpq-dev curl netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*



RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
RUN mkdir -p /app/Management /app/c2server

COPY Management/pyproject.toml Management/poetry.lock* /app/Management/
COPY c2server/pyproject.toml c2server/poetry.lock* /app/c2server/

WORKDIR /app/Management
RUN poetry lock --no-interaction --no-ansi

WORKDIR /app
COPY . /app

RUN chmod +x /app/Management/docker-entrypoint.sh \
    && chmod +x /app/Management/start.sh

WORKDIR /app/Management
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

# Corrected entrypoint path
ENTRYPOINT ["/app/Management/docker-entrypoint.sh"]

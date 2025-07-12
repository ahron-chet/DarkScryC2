FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml /app/
RUN poetry install --only main --no-interaction --no-ansi

COPY darkscryc2server /app/darkscryc2server
COPY main.py /app/

EXPOSE 876
EXPOSE 9100

CMD ["python", "main.py"]

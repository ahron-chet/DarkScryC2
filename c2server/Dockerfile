FROM python:3.11.9-slim


RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copy project metadata & install dependencies
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of your code (including test.py)
COPY . /app

# Expose main manager port (if you’d like to be explicit):
EXPOSE 9100
EXPOSE 1234
EXPOSE 876

# CMD ["poetry", "run", "python", "test.py"]
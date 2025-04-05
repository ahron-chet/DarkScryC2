FROM python:3.10-slim

# For Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install OS deps needed for Poetry & building packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy only the pyproject and lockfile first for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies (no-root means do not install this project itself as a package)
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of your code
COPY . /app

# (Optional) Collect static
RUN poetry run python manage.py collectstatic --noinput || true

EXPOSE 8000

# Default command: run Django via uvicorn
CMD ["poetry", "run", "uvicorn", "DarkScryC2Managment.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

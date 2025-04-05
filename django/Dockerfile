# django/Dockerfile

FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Make a working dir
WORKDIR /app

###############################################
# 1) Copy only pyproject + lock for Django & c2server
###############################################
# This replicates the final structure:
#   /app/django/pyproject.toml
#   /app/c2server/pyproject.toml
RUN mkdir -p /app/django /app/c2server

COPY django/pyproject.toml django/poetry.lock* /app/django/
COPY c2server/pyproject.toml c2server/poetry.lock* /app/c2server/

# We have NOT copied the code yet—just the metadata.

###############################################
# 2) Poetry lock only (optional for caching)
###############################################
WORKDIR /app/django
RUN poetry lock --no-interaction --no-ansi

# You can skip this step if you don’t want the partial cache.

###############################################
# 3) Copy the entire repo so that ../c2server exists physically
###############################################
WORKDIR /app
COPY . /app
# Now /app/django and /app/c2server have full code.

###############################################
# 4) Final poetry install
###############################################
WORKDIR /app/django
RUN poetry install --no-root --no-interaction --no-ansi


WORKDIR /app
# Copy the entrypoint script
COPY django/docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

WORKDIR /app/django/DarkScryC2Managment

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
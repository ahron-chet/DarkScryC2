#!/bin/bash
set -e

# Where we store ephemeral DB password for Postgres
PASSWORD_FILE="/run/secrets/db_password"

# If user didn't supply DB_PASSWORD externally, generate ephemeral
if [ -z "$DB_PASSWORD" ]; then
  echo "[django-entrypoint] No DB_PASSWORD. Generating ephemeral..."
  mkdir -p /run/secrets
  openssl rand -base64 32 > "$PASSWORD_FILE"
  export DB_PASSWORD="$(cat "$PASSWORD_FILE")"
else
  echo "[django-entrypoint] Using user-provided DB_PASSWORD=$DB_PASSWORD"
  # Make sure Postgres can also see it if it doesn't exist
  if [ ! -f "$PASSWORD_FILE" ]; then
    mkdir -p /run/secrets
    echo "$DB_PASSWORD" > "$PASSWORD_FILE"
  fi
fi

# Now $DB_PASSWORD is set, and the file /run/secrets/db_password is in place.
echo "[django-entrypoint] Final DB_PASSWORD=$DB_PASSWORD"

# Exec the real command (uvicorn, etc.)
exec "$@"

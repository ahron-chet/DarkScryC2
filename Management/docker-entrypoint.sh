#!/bin/bash
set -e

echo "[management-entrypoint] Starting..."

PASSWORD_FILE="/run/secrets/db_password"

# 1) Ephemeral DB password logic
if [ -z "$DB_PASSWORD" ]; then
  echo "[management-entrypoint] No DB_PASSWORD provided. Generating ephemeral..."
  mkdir -p /run/secrets
  openssl rand -base64 32 > "$PASSWORD_FILE"
  export DB_PASSWORD="$(cat "$PASSWORD_FILE")"
else
  echo "[management-entrypoint] Using user-provided DB_PASSWORD=$DB_PASSWORD"
  if [ ! -f "$PASSWORD_FILE" ]; then
    mkdir -p /run/secrets
    echo "$DB_PASSWORD" > "$PASSWORD_FILE"
  fi
fi

echo "[management-entrypoint] Final DB_PASSWORD=$DB_PASSWORD"

# 2) Migrate
echo "[management-entrypoint] Running migrations..."
poetry run python manage.py migrate --noinput

# 3) Create or update superuser
if [ -z "$SUPER_USER_NAME" ]; then
  export SUPER_USER_NAME=admin
fi
if [ -z "$SUPER_USER_EMAIL" ]; then
  export SUPER_USER_EMAIL=admin@darkscryc2.com
fi
if [ -z "$SUPER_USER_PASSWORD" ]; then
  export SUPER_USER_PASSWORD="$(openssl rand -base64 16)"
fi

echo "[management-entrypoint] Creating/updating superuser..."

poetry run manager create_user --username "$SUPER_USER_NAME" --password "$SUPER_USER_PASSWORD" --email "$SUPER_USER_EMAIL" --role admin

echo "[management-entrypoint] ==========================================="
echo "[management-entrypoint] 👤 Username: ${SUPER_USER_NAME}"
echo "[management-entrypoint] 🔑 Password: ${SUPER_USER_PASSWORD}"
echo "[management-entrypoint] 📧 Email:    ${SUPER_USER_EMAIL}"
echo "[management-entrypoint] ==========================================="

# 4) Exec the main command
exec "$@"

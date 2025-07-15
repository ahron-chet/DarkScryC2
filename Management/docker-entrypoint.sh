#!/usr/bin/env bash

set -e

echo "[management-entrypoint] Starting..."

PASSWORD_FILE="${DB_PASSWORD_FILE:-/run/secrets/db_password}"

# Check if the password file exists and is not empty
if [ -s "$PASSWORD_FILE" ]; then
  echo "[management-entrypoint] Existing DB password found. Using it."
  export DB_PASSWORD="$(cat "$PASSWORD_FILE")"
else
  echo "[management-entrypoint] No existing DB password found. Generating a new one..."
  mkdir -p "$(dirname "$PASSWORD_FILE")"
  openssl rand -base64 32 > "$PASSWORD_FILE"
  export DB_PASSWORD="$(cat "$PASSWORD_FILE")"
fi

echo "[management-entrypoint] Final DB_PASSWORD=${DB_PASSWORD}"


echo "[management-entrypoint] Runing DB migration"
poetry run alembic upgrade head
# 3) Create or update superuser
SUPER_USER_NAME="${SUPER_USER_NAME:-admin}"
SUPER_USER_EMAIL="${SUPER_USER_EMAIL:-admin@darkscryc2.com}"
SUPER_USER_PASSWORD="${SUPER_USER_PASSWORD:-$(openssl rand -base64 16)}"

echo "[management-entrypoint] Creating/updating superuser..."

poetry run manager create_user \
    --username "$SUPER_USER_NAME" \
    --password "$SUPER_USER_PASSWORD" \
    --email "$SUPER_USER_EMAIL" \
    --role admin

echo "[management-entrypoint] ==========================================="
echo "[management-entrypoint] 👤 Username: ${SUPER_USER_NAME}"
echo "[management-entrypoint] 🔑 Password: ${SUPER_USER_PASSWORD}"
echo "[management-entrypoint] 📧 Email:    ${SUPER_USER_EMAIL}"
echo "[management-entrypoint] ==========================================="

# Execute the provided CMD
exec "$@"

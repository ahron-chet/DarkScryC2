#!/bin/bash
set -e

echo "[django-entrypoint] Starting..."

PASSWORD_FILE="/run/secrets/db_password"

# 1) Ephemeral DB password logic
if [ -z "$DB_PASSWORD" ]; then
  echo "[django-entrypoint] No DB_PASSWORD provided. Generating ephemeral..."
  mkdir -p /run/secrets
  openssl rand -base64 32 > "$PASSWORD_FILE"
  export DB_PASSWORD="$(cat "$PASSWORD_FILE")"
else
  echo "[django-entrypoint] Using user-provided DB_PASSWORD=$DB_PASSWORD"
  if [ ! -f "$PASSWORD_FILE" ]; then
    mkdir -p /run/secrets
    echo "$DB_PASSWORD" > "$PASSWORD_FILE"
  fi
fi

echo "[django-entrypoint] Final DB_PASSWORD=$DB_PASSWORD"

# 2) Migrate
echo "[django-entrypoint] Running migrations..."
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

echo "[django-entrypoint] Creating/updating superuser..."

poetry run python manage.py shell <<EOF || true
from django.contrib.auth import get_user_model;
User = get_user_model();

username = "$SUPER_USER_NAME"
email = "$SUPER_USER_EMAIL"
password = "$SUPER_USER_PASSWORD"

try:
    user = User.objects.get(username=username)
    print("User already exists, updating password...")
    user.set_password(password)
    user.email = email
    user.save()
    print(f"Updated existing user: {username}, password={password}")
except User.DoesNotExist:
    print("User does not exist, creating superuser...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created new superuser: {username}, password={password}")
EOF

echo "[django-entrypoint] ==========================================="
echo "[django-entrypoint] 👤 Username: ${SUPER_USER_NAME}"
echo "[django-entrypoint] 🔑 Password: ${SUPER_USER_PASSWORD}"
echo "[django-entrypoint] 📧 Email:    ${SUPER_USER_EMAIL}"
echo "[django-entrypoint] ==========================================="

# 4) Exec the main command
exec "$@"

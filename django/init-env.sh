#!/bin/sh

ENV_FILE="/env/.env"  # We'll mount env_data -> /env inside the setup container

if [ ! -f "$ENV_FILE" ]; then
    echo "Generating new .env with secure random secrets..."

    SECRET_KEY=$(openssl rand -base64 64)
    JWT_SECRET=$(openssl rand -base64 64)
    JWT_REFRESH_SECRET=$(openssl rand -base64 64)
    DB_PASSWORD=$(openssl rand -base64 32)

    cat <<EOL > "$ENV_FILE"
# Django settings
DEBUG=False
SECRET_KEY=$SECRET_KEY

# PostgreSQL settings
DB_NAME=darkscry_db
DB_USER=darkscry_user
DB_PASSWORD=$DB_PASSWORD
DB_HOST=db
DB_PORT=5432

# JWT settings
JWT_SECRET=$JWT_SECRET
JWT_REFRESH_SECRET=$JWT_REFRESH_SECRET

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000
EOL

    echo ".env file generated."
else
    echo ".env file already exists, skipping generation."
fi

# Keep the container alive so other containers can read the file
tail -f /dev/null

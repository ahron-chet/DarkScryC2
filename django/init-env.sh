#!/bin/bash

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Generating new .env file with secure random secrets..."

    SECRET_KEY=$(openssl rand -base64 64)
    JWT_SECRET=$(openssl rand -base64 64)
    JWT_REFRESH_SECRET=$(openssl rand -base64 64)
    DB_PASSWORD=$(openssl rand -base64 32)

    cat <<EOL > $ENV_FILE
# Django Settings
DEBUG=False
SECRET_KEY=$SECRET_KEY

# Database configuration
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

    echo ".env file generated successfully."
else
    echo ".env file already exists."
fi

#!/bin/bash

# Check if .env file already exists
if [ -f .env ]; then
  exit 0
fi

# Generate random password and secret key
POSTGRES_PASSWORD=$(openssl rand -base64 12)
JWT_SECRET_KEY=$(openssl rand -base64 32)

# Create .env file
cat <<EOL > .env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_HOST=localhost
POSTGRES_DB=postgres

API_PORT=8080
FRONTEND_PORT=3000

JWT_SECRET_KEY=$JWT_SECRET_KEY
JWT_ALGORITHM=HS256
JWT_TTL_MINUTES=30
EOL


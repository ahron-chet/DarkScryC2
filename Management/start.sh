#!/bin/sh

# Convert debug value to lowercase for comparison
DEBUG="$(echo "$MANAGEMENT_DEBUG" | tr '[:upper:]' '[:lower:]')"

if [ "$DEBUG" = "true" ]; then
    echo "Starting with reload (debug mode)..."
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level trace
else
    echo "Starting without reload (production mode)..."
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level trace
fi

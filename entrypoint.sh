#!/bin/sh

set -e

if [ "$ENV" = "production" ]; then
    echo "Running database migrations..."
    poetry run alembic upgrade head

    echo "Starting the application in production mode..."
    poetry run fastapi run fast_zero/app.py --host 0.0.0.0
else
    echo "Running database migrations..."
    poetry run alembic upgrade head

    echo "Starting the application in development mode..."
    poetry run fastapi dev fast_zero/app.py --host 0.0.0.0
fi
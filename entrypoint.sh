#!/bin/sh

set -e

if [ "$ENV" = "prod" ]; then
    echo "Running database migrations..."
    poetry run alembic upgrade head

    echo "Starting the application in production mode..."
    poetry run fastapi run fast_zero/app.py --host 0.0.0.0 --port=8000
else
    echo "Running database migrations..."
    poetry run alembic upgrade head

    echo "Starting the application in development mode..."
    poetry run fastapi dev fast_zero/app.py --host 0.0.0.0 --port=8000
fi
#!/bin/sh

# Executes the database migrations
poetry run alembic upgrade head

# Starts the application
poetry run uvicorn --host 0.0.0.0 --port 8000 fast_zero.app:app
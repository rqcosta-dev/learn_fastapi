FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

# Set working directory
WORKDIR /app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
FROM python:3.10-alpine3.17

WORKDIR /app

# Setup timezone with host timezone
ENV TZ=America/Sao_Paulo
RUN apk add --no-cache tzdata

# Install libpq-dev
RUN apk add gcc musl-dev postgresql-dev libpq

COPY poetry.lock pyproject.toml ./

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

# Copy source code
COPY . .

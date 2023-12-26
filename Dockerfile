FROM python:3.11.5-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        make \
        git

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH "${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false


COPY pyproject.toml poetry.lock ./
RUN poetry install  --no-interaction --no-ansi

COPY . /app
ENV DJANGO_SETTINGS_MODULE="src.settings"

EXPOSE 8000
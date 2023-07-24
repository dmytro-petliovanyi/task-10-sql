FROM python:3.10


RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . .

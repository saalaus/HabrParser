FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY . /app

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

EXPOSE 8000

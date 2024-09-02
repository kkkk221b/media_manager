FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev libpq-dev gcc

RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml .
ADD poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . .

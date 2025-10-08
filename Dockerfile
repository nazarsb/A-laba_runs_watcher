FROM python:3.12-alpine

RUN apk add --no-cache dcron python3 py3-pip bash postgresql-client curl
RUN pip install --upgrade pip && \
    pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY pyproject.toml poetry.lock* ./
COPY . .
RUN chmod -R +x scheduled_tasks/cron_scripts/*

COPY ./scheduled_tasks/cron_jobs/* /etc/cron.d/
RUN chmod -R 0644 /etc/cron.d/* && \
    touch /var/log/cron.log

RUN poetry install --no-interaction --no-ansi


CMD ["python", "main.py"]
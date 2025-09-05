FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV IS_DOCKER_CONTAINER 1

RUN apt-get -y update && apt-get -y install curl

WORKDIR /service

COPY pyproject.toml .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY migrations migrations
COPY src src

COPY alembic.ini .

RUN useradd -m appuser
USER appuser

EXPOSE 8080
CMD bash -c "alembic upgrade heads && \
             cd src && \
             uvicorn --factory main:create_app --reload --port 8080 --host 0.0.0.0"

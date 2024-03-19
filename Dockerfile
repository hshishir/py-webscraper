FROM python:3.11-alpine

RUN pip install poetry==1.6.1

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
COPY src src
RUN touch README.md

RUN poetry install

ENTRYPOINT [ "poetry","run","py_webscraper","parseurl"]
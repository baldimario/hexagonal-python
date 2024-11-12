FROM python:3.13-alpine AS base
WORKDIR /app
RUN pip install poetry
COPY app/ .

FROM base AS dev
ENV ENV=dev
RUN apk add black
RUN poetry install
RUN poetry run pyright --version
CMD poetry run python src/main.py

FROM dev AS test
ENV ENV=test
RUN poetry install --witout dev
CMD poetry run coverage run -a -m pytest && poetry run coverage run -a -m behave && poetry run coverage report

FROM base AS prod
ENV ENV=test
RUN poetry install --without test,dev
CMD poetry run python src/main.py

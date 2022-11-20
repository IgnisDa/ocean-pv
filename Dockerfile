
FROM python:3.8-slim

ARG DATABASE_URL \
    SECRET_KEY \
    EMAIL_HOST_PASSWORD \
    EMAIL_HOST_USER \
    GOOGLE_RECAPTCHA_SECRET_KEY \
    GOOGLE_RECAPTCHA_SITE_KEY \
    SECRET_KEY \
    POETRY_VERSION=1.2.2

ENV DATABASE_URL=${DATABASE_URL} \
    EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD} \
    EMAIL_HOST_USER=${EMAIL_HOST_USER} \
    GOOGLE_RECAPTCHA_SECRET_KEY=${GOOGLE_RECAPTCHA_SECRET_KEY} \
    GOOGLE_RECAPTCHA_SITE_KEY=${GOOGLE_RECAPTCHA_SITE_KEY} \
    SECRET_KEY=${SECRET_KEY} \
    APP_ROOT=/server \
    PORT=80

WORKDIR ${APP_ROOT}

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install  --no-root --no-interaction --no-ansi --only main

COPY . ./

EXPOSE 80

ENTRYPOINT [ "/server/entrypoint.bash" ]

FROM python:3.11-alpine

# install build utils and dependencies
RUN apk update && apk upgrade
RUN apk add --no-cache pkgconfig \
    gcc \
    musl-dev \
    libffi-dev \
    && rm -rf /var/cache/apk/*


# Add user app
RUN python -m pip install -U pip
RUN adduser -D app
USER app
WORKDIR /home/app

# set environment varibles
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONHASHSEED random
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

# install poetry
RUN pip install --user poetry
ENV PATH="/home/app/.local/bin:${PATH}"

# install app dependencies
COPY --chown=app:app poetry.lock .
COPY --chown=app:app pyproject.toml .
COPY --chown=app:app poetry.toml .

RUN poetry install --no-dev --no-interaction --no-ansi
# add gunicorn
RUN poetry add gunicorn

COPY --chown=app:app . .

FROM python:3.12

RUN apt update -y && apt install -y --no-install-recommends libpq-dev

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISBALE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERION=2.0.0

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /riscvlab
COPY ./poetry.lock ./pyproject.toml /riscvlab/

RUN poetry install --only=main --no-interaction --no-ansi --no-root
COPY ./riscvlab/. /riscvlab/
CMD ["./poll_builds.py", "--no-debug"]

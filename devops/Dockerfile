
FROM python:3.11-slim-bookworm AS base


FROM base AS builder

ENV PATH=/root/.local/bin:$PATH

RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -LsSf https://astral.sh/uv/0.7.9/install.sh | sh


FROM builder AS appbuilder

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync


FROM builder AS testbuilder

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-groups


FROM base AS app

WORKDIR /app

COPY --from=appbuilder /app/.venv /app/.venv

ENV PATH=/app/.venv/bin:$PATH \
    PYTHONPATH=/app/

COPY newsletter /app/newsletter
COPY alembic.ini /app/

CMD [ "/bin/sh", "-c", "python -m newsletter.main" ]

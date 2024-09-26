# syntax=docker/dockerfile:1.9
ARG python_version=3.12.6

FROM python:$python_version as build

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app

COPY --from=ghcr.io/astral-sh/uv:0.4.16 /uv /bin/uv

COPY pyproject.toml /_lock/
COPY uv.lock /_lock/

RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --frozen \
    --no-dev \
    --no-install-project
EOT

FROM build as test

RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --frozen \
    --no-dev \
    --no-install-project \
    --extra=test
EOT

WORKDIR /test


COPY test_scrape_pokemon.py scrape_pokemon.py ./
COPY test_data ./test_data

CMD ["/app/bin/python", "-m", "pytest"]

FROM python:$python_version as scrape

COPY --from=build /app /app

COPY scrape_pokemon.py ./

CMD ["/app/bin/python", "scrape_pokemon.py"]

FROM python:$python_version as run

COPY --from=build /app /app

COPY grammar.yml run.py pokemon.txt ./

CMD ["/app/bin/python", "run.py"]


ARG python_version=3.10.6
FROM python:$python_version as common

COPY ci-requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip/http pip install -r ci-requirements.txt

WORKDIR /app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip/http pip-sync

FROM common as scrape

COPY scrape_pokemon.py ./

CMD ["python", "scrape_pokemon.py"]

FROM common as run

COPY grammar.yml run.py pokemon.txt ./

CMD ["python", "run.py"]

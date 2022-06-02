ARG python_version=3.10
FROM python:$python_version as common

RUN pip install -U --no-cache-dir pip pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system

FROM common as scrape

RUN pipenv sync -d --system

WORKDIR /app

COPY scrape_pokemon.py ./

CMD ["python", "scrape_pokemon.py"]

FROM common as run

WORKDIR /app

COPY grammar.yml run.py pokemon.txt ./

CMD ["python", "run.py"]

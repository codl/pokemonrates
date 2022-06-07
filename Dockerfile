ARG python_version=3.10
FROM python:$python_version as common

RUN pip install -U --no-cache-dir pip pip-tools

WORKDIR /app

COPY requirements.txt ./
RUN pip-sync

FROM common as scrape

COPY scrape_pokemon.py ./

CMD ["python", "scrape_pokemon.py"]

FROM common as run

COPY grammar.yml run.py pokemon.txt ./

CMD ["python", "run.py"]

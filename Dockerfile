FROM python:3 as scrape

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY scrape_pokemon.py ./

CMD ["python", "scrape_pokemon.py", "-"]

FROM python:3 as run

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY grammar.yml run.py pokemon.txt ./

CMD ["python", "run.py"]

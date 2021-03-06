ARG python_version=3
FROM python:$python_version as scrape

WORKDIR /app

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY scrape_pokemon.py ./
RUN python -m py_compile scrape_pokemon.py

CMD ["python", "scrape_pokemon.py"]

FROM python:$python_version as run

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY grammar.yml run.py pokemon.txt ./
RUN python -m py_compile run.py

CMD ["python", "run.py"]

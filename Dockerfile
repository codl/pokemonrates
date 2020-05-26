from python:3

workdir /app

copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy grammar.yml run.py pokemon.txt ./

#ARG INSTANCE
#ARG CLIENT_KEY
#ARG CLIENT_SECRET
#ARG ACCESS_TOKEN
#COPY bot.yml.dockertemplate /app/
#RUN envsubst < bot.yml.dockertemplate > bot.yml && rm bot.yml.dockertemplate

CMD ["python", "run.py"]

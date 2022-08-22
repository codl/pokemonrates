# pokemon rates

is a mastodon bot that rates pokémon. it can be found at [pokemonrates@botsin.space](https://botsin.space/@pokemonrates)

## running

these instructions are probably not for you

### natively

make sure python 3.6ish or higher is installed, and that you're in [a venv](https://docs.python.org/3.10/library/venv.html)

```
# install dependencies
pip install -r requirements.txt

# configure
cp bot.example.yml bot.yml
$EDITOR bot.yml

# run
python run.py
```

### docker

```
# build docker image
docker buildx build -t pokemonrates .

# configure
cp bot.example.yml bot.yml
$EDITOR bot.yml

# run
docker run -d -v /absolute/path/to/bot.yml:/app/bot.yml pokemonrates
```

`--restart unless-stopped` may be a wise addition to that `docker run` command

## scraping pokemon names

this scrapes names of pokémon from bulbapedia. it's bad but i don't have anything better

### natively

```
python scrape_pokemon.py > pokemon.txt
```

### docker

```
docker buildx build -t pokemonrates:scrape --target scrape .
docker run --rm pokemonrates:scrape > pokemon.txt
```

note that you'll need to rebuild the bot's main docker image to include the new list of pokémon

#!/bin/bash

cd $(dirname $0)
docker buildx build -t pokemonrates . \
&& docker buildx build -t pokemonrates:scrape --target scrape .

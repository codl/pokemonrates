#!/bin/bash

cd $(dirname $0)
docker build -t pokemonrates . \
&& docker build -t pokemonrates:scrape --target scrape .

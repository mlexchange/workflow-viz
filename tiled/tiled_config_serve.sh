#!/bin/sh
source .env
export PYTHONPATH="$PYTHONPATH:$PWD/tiled/config/"
tiled serve config ./tiled/config/config.yml
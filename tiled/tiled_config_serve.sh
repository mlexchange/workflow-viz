#!/bin/sh
source .env
export PYTHONPATH="$PYTHONPATH:$PWD/tiled/config/"
export TILED_SINGLE_USER_API_KEY=$TILED_API_KEY
tiled serve config ./tiled/config/config.yml
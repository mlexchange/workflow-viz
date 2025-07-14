#!/bin/bash
# Export environment variables to this shell
set -o allexport
source .env
set +o allexport

# Replace environment variables in config.yml
# envsubst < ./tiled/config/config.yml > ./tiled/config/config_tmp.yml
UVICORN_HOST=0.0.0.0 tiled serve config /app/tiled/config/config.yml
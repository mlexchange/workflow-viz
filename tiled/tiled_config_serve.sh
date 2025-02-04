#!/bin/bash
# Export environment variables to this shell
set -o allexport
source .env
set +o allexport
export TILED_SINGLE_USER_API_KEY=$TILED_API_KEY

# Replace environment variables in config.yml
# envsubst < ./tiled/config/config.yml > ./tiled/config/config_tmp.yml
tiled serve config /app/tiled/config/config.yml
# equivalent to "source .env"
./set_env.ps1
$Env:TILED_SINGLE_USER_API_KEY=$Env:TILED_API_KEY

tiled serve config ./tiled/config/config.yml
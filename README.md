# Workflow Setup Visualization Prototype

## Initial setup: Clone the repository, create an environment, activate the environment, with venv:

Clone the repository:

```bash
git clone git@github.com:als-computing/workflow-viz.git
cd workflow-viz
```

Setup an environment, with venv:

```bash
python3 -m venv workflow-viz-env
source workflow-viz-env/bin/activate
```

or Anaconda:

```bash
conda create --name workflow-viz-env
conda activate workflow-viz-env
```

and install the requirements:

```bash
pip install -r requirements.txt
```

## Initial + beamtime setup: Set correct paths

In a file `.env`, set the following variables and adapt the path 

```bash
TILED_URI="http://127.0.0.1:8888"
TILED_API_KEY="<randomly generated key>"
TILED_WHITELIST="<comma seperated list of file or directory names to process>"
TILED_BLACKLIST="<comma seperated list of file or directory names to ignore>"
PREFECT_API_URL="http://127.0.0.1:4200/api"
PATH_TO_DATA_ALS="<path to folder>"
PATH_TO_DATA_DESY="<path to folder that has structure as beamtime (with subfolders /raw, /processed/ ...)>"
PATH_TO_DATA_CATALOG="./tiled/db/catalog.db"
```

Either `PATH_TO_DATA_ALS` or `PATH_TO_DATA_DESY` can be omitted, but must match with the `PATH_TO_DATA` path in the `SAXSWAXS-workflows` environment.

Additionally, the `TILED_API_KEY` needs to be the same.

If `TILED_WHITELIST` is empty, no files/directories will be skipped, but if it is not one needs to specify all names to be whitelisted (including top-level directory names, e.g. `"raw, processed, <beamtimeid>"`).

If `TILED_WHITELIST` is empty, no files/directories will be skipped, but if it is not one needs to specify all names to be whitelisted (including top-level directory names, e.g. `"raw, processed, <beamtimeid>"`).

## Beamtime setup: Start up a Tiled

Within two seperate processed, start the Tiled server

```bash
tiled/tiled_config_serve.sh
```

and register the already existing files to Tiled

```bash
tiled/tiled_catalog_register.sh
```

## Beamtime setup: Start up the Dash application

```bash
python app.py
```

# Alternative: Initial setup with Docker: 

```bash
docker network create workflow_viz_default
```


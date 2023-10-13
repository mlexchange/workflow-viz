# Workflow Setup Visualization Prototype

# Initial setup: Clone the repository, create an environment, activate the environment

```bash
git clone git@github.com:als-computing/workflow-viz.git
cd workflow-viz
python3 -m venv workflow-viz-env
source workflow-viz-env/bin/activate
pip install -r requirements.txt
```

# Set correct paths

In a file `.env`, set the following variables and adapt the path 

```bash
TILED_URI="http://127.0.0.1:8888"
TILED_API_KEY="<randomly generated key>"
PREFECT_API_URL="http://127.0.0.1:4200/api"
PATH_TO_DATA_ALS="<path to folder that>"
PATH_TO_DATA_DESY="<path to folder that has structure as beamtime (with subfolders /raw, /processed/ ...)>"
PATH_TO_DATA_CATALOG="./tiled/db/catalog.db"
```

Either `PATH_TO_DATA_ALS` or `PATH_TO_DATA_DESY` can be omitted, but must match with the `PATH_TO_DATA` path in the `SAXSWAXS-workflows` environment.

Additionally, the `TILED_API_KEY` needs to be the same.

# Start up a Tiled server

```bash
tiled/tiled_catalog_register.sh
tiled/tiled_config_serve.sh
```
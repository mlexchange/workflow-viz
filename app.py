import os

import dash_mantine_components as dmc
from dash import Dash, dcc, html

from utils.redis import RedisConn

try:
    import utils.data_retrieval
except Exception as e:
    import sys

    print(
        "Error importing utils.data_retrieval. "
        "This is often caused by not being able to connect to the Tiled server. "
        f"Error: {e}"
    )
    sys.exit(1)

from callbacks.config_loader import *
from callbacks.controls_calibration import *
from callbacks.controls_reduction import *
from callbacks.progress import *
from callbacks.reduction import *
from callbacks.scan import *
from callbacks.tiled_viewer import *  # Add this line
from components.config_loader import layout as config_layout
from components.controls_calibration import layout as controls_calibration_layout
from components.controls_reduction import layout as controls_reduction_layout
from components.progress import layout as progress_layout
from components.reduction import layout as reduction_layout
from components.scan import layout as scan_layout

# Configurable host and port to suport containerization,
# which needs to attach to 0.0.0.0
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = os.getenv("FLASK_PORT", 8095)

# Configure dash to listen to a specific pathname prefix,
# great for being served behind a reverse proxy
PATHNAME_PREFIX = os.getenv("REQUEST_PATHNAME_PREFIX", "/")

redis_conn = None
# Initialize the Dash app
app = Dash(
    __name__,
    requests_pathname_prefix=PATHNAME_PREFIX,
    routes_pathname_prefix=PATHNAME_PREFIX,
)
app.title = "Workflow Configuration"
application = app.server


redis_conn = RedisConn.from_env()


app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        dmc.Center(progress_layout()),
        dcc.Store(id="prefect-flow-run", data={"id": None, "result_uri": None}),
        dcc.Interval(id="prefect-flow-check", interval=1000),
        dmc.Grid(
            # grow=True,
            children=[
                dmc.Col(
                    html.Div(
                        children=[
                            scan_layout(),
                            controls_calibration_layout(),
                            controls_reduction_layout(),
                            config_layout(),
                        ]
                    ),
                    span=6,
                ),
                dmc.Col(html.Div(children=[reduction_layout()]), span=6),
            ],
        ),
    ],
)


if __name__ == "__main__":
    print(
        (
            f"Starting Dash app on {FLASK_HOST}:{FLASK_PORT} "
            f"with pathname prefix '{PATHNAME_PREFIX}'"
        )
    )
    app.run(
        debug=True,
        host=FLASK_HOST,
        port=FLASK_PORT,
    )

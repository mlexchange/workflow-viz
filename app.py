import os

import dash_mantine_components as dmc
from dash import Dash, dcc, html
from redis import Redis

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
from components.config_loader import layout as config_layout
from components.controls_calibration import layout as controls_calibration_layout
from components.controls_reduction import layout as controls_reduction_layout
from components.progress import layout as progress_layout
from components.reduction import layout as reduction_layout
from components.scan import layout as scan_layout
from utils.redis import RedisWorkflow

redis_conn = None
try:
    host = os.getenv("FLASK_HOST", "127.0.0.01")
    port = os.getenv("FLASK_PORT", 8095)
    redis_conn = Redis("localhost", 44444)
except Exception as e:
    print(f"redis unavaialble {e}")

FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = os.getenv("FLASK_PORT", "8095")

# Initialize the Dash app
app = Dash(__name__)
app.title = "Workflow Configuration"
application = app.server


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
    app.run(
        requests_pathname_prefix="/workflow-viz/",
        routes_pathname_prefix="/workflow-viz/",
        debug=True,
        host=FLASK_HOST,
        port=FLASK_PORT,
    )

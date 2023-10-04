import os

import dash_mantine_components as dmc
from dash import Dash, html
from tiled.client import from_uri
from tiled.client.cache import Cache

from callbacks.controls_calibration import *
from callbacks.controls_reduction import *
from callbacks.progress import *
from callbacks.reduction import *
from callbacks.scan import *
from components.controls_calibration import layout as controls_calibration_layout
from components.controls_reduction import layout as controls_reduction_layout
from components.progress import layout as progress_layout
from components.reduction import layout as reduction_layout
from components.scan import layout as scan_layout

# Initialize the Dash app
app = Dash(__name__)
app.title = "Workflow Configuration"
application = app.server


app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        dmc.Center(progress_layout()),
        dmc.Grid(
            # grow=True,
            children=[
                dmc.Col(
                    html.Div(
                        children=[
                            scan_layout(),
                            controls_calibration_layout(),
                            controls_reduction_layout(),
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
    app.run_server(debug=True)

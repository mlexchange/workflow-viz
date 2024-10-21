import os

import dash_mantine_components as dmc
import numpy as np
from dash import Dash, html
from dash_extensions import WebSocket
from tiled.client import from_uri

from callbacks.streamed_reduction import *

# from components.scan_summary import layout

# Initialize the Dash app
app = Dash(
    __name__,
    requests_pathname_prefix="/reduction_viewer/",
)
app.title = "Live View"
application = app.server

# Initialize the Tiled server
TILED_URI = os.getenv("TILED_URI")
TILED_API_KEY = os.getenv("TILED_API_KEY")

# TILED_EXPERIMENT_URI = "http://127.0.0.1:8888/api/v1/metadata/processed/NaCl_1_10_2"
TILED_EXPERIMENT_URI = (
    "http://127.0.0.1:8888/api/v1/metadata/processed/Autonomous/NaCl_1_10_C"
)


def extract_full_scan(experiment_uri):
    client = from_uri(experiment_uri, api_key=TILED_API_KEY)
    num_keys = len(client.keys())
    x_data = np.zeros(num_keys)
    y_data = np.zeros(num_keys)
    feature_data = np.zeros(num_keys)
    reduction_uris = [None] * num_keys
    feature_name = "max_intensity"
    # feature_name = "max_intensity"
    # feature_name = "area_under_curve"
    counter = 0
    for scan_key in client.keys():
        scan_client = client[scan_key]
        if counter >= num_keys:
            break
        for reduction_key in scan_client:
            if "integration-azimuthal" in reduction_key:
                reduction_client = scan_client[reduction_key]
                reduction_metadata = reduction_client.metadata
                reduction_uris[counter] = reduction_client.uri
                # Get feature from the meta data
                feature = reduction_metadata[feature_name]
                feature_data[counter] = feature
                # Get motor positions from the input_uri
                input_metadata = from_uri(reduction_metadata["input_uri"]).metadata
                x = input_metadata["Sample X Stage"]
                y = input_metadata["Sample Y Stage"]
                x_data[counter] = x
                y_data[counter] = y
                counter = counter + 1


app.layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        dmc.Grid(
            # grow=True,
            children=[
                dmc.Col(
                    html.Div(
                        children=[
                            dmc.Text(id="reduction_update_message"),
                            WebSocket(
                                id="ws-reduction-update",
                                url="ws://127.0.0.1:5001/ws/reduction_update",
                            ),
                        ]
                    ),
                    span=6,
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port="8075")

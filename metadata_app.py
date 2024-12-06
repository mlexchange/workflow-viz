import dash
from dash import html

from callbacks.metadata_interface import *  # noqa: F401, F403
from components.metadata_interface import (
    interface_components,
    table_modification_components,
)

"""
Please run matadata_utils.ipynb in the utils folder before running this app
It creates a new Tiled node for a new experiment and a csv file on the filesystem
"""

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        # dmc.Grid(
        #     [
        #         interface_components(),
        #         table_modification_components(),
        #     ]
        # ),
        interface_components(),
        table_modification_components(),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

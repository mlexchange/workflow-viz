import plotly.express as px
from dash import dcc, html

from utils.create_shapes import create_rect
from utils.generate_random import generate_random

COMPONENT_STYLE = {
    #   "width": "800px",
    #   "height": "calc(60vh - 40px)",
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
}


def layout():
    scan_width = 2000
    scan_height = 1000
    data = generate_random(width=scan_width, height=scan_height)

    figure = px.imshow(
        data, origin="lower", aspect="equal", color_continuous_scale="viridis"
    )

    center = (scan_width / 2, scan_height / 2)
    figure.add_shape(
        create_rect(
            center[0],
            center[1],
            rect_width=10,
            rect_height=scan_height,
            scan_width=scan_width,
            scan_height=scan_height,
        )
    )

    figure.update_layout(title="Scan")

    return html.Div(
        style=COMPONENT_STYLE,
        children=[
            dcc.Graph(id="scan", figure=figure),
            dcc.Store(id="scan_width", data=scan_width),
            dcc.Store(id="scan_height", data=scan_height),
        ],
    )

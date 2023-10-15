import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import dcc, html

from utils.create_shapes import create_cross

COMPONENT_STYLE = {
    #   "width": "800px",
    #   "height": "calc(60vh - 40px)",
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
}


def layout():
    scan_width = 1679
    scan_height = 1475
    # data = generate_zeros(width=scan_width, height=scan_height)

    figure = go.Figure(go.Scatter(x=[], y=[]))
    figure.update_layout(template=None)
    figure.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    figure.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    figure.update_layout(title="Scan")

    horizontal_line, vertical_line = create_cross(
        scan_width / 2, scan_height / 2, 20, 20, scan_width, scan_height
    )

    figure.add_shape(horizontal_line)
    figure.add_shape(vertical_line)

    return html.Div(
        id="scan-container",
        style=COMPONENT_STYLE,
        children=[
            dmc.LoadingOverlay(
                id="scan-viewer-loading",
                overlayOpacity=0,
                loaderProps=dict(
                    color=dmc.theme.DEFAULT_COLORS["blue"][6], variant="bars"
                ),
                children=[
                    dcc.Graph(id="scan-viewer", figure=figure),
                ],
            ),
            dcc.Store(
                id="scan-dims", data={"width": scan_width, "height": scan_height}
            ),
        ],
    )

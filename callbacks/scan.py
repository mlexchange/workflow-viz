# import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, Patch, State, callback
from dash.exceptions import PreventUpdate

from components.scan import SCAN_FIGURE_LAYOUT
from utils.create_shapes import create_cross
from utils.data_retrieval import get_mask_data, get_scan_data


@callback(
    Output("scan-viewer", "figure", allow_duplicate=True),
    Output("scan-dims", "data"),
    Input("scan-name", "value"),
    Input("mask-name", "value"),
    State("scan-name-uri-map", "data"),
    State("mask-name-uri-map", "data"),
    prevent_initial_call=True,
)
def upate_scan(scan_name, mask_name, scan_name_uri_map, mask_name_uri_map):
    if scan_name:
        scan_uri = scan_name_uri_map[scan_name]
        scan_data = get_scan_data(scan_uri)
        scan_width = scan_data.shape[1]
        scan_height = scan_data.shape[0]
        scan = go.Heatmap(z=scan_data, colorscale="viridis", zmax=100, zauto=False)
        figure = go.Figure(data=scan, layout=SCAN_FIGURE_LAYOUT)
    else:
        scan_width = 1679
        scan_height = 1475
        # data = generate_zeros(width=scan_width, height=scan_height)
        figure = go.Figure(go.Scatter(x=[], y=[]))
    if mask_name:
        mask_uri = mask_name_uri_map[mask_name]
        mask_data = get_mask_data(
            mask_uri, scan_height=scan_height, scan_width=scan_width
        )
        if mask_data is not None:
            figure.add_trace(
                go.Heatmap(z=mask_data, colorscale="Greys", showscale=False)
            )
            figure["data"][1]["opacity"] = 1 / 10

    return figure, {"width": scan_width, "height": scan_height}


@callback(
    Output("scan-viewer", "figure", allow_duplicate=True),
    Output("beamcenter-x", "value"),
    Output("beamcenter-y", "value"),
    Input("scan-viewer", "clickData"),
    State("scan-dims", "data"),
    State("progress-stepper", "active"),
    prevent_initial_call=True,
)
def handle_click(
    click_data,
    current_step,
    scan_dims,
):
    if current_step != 1:
        raise PreventUpdate
    scan_width = scan_dims["width"]
    scan_height = scan_dims["height"]
    if click_data is not None:
        x_value = click_data["points"][0]["x"]
        y_value = click_data["points"][0]["y"]
    else:
        x_value = scan_width / 2
        y_value = scan_height / 2
    patched_figure = Patch()

    horizontal_line, vertical_line = create_cross(
        x_value, y_value, 200, 200, scan_width, scan_height
    )
    patched_figure["layout"]["shapes"][0].update(horizontal_line)
    patched_figure["layout"]["shapes"][0].update(vertical_line)

    return patched_figure, x_value, y_value

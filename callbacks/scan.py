# import plotly.express as px
import numpy as np
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
        zmin = np.percentile(scan_data, 1)
        zmax = np.percentile(scan_data, 99)
        scan = go.Heatmap(
            z=scan_data, colorscale="viridis", zmin=zmin, zmax=zmax, zauto=False
        )
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
        ).astype(np.uint8)
        if mask_data is not None:
            # Masks exported from Igor have zeros for areas to be masked out
            # Masks exported from pyFAI have non-zero values for these areas
            # Fully transparent for non-masked values, fully opaque for masked
            mask_colorscale = [
                [0, "rgba(0, 0, 0, 1)"],
                [1, "rgba(0, 0, 0, 0)"],
            ]
            figure.add_trace(
                go.Heatmap(z=mask_data, colorscale=mask_colorscale, showscale=False)
            )
            # figure["data"][1]["opacity"] = 1 / 2
    figure["layout"]["yaxis"]["autorange"] = "reversed"
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

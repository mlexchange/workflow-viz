# import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, Patch, State, callback, ctx, no_update
from dash.exceptions import PreventUpdate

from components.scan import SCAN_FIGURE_LAYOUT
from utils.create_shapes import create_cross, create_rect_center_line
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
        scan_height = 1679
        scan_width = 1475
        # data = generate_zeros(width=scan_width, height=scan_height)
        figure = go.Figure(go.Scatter(x=[], y=[]))
    if mask_name:
        mask_uri = mask_name_uri_map[mask_name]
        mask_data = get_mask_data(
            mask_uri, scan_height=scan_height, scan_width=scan_width
        )
        if mask_data is not None:
            # Masks exported from Igor have zeros for areas to be masked out
            # Masks exported from pyFAI have non-zero values for these areas
            # We assume the pyFAI convention with non-zero values being masked
            # Fully transparent for non-masked values, fully opaque for masked
            mask_colorscale = [
                [0, "rgba(0, 0, 0, 0)"],
                [1, "rgba(0, 0, 0, 1)"],
            ]
            figure.add_trace(
                go.Heatmap(
                    z=mask_data.astype(np.uint8),
                    colorscale=mask_colorscale,
                    showscale=False,
                )
            )
            figure["data"][1]["opacity"] = 1 / 2
    figure["layout"]["yaxis"]["autorange"] = "reversed"
    return figure, {"width": scan_width, "height": scan_height}


@callback(
    Output("scan-viewer", "figure", allow_duplicate=True),
    Output("beamcenter-x", "value"),
    Output("beamcenter-y", "value"),
    Input("scan-viewer", "clickData"),
    Input("beamcenter-x", "value"),
    Input("beamcenter-y", "value"),
    State("progress-stepper", "active"),
    State("scan-dims", "data"),
    prevent_initial_call=True,
)
def update_beamcenter_indicator(
    click_data,
    beamcenter_x,
    beamcenter_y,
    current_step,
    scan_dims,
):
    if current_step != 0:
        raise PreventUpdate

    scan_width = scan_dims["width"]
    scan_height = scan_dims["height"]

    trigger = ctx.triggered_id
    if click_data is not None and trigger == "scan-viewer":
        x_value = click_data["points"][0]["x"]
        y_value = click_data["points"][0]["y"]
    else:
        x_value = beamcenter_x
        y_value = beamcenter_y

    patched_figure = Patch()

    horizontal_line, vertical_line = create_cross(
        x_value, y_value, 50, 50, scan_width, scan_height
    )

    # A placeholder cross for the beamcenter was added on initialization
    # We can simply update these two lines here
    patched_figure["layout"]["shapes"][0].update(horizontal_line)
    patched_figure["layout"]["shapes"][1].update(vertical_line)

    # Prevent unneccessary update to beamcenter number inputs
    if x_value == beamcenter_x and y_value == beamcenter_y:
        return patched_figure, no_update, no_update

    return patched_figure, x_value, y_value


@callback(
    Output("scan-viewer", "figure", allow_duplicate=True),
    Output("horizontal-cut-pos-y", "value", allow_duplicate=True),
    Output("horizontal-x-min", "value", allow_duplicate=True),
    Output("horizontal-x-max", "value", allow_duplicate=True),
    Input("scan-viewer", "clickData"),
    State("scan-viewer", "figure"),
    State("experiment-type", "value"),
    Input("horizontal-cut-pos-y", "value"),
    Input("horizontal-cut-half-width", "value"),
    Input("horizontal-x-min", "value"),
    Input("horizontal-x-max", "value"),
    Input("progress-stepper", "active"),
    State("scan-dims", "data"),
    prevent_initial_call=True,
)
def update_horizontal_cut_indicator(
    click_data,
    fig,
    experiment_type,
    horizontal_cut_pos_y,
    horizontal_cut_half_width,
    horizontal_cut_x_min,
    horizontal_cut_x_max,
    current_step,
    scan_dims,
):
    if current_step != 1 or (
        experiment_type is not None and not experiment_type.startswith("GI")
    ):
        raise PreventUpdate

    scan_width = scan_dims["width"]
    scan_height = scan_dims["height"]

    trigger = ctx.triggered_id
    if click_data is not None and trigger == "scan-viewer":
        x_value = click_data["points"][0]["x"]
        y_value = click_data["points"][0]["y"]
        # Assume that the user wants the width of the cut to stay the
        old_width = horizontal_cut_x_max - horizontal_cut_x_min + 1
        x_min = max(0, int(x_value - old_width / 2))
        x_max = min(scan_width - 1, int(x_value + old_width / 2))
    else:
        x_value = (horizontal_cut_x_min + horizontal_cut_x_max) / 2
        y_value = horizontal_cut_pos_y
        x_min = horizontal_cut_x_min
        x_max = horizontal_cut_x_max

    rect, center_line = create_rect_center_line(
        center_x=x_value,
        center_y=y_value,
        rect_width=horizontal_cut_x_max - horizontal_cut_x_min + 1,
        rect_height=horizontal_cut_half_width * 2 + 1,
        scan_width=scan_width,
        scan_height=scan_height,
    )

    patched_figure = Patch()

    current_shapes = fig.get("layout", {}).get("shapes", [])

    if len(current_shapes) < 4:
        patched_figure["layout"]["shapes"].append(rect)
        patched_figure["layout"]["shapes"].append(center_line)
    else:
        patched_figure["layout"]["shapes"][2] = rect
        patched_figure["layout"]["shapes"][3] = center_line

    y_update = y_value if y_value != horizontal_cut_pos_y else no_update
    x_min_update = x_min if x_min != horizontal_cut_x_min else no_update
    x_max_update = x_max if x_max != horizontal_cut_x_max else no_update

    return patched_figure, y_update, x_min_update, x_max_update

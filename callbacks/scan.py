import plotly.express as px
import plotly.graph_objects as go

# import plotly.graph_objects as go
from dash import Input, Output, callback  # Patch
from dash.exceptions import PreventUpdate

# from utils.create_shapes import create_rect
from utils.data_retrieval import get_mask_data, get_scan_data
from utils.generate_random import generate_zeros


@callback(
    Output("scan-viewer", "figure"),
    Output("scan-dims", "data"),
    Input("scan-uri", "value"),
    Input("mask-uri", "value"),
)
def render_scan(scan_uri, mask_uri):
    if scan_uri:
        data = get_scan_data(scan_uri)
        scan_width = data.shape[1]
        scan_height = data.shape[0]
    else:
        scan_width = 1679
        scan_height = 1475
        data = generate_zeros(width=scan_width, height=scan_height)
    figure = px.imshow(
        data,
        origin="lower",
        aspect="equal",
        color_continuous_scale="viridis",
        zmax=100,
    )
    if mask_uri:
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
    Input("scan-viewer", "clickData"),
    Input("scan-dims", "data"),
    Input("progress-stepper", "active"),
    prevent_initial_call=True,
)
def update_cut(click_data, scan_dims, current_step):
    if current_step != 1:
        raise PreventUpdate
    # scan_width = scan_dims["width"]
    # scan_height = scan_dims["height"]
    # if click_data is not None:
    #    x_value = click_data["points"][0]["x"]
    #    y_value = click_data["points"][0]["y"]
    # else:
    #    x_value = scan_width / 2
    #    y_value = scan_height / 2
    # patched_figure = Patch()
    # patched_figure["layout"]["shapes"][0].update(
    #    create_rect(
    #        center_x=x_value,
    #        center_y=y_value,
    #        rect_width=cut_width,
    #        rect_height=cut_height,
    #        scan_width=scan_width,
    #        scan_height=scan_height,
    #    )
    # )
    # return patched_figure

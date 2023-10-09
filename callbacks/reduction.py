# import numpy as np
from dash import Input, Output, Patch, State, callback


@callback(
    Output("reduction-viewer", "figure"),
    State("scan-viewer", "figure"),
    Input("cut-width", "value"),
    Input("cut-height", "value"),
    Input("scan-viewer", "clickData"),
    Input("cut-direction", "checked"),
    Input("scan-dims", "data"),
)
def update_cut(
    scan_figure, cut_width, cut_height, click_data, cut_horizontal, scan_dims
):
    # scan_width = scan_dims["width"]
    # scan_height = scan_dims["height"]
    # if click_data is not None:
    #    x_clicked = click_data["points"][0]["x"]
    #    y_clicked = click_data["points"][0]["y"]
    # else:
    #    x_clicked = scan_width / 2
    #    y_clicked = scan_height / 2
    # x0 = max(0, int(x_clicked - cut_width / 2))
    # y0 = max(0, int(y_clicked - cut_height / 2))
    # x1 = min(scan_width - 1, int(x_clicked + cut_width / 2))
    # y1 = min(scan_height - 1, int(y_clicked + cut_height / 2))

    # Update x and y for the line plot
    patched_figure = Patch()

    return patched_figure


# @callback(
#    Output("output-details", "children", allow_duplicate=True),
#    Output("submitted-job-id", "data", allow_duplicate=True),
#    Input("submitted-job-id", "data"),
#    Input("model-check", "n_intervals"),
#    prevent_initial_call=True,
# )
# def check_flow(job_id, n_intervals):
#    pass


@callback(
    Output("reduction-container", "style"),
    Input("progress-stepper", "active"),
)
def toggle_controls_reduction_visibility(current_step):
    step = current_step if current_step is not None else 0
    if step == 1:
        return {"display": "block"}
    else:
        return {"display": "none"}

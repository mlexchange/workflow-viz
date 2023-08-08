import numpy as np
from dash import Input, Output, Patch, State, callback


@callback(
    Output("reduction", "figure"),
    State("scan", "figure"),
    Input("cut-width", "value"),
    Input("cut-height", "value"),
    Input("scan", "clickData"),
    Input("cut-direction", "checked"),
    Input("scan_height", "data"),
    Input("scan_width", "data"),
)
def update_cut(
    scan_figure,
    cut_width,
    cut_height,
    click_data,
    cut_horizontal,
    scan_height,
    scan_width,
):
    if click_data is not None:
        x_clicked = click_data["points"][0]["x"]
        y_clicked = click_data["points"][0]["y"]
    else:
        x_clicked = scan_width / 2
        y_clicked = scan_height / 2
    x0 = max(0, int(x_clicked - cut_width / 2))
    y0 = max(0, int(y_clicked - cut_height / 2))
    x1 = min(scan_width - 1, int(x_clicked + cut_width / 2))
    y1 = min(scan_height - 1, int(y_clicked + cut_height / 2))

    cut_data = np.array(scan_figure["data"][0]["z"])[y0:y1, x0:x1]
    # Update x and y for the line plot
    patched_figure = Patch()

    # Take mean across either horizontal or vertical direction
    if cut_horizontal:
        x_data_cut = np.arange(x0, x1, 1, dtype=int)
        y_data_cut = np.mean(cut_data, axis=0)
    else:
        x_data_cut = np.arange(y0, y1, 1, dtype=int)
        y_data_cut = np.mean(cut_data, axis=1)
    patched_figure["data"][0]["x"] = x_data_cut
    patched_figure["data"][0]["y"] = y_data_cut
    return patched_figure

from dash import Input, Output, Patch, callback

from utils.create_shapes import create_rect


@callback(
    Output("scan", "figure"),
    Input("cut-width", "value"),
    Input("cut-height", "value"),
    Input("scan", "clickData"),
    Input("scan_width", "data"),
    Input("scan_height", "data"),
)
def update_cut(cut_width, cut_height, click_data, scan_width, scan_height):
    if click_data is not None:
        x_value = click_data["points"][0]["x"]
        y_value = click_data["points"][0]["y"]
    else:
        x_value = scan_width / 2
        y_value = scan_height / 2
    patched_figure = Patch()
    patched_figure["layout"]["shapes"][0].update(
        create_rect(
            center_x=x_value,
            center_y=y_value,
            rect_width=cut_width,
            rect_height=cut_height,
            scan_width=scan_width,
            scan_height=scan_height,
        )
    )
    return patched_figure

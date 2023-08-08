from plotly import graph_objects as go


def create_rect(
    center_x,
    center_y,
    rect_width,
    rect_height,
    scan_width,
    scan_height,
    line_color="black",
    line_width=5,
):
    return go.layout.Shape(
        type="rect",
        x0=max(0, int(center_x - rect_width / 2)),
        y0=max(0, int(center_y - rect_height / 2)),
        x1=min(scan_width - 1, int(center_x + rect_width / 2)),
        y1=min(scan_height - 1, int(center_y + rect_height / 2)),
        line=dict(color=line_color, width=line_width),
    )

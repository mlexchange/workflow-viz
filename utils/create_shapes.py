from plotly import graph_objects as go


def create_cross(
    center_x,
    center_y,
    width,
    height,
    scan_width,
    scan_height,
    line_color="rgba(255, 0, 0, 0.7)",
    line_width=3,
):
    horizontal_line = go.layout.Shape(
        type="line",
        x0=max(0, int(center_x)),
        y0=max(0, int(center_y - height / 2)),
        x1=min(scan_width - 1, int(center_x)),
        y1=min(scan_height - 1, int(center_y + height / 2)),
        line=dict(color=line_color, width=line_width),
    )
    vertical_line = go.layout.Shape(
        type="line",
        x0=max(0, int(center_x - width / 2)),
        y0=max(0, int(center_y)),
        x1=min(scan_width - 1, int(center_x + width / 2)),
        y1=min(scan_height - 1, int(center_y)),
        line=dict(color=line_color, width=line_width),
    )
    return horizontal_line, vertical_line


def create_rect_center_line(
    center_x,
    center_y,
    rect_width,
    rect_height,
    scan_width,
    scan_height,
    line_color="rgba(255, 255, 255, 0.7)",
    line_width=3,
    line_width_center=1,
    horizontal=True,
):
    # Define the rectangle
    rect = go.layout.Shape(
        type="rect",
        x0=max(0, int(center_x - rect_width / 2)),
        y0=max(0, int(center_y - rect_height / 2)),
        x1=min(scan_width - 1, int(center_x + rect_width / 2)),
        y1=min(scan_height - 1, int(center_y + rect_height / 2)),
        line=dict(color=line_color, width=line_width),
    )

    # Define the center line (dashed)
    if horizontal:
        center_line = go.layout.Shape(
            type="line",
            x0=max(0, int(center_x - rect_width / 2)),
            y0=center_y,
            x1=min(scan_width - 1, int(center_x + rect_width / 2)),
            y1=center_y,
            line=dict(color=line_color, width=line_width_center, dash="dash"),
        )
    else:
        center_line = go.layout.Shape(
            type="line",
            x0=center_x,
            y0=max(0, int(center_y - rect_height / 2)),
            x1=center_x,
            y1=min(scan_height - 1, int(center_y + rect_height / 2)),
            line=dict(color=line_color, width=line_width_center, dash="dash"),
        )

    return rect, center_line

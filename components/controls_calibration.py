import dash_mantine_components as dmc
from dash import html


def layout():
    # beamcenter_x:
    # beamcenter_y:
    # wavelength: 0.00000000105
    # pixel_size: 172
    # sample_detector_distance: 5560
    # detector_tilt: 0
    # detector_rotation: 0
    # mask_path
    # detector_image_sample

    masks_available = []

    mask = dmc.Grid(
        children=[
            dmc.Col(dmc.Text("Mask")),
            dmc.Col(
                dmc.Select(
                    id="mask_uri",
                    data=masks_available,
                    value=masks_available[0] if masks_available else None,
                    placeholder="Select a mask...",
                )
            ),
            dmc.Space(h=20),
        ]
    )

    return html.Div(
        id="controls_calibration",
        children=[mask],
        style={
            "display": "block",
        },
    )

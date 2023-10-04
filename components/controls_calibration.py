import dash_mantine_components as dmc
from dash import html

from utils.data_retrieval import get_mask_options, get_scan_options


def layout():
    # beamcenter_x:
    # beamcenter_y:
    # wavelength: 0.00000000105
    # pixel_size: 172
    # sample_detector_distance: 5560
    # detector_tilt: 0
    # detector_rotation: 0

    scans_available = get_scan_options()

    scan = dmc.Grid(
        children=[
            dmc.Col(dmc.Text("Scan")),
            dmc.Col(
                dmc.Select(
                    id="scan_uri",
                    data=scans_available,
                    value=scans_available[0] if scans_available else None,
                    placeholder="Select a calibration scan...",
                )
            ),
            dmc.Space(h=20),
        ]
    )

    masks_available = get_mask_options()

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
        children=[scan, mask],
        style={
            "display": "block",
        },
    )

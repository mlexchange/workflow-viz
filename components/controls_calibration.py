import dash_mantine_components as dmc
from dash import html

from utils.data_retrieval import get_mask_options, get_scan_options


def layout():
    scans_available = get_scan_options()

    scan = dmc.Grid(
        children=[
            dmc.Col(dmc.Text("Scan")),
            dmc.Col(
                dmc.Select(
                    id="scan-uri",
                    data=scans_available,
                    value=None,
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
                    id="mask-uri",
                    data=masks_available,
                    value=None,
                    placeholder="Select a mask...",
                ),
            ),
            dmc.Space(h=20),
        ]
    )

    beamcenter = dmc.Grid(
        children=[
            dmc.Col(dmc.Text("Calibration Values")),
            dmc.Col(
                dmc.NumberInput(
                    label="Beam Center X",
                    description="in pixel",
                    id="beamcenter_x",
                    type="number",
                    value=0,
                    precision=3,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Beam Center Y",
                    description="in pixel",
                    id="beamcenter_y",
                    value=0,
                    precision=3,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Wavelength",
                    description="in ångström",
                    id="wavelength",
                    value=0,
                    precision=4,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Incident Angle",
                    description="in degrees",
                    id="indicent-angle",
                    value=0,
                    precision=3,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=1,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Pixel Size",
                    description="in microns",
                    id="pix-size",
                    value=0,
                    precision=0,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Sample Detector Distance",
                    description="in millimeter",
                    id="sdd",
                    value=0,
                    precision=5,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Detector Rotation",
                    description="in degrees",
                    id="detector-rotation",
                    value=0,
                    precision=5,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=10,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Detector Tilt",
                    description="in degrees",
                    id="detector-tilt",
                    value=0,
                    precision=5,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                ),
                span=3,
            ),
            dmc.Space(h=20),
        ]
    )

    return html.Div(
        id="controls-calibration",
        children=[scan, mask, beamcenter],
        style={
            "display": "block",
        },
    )

import dash_mantine_components as dmc
from dash import dcc, html

from utils.data_retrieval import get_mask_options, get_scan_options


def layout():
    scans_available = get_scan_options()
    masks_available = get_mask_options()

    scan_mask_selection = dmc.Grid(
        children=[
            dmc.Col(
                dmc.Select(
                    label="Scan",
                    id="scan-name",
                    data=list(scans_available.keys()),
                    value=None,
                    placeholder="Select a calibration scan...",
                ),
                span=12,
            ),
            dmc.Col(
                dmc.Select(
                    label="Experiment",
                    id="experiment-type",
                    data=["SAXS", "WAXS", "GISAXS", "GIWAXS"],
                    value=None,
                    placeholder="Select experiment type...",
                ),
                span=3,
            ),
            dmc.Col(
                dmc.Select(
                    label="Mask",
                    id="mask-name",
                    data=list(masks_available.keys()),
                    value=None,
                    placeholder="Select a mask...",
                ),
                span=9,
            ),
            dcc.Store(id="scan-name-uri-map", data=scans_available),
            dcc.Store(id="mask-name-uri-map", data=masks_available),
            dmc.Space(h=20),
        ]
    )

    experiment_type = dmc.Grid(
        children=[
            dmc.Space(h=20),
        ]
    )

    calibration_values = dmc.Grid(
        children=[
            dmc.Col(
                dmc.NumberInput(
                    label="Beam Center X",
                    description="in pixel",
                    id="beamcenter-x",
                    type="number",
                    value=0,
                    precision=3,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                    persistence=True,
                    persistence_type="session",
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Beam Center Y",
                    description="in pixel",
                    id="beamcenter-y",
                    value=0,
                    precision=3,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                    persistence=True,
                    persistence_type="session",
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
                    persistence=True,
                    persistence_type="session",
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Incident Angle",
                    description="in degrees",
                    id="incident-angle",
                    value=0,
                    precision=3,
                    step=0.01,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=1,
                    disabled=True,
                    persistence=True,
                    persistence_type="session",
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
                    persistence=True,
                    persistence_type="session",
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Detector Distance",
                    description="in millimeter",
                    id="sample-detector-dist",
                    value=0,
                    precision=5,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                    persistence=True,
                    persistence_type="session",
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
                    persistence=True,
                    persistence_type="session",
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
                    persistence=True,
                    persistence_type="session",
                ),
                span=3,
            ),
            dmc.Space(h=20),
        ]
    )

    return html.Div(
        id="controls-calibration",
        children=[experiment_type, scan_mask_selection, calibration_values],
        style={
            "display": "block",
        },
    )

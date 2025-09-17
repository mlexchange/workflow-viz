import dash_mantine_components as dmc
from dash import dcc, html
import tiled_viewer  # Import the TiledViewer component
import os

# Get API key from environment variable if needed
# TILED_API_KEY = os.getenv("TILED_API_KEY")
TILED_URI = os.getenv("TILED_URI", "http://127.0.0.1:8888")

def layout():

    scan_mask_selection = dmc.Grid(
        children=[
            # Scan selection with TiledViewer only
            dmc.Col(
                html.Div([
                    dmc.Text("Scan"),
                    # TiledViewer component for scan selection
                    tiled_viewer.TiledViewer(
                        id='scan-selector',
                        tiledBaseUrl=f"https://tiled.localhost/api/v1",
                        isPopup=True,
                        isButtonMode=True,
                        buttonModeText="Select Calibration Scan",
                        inButtonModeShowSelectedData=True

                    ),
                    # Hidden input field to store the selected scan URI
                    dmc.TextInput(
                        id="scan-uri-input",
                        style={"display": "none"},  # Hide it with CSS
                    ),
                ]),
                span=12,
            ),
            # Experiment type selection (unchanged)
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
            # Mask selection with TiledViewer only
            dmc.Col(
                html.Div([
                    dmc.Text("Mask"),
                    # TiledViewer component for mask selection
                    tiled_viewer.TiledViewer(
                        id='mask-selector',
                        tiledBaseUrl=f"{TILED_URI}/api/v1",
                        isPopup=True,
                        isButtonMode=True,
                        buttonModeText="Select Mask",
                        inButtonModeShowSelectedData=True
                    ),
                    # Hidden input field to store the selected mask URI
                    dmc.TextInput(
                        id="mask-uri-input",
                        style={"display": "none"},  # Hide it with CSS
                    ),
                ]),
                span=9,
            ),
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
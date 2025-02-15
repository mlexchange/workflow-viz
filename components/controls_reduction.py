import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

COMPONENT_STYLE = {
    "width": "800px",
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
    "display": "block",
}


def layout():
    # radial_vs_azimuthal = dmc.Switch()
    # game-icons:radial-balance

    controls_integration = dmc.Grid(
        id="controls-reduction-integration",
        children=[
            dmc.Col(
                dmc.NumberInput(
                    label="Number of Bins",
                    description="bins = output points",
                    id="num-bins-integration",
                    type="number",
                    value=1000,
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
                span=9,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Radial Range Min",
                    description="in pixel [0, ...]",
                    id="radial-range-min",
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
                    label="Radial Range Max",
                    description="in pixel [0, ...]",
                    id="radial-range-max",
                    value=5000,
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
                    label="Azimuthal Range Min",
                    description="in degrees [-180,180]",
                    id="azimuthal-range-min",
                    value=-180,
                    precision=0,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=1,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="Azimuthal Range",
                    description="in degrees [-180,180]",
                    id="azimuthal-range-max",
                    value=180,
                    precision=0,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=100,
                    persistence=True,
                    persistence_type="session",
                ),
                span=3,
            ),
        ],
    )

    controls_horizontal_cut = dmc.Grid(
        id="controls-reduction-cut",
        children=[
            dmc.Col(
                dmc.NumberInput(
                    label="Cut Position in Y",
                    description="in pixel [0, ...]",
                    id="cut-pos-y",
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
                    label="Half Width of Cut",
                    description="in pixel [0, ...]",
                    id="horizontal-cut-half-width",
                    type="number",
                    value=5,
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
                    label="X Min",
                    description="in pixel [0, ...]",
                    id="horizontal-x-min",
                    value=0,
                    precision=0,
                    size="sm",
                    stepHoldDelay=500,
                    stepHoldInterval=1,
                ),
                span=3,
            ),
            dmc.Col(
                dmc.NumberInput(
                    label="X Max",
                    description="in pixel [0, ...]",
                    id="horizontal-x-max",
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
        ],
    )

    return html.Div(
        id="controls-reduction",
        style=COMPONENT_STYLE,
        children=[
            controls_integration,
            controls_horizontal_cut,
            dmc.Space(h=20),
            dmc.Center(
                dmc.Button(
                    "Compute Reduction",
                    id="compute-reduction-button",
                    leftIcon=DashIconify(icon="material-symbols:calculate"),
                ),
            ),
        ],
    )

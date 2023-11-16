import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def layout():
    peak_shape = dmc.Select(
        label="Parameters",
        id="fitting-peak-shape",
        data=["Gaussian", "Voigt"],
        value="Voigt",
        placeholder="Select peak shape...",
    )

    return html.Div(
        id="controls-fitting",
        children=[
            peak_shape,
            dmc.Space(h=20),
            dmc.Center(
                dmc.Button(
                    "Compute Reduction",
                    id="compute-reduction-button",
                    leftIcon=DashIconify(icon="material-symbols:calculate"),
                ),
            ),
        ],
        style={
            "display": "block",
        },
    )

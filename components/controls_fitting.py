import dash_mantine_components as dmc
from dash import dash_table, html
from dash.dash_table.Format import Format
from dash_iconify import DashIconify


def layout():
    peak_shape = dmc.Select(
        label="Parameters",
        id="fitting-peak-shape",
        data=["Gaussian", "Voigt"],
        value="Voigt",
        placeholder="Select peak shape...",
    )

    fitting_initialization = html.Div(
        children=[
            dmc.Center(dmc.Text("Initial Peaks")),
            dash_table.DataTable(
                id="fitting-initialization-table",
                columns=[
                    {
                        "name": "Peak X",
                        "id": "peak-x",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Peak Y",
                        "id": "peak-y",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Initial Standard Deviation",
                        "id": "stddev",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Initial FWHM_G",
                        "id": "fwhm-g",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Initial FWHM_L",
                        "id": "fwhm-l",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                ],
                data=[
                    {
                        "peak-x": 0,
                        "peak-y": 1,
                        "stddev": 0.01,
                        "fwhm-g": 0.01,
                        "fwhm-l": 0.01,
                    }
                ],
                editable=True,
                row_deletable=True,
            ),
        ]
    )

    return html.Div(
        id="controls-fitting",
        children=[
            peak_shape,
            fitting_initialization,
            dmc.Space(h=20),
            dmc.Center(
                dmc.Button(
                    "Compute Fitting",
                    id="compute-fitting-button",
                    leftIcon=DashIconify(icon="material-symbols:calculate"),
                ),
            ),
        ],
        style={
            "display": "none",
        },
    )

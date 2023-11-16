import dash_mantine_components as dmc
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format

COMPONENT_STYLE = {
    #    "width": "800px",
    #    "height": "calc(60vh - 40px)",
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
}

FITTING_FIGURE_CONFIG = {"displayModeBar": False}


def layout():
    peak_table = html.Div(
        children=[
            dmc.Center(dmc.Text("Current Tags")),
            dash_table.DataTable(
                id="peak-table",
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
                        "name": "SD",
                        "id": "stddev",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "FWHM_G",
                        "id": "fwhm-g",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "FWHM_L",
                        "id": "fwhm-l",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Fitted Peak X",
                        "id": "fitted-peak-x",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Fitted Peak Y",
                        "id": "fitted-peak-y",
                        "type": "numeric",
                        "format": Format(precision=2),
                    },
                    {
                        "name": "Fitted FWHM",
                        "id": "fitted-fwhm",
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
                        "fitted-peak-x": None,
                        "fitted-peak-y": None,
                        "fitted-fwhm": None,
                    }
                ],
                editable=True,
                row_deletable=True,
            ),
        ]
    )

    # Definition of warning modal
    fitting_warning = dmc.Modal(
        title="Warning",
        children=[
            dmc.Text(
                "Fitting process failed. Please adjust the parameters and try again."
            ),
        ],
        id="fitting-warning",
        is_open=False,
        style={"color": "red"},
    )

    figure = None

    return html.Div(
        id="fitting-container",
        style=COMPONENT_STYLE,
        children=[
            dmc.Center(children=dmc.Text("Fitting", weight=500, size="lg")),
            dcc.Graph(id="fitting-viewer", figure=figure, config=FITTING_FIGURE_CONFIG),
            peak_table,
            fitting_warning,
        ],
    )

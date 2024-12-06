import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import dash_table, dcc, html
from dash.dash_table.Format import Format

COMPONENT_STYLE = {
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
    "display": "none",
}

FITTING_FIGURE_CONFIG = {"displayModeBar": False}


def layout():
    fitting_result = html.Div(
        children=[
            dmc.Center(dmc.Text("Fitted Peaks")),
            dash_table.DataTable(
                id="fitting-result-table",
                columns=[
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
                        "fitted-peak-x": None,
                        "fitted-peak-y": None,
                        "fitted-fwhm": None,
                    }
                ],
                editable=False,
                row_deletable=True,
            ),
        ]
    )

    figure_layout = go.Layout(
        # title=dict(text="Step Preview", automargin=True, yref="paper"),
        plot_bgcolor="#FFFFFF",
        hovermode="x",
        # Distance to show hover label of data point
        hoverdistance=100,
        # Distance to show spike
        spikedistance=1000,
        xaxis=dict(
            title="pixel",
            linecolor="#BCCCDC",
            # Show spike line for X-axis
            showspikes=True,
            # Format spike
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across",
        ),
        yaxis=dict(title="intensity", linecolor="#BCCCDC"),
        margin={"b": 10, "t": 20},
    )

    figure = go.Figure(data=go.Scatter(), layout=figure_layout)
    figure.update_traces(line_color="#1f78b4")

    return html.Div(
        id="fitting-container",
        style=COMPONENT_STYLE,
        children=[
            dmc.Center(children=dmc.Text("Fitting", weight=500, size="lg")),
            dcc.Graph(id="fitting-viewer", figure=figure, config=FITTING_FIGURE_CONFIG),
            fitting_result,
        ],
    )

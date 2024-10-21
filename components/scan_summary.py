import dash_mantine_components as dmc
import numpy as np
import plotly.graph_objects as go
from dash import dcc, html

COMPONENT_STYLE = {
    "width": "1000px",
    "height": "calc(90vh - 40px)",
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
}

SCAN_FIGURE_CONFIG = {"displayModeBar": False}
SCAN_FIGURE_LAYOUT = go.Layout(
    # title=dict(text="Scan", automargin=True, yref="container"),
    plot_bgcolor="#FFFFFF",
    xaxis=dict(title="Sample X Stage", linecolor="#BCCCDC", autorange="reversed"),
    yaxis=dict(
        title="Sample Y Stage",
        linecolor="#BCCCDC",
        scaleanchor="x",
        autorange="reversed",
    ),
    margin={"b": 10, "t": 25},
)


def layout(x_data, y_data, feature_data, feature_name, data_uris):
    cmin = np.percentile(feature_data, 1)
    cmax = np.percentile(feature_data, 99)

    figure = go.Figure(layout=SCAN_FIGURE_LAYOUT)

    figure.add_trace(
        go.Scatter(
            x=x_data,
            y=y_data,
            mode="markers",
            marker=dict(
                size=15,
                color=feature_data,
                colorbar=dict(title=feature_name),
                cmin=cmin,
                cmax=cmax,
            ),
            hovertemplate="Sample X Stage: $%{x:.2f}"
            + "<br>Sample Y Stage: %{y:.2f}"
            + "<br>"
            + feature_name
            + ": %{customdata:.2f}"
            "<br>%{text}",
            text=data_uris,
            customdata=feature_data,
        )
    )

    return html.Div(
        id="scan-summary-container",
        style=COMPONENT_STYLE,
        children=[
            dmc.Center(children=dmc.Text("Scan Summary", weight=500, size="lg")),
            dmc.LoadingOverlay(
                id="scan-summary-viewer-loading",
                overlayOpacity=0,
                loaderProps=dict(
                    color=dmc.theme.DEFAULT_COLORS["blue"][6], variant="bars"
                ),
                children=[
                    dcc.Graph(
                        id="scan-summary-viewer",
                        figure=figure,
                        config=SCAN_FIGURE_CONFIG,
                    ),
                ],
            ),
        ],
    )

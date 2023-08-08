import plotly.graph_objects as go
from dash import dcc, html

COMPONENT_STYLE = {
    #    "width": "800px",
    #    "height": "calc(60vh - 40px)",
    "padding": "10px",
    "borderRadius": "5px",
    "overflowY": "auto",
}


def layout():
    figure_layout = go.Layout(
        title="Step Preview",
        plot_bgcolor="#FFFFFF",
        hovermode="x",
        hoverdistance=100,  # Distance to show hover label of data point
        spikedistance=1000,  # Distance to show spike
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
        yaxis=dict(title="mean intensity", linecolor="#BCCCDC"),
    )

    # figure = px.line(markers=False)

    figure = go.Figure(data=go.Scatter(), layout=figure_layout)
    figure.update_traces(line_color="#1f78b4")
    # figure.update_layout(hovermode="y")

    return html.Div(
        style=COMPONENT_STYLE,
        children=[
            dcc.Graph(id="reduction", figure=figure),
        ],
    )

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
    return html.Div(
        id="controls-reduction",
        style=COMPONENT_STYLE,
        children=[
            dmc.Center(
                dmc.Switch(
                    id="cut-direction",
                    offLabel=DashIconify(
                        icon="material-symbols:border-horizontal",
                        color=dmc.theme.DEFAULT_COLORS["blue"][6],
                        width=20,
                    ),
                    onLabel=DashIconify(
                        icon="mdi:border-vertical",
                        width=20,
                    ),
                    label="Vertical Cut",
                    checked=False,
                    size="lg",
                )
            ),
            dmc.AccordionMultiple(
                children=[
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(
                                "Width",
                                icon=DashIconify(
                                    icon="material-symbols:width",
                                    color=dmc.theme.DEFAULT_COLORS["blue"][6],
                                    width=20,
                                ),
                            ),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Space(h=20),
                                    dmc.Slider(
                                        id="cut-width",
                                        value=5,
                                        min=0,
                                        max=10000,
                                        step=1,
                                        size="sm",
                                        labelAlwaysOn=True,
                                    ),
                                ],
                            ),
                        ],
                        value="width",
                    ),
                    dmc.AccordionItem(
                        [
                            dmc.AccordionControl(
                                "Height",
                                icon=DashIconify(
                                    icon="material-symbols:height",
                                    color=dmc.theme.DEFAULT_COLORS["blue"][6],
                                    width=20,
                                ),
                            ),
                            dmc.AccordionPanel(
                                children=[
                                    dmc.Space(h=20),
                                    dmc.Slider(
                                        id="cut-height",
                                        value=1000,
                                        min=0,
                                        max=10000,
                                        step=1,
                                        size="sm",
                                        labelAlwaysOn=True,
                                    ),
                                ]
                            ),
                        ],
                        value="height",
                    ),
                ],
            ),
        ],
    )

import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def layout():
    config_import_button = dmc.Affix(
        dmc.Button(
            children=[
                DashIconify(
                    icon="mdi:database-import",
                    height=25,
                    style={"cursor": "pointer"},
                ),
                dmc.Text("Import Config", size="sm"),
            ],
            id="config-import-button",
            size="lg",
            radius="sm",
            compact=True,
            variant="outline",
            color="blue",
        ),
        position={"right": "25px", "top": "25px"},
    )

    config_import_modal = dmc.Modal(
        title="Directly set configuration parameters.",
        id="config-import-modal",
        zIndex=10000,
        children=[
            dmc.Space(h=20),
            dmc.JsonInput(
                label="Configuration parameters",
                placeholder='{\n  "beamcenter_x": 500\n  ...\n}',
                validationError="Invalid json",
                formatOnBlur=True,
                autosize=True,
                minRows=10,
                id="config-import-parmeters",
            ),
            dmc.Group(
                [
                    dmc.Button("Apply", id="config-import-apply-button"),
                ],
                position="right",
            ),
        ],
    )

    return html.Div(
        id="config-import-container",
        children=[config_import_button, config_import_modal],
    )

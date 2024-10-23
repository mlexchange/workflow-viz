import dash_mantine_components as dmc

# from PIL import Image
from dash import dash_table, dcc, html


def interface_components():
    experiment_name_input = dcc.Dropdown(
        options=[],
        placeholder="Select an experiment",
        id="experiment-name-dropdown",
        style={"width": 250},
    )

    select_experiment_button = dmc.Button(
        id="select-expt-button",
        children="Select Experiment",
        variant="filled",
        style={"width": 250},
    )

    column_names_input = dcc.Dropdown(
        options=[],
        placeholder="Select uneditable columns",
        id="columns-name-dropdown",
        style={"width": 250},
        multi=True,
    )

    select_column_button = dmc.Button(
        id="select-column-button",
        children="Select Column",
        variant="filled",
        style={"width": 250},
    )

    # stack = dmc.Aside(
    #     p="md",
    #     width={"base": 300},
    #     height="30%",
    #     fixed=True,
    #     position={"left": 0, "top": 0},
    #     children=[
    #         html.Div(["Experiment name"]),
    #         experiment_name_input,
    #         dmc.Space(h=8),
    #         select_experiment_button,
    #     ],
    # )
    stack = html.Div(
        children=[
            html.Div(["Experiment name"]),
            dmc.Space(h=8),
            experiment_name_input,
            dmc.Space(h=8),
            select_experiment_button,
            dmc.Space(h=16),
            html.Div(["Select uneditabl column names"]),
            dmc.Space(h=8),
            column_names_input,
            dmc.Space(h=8),
            select_column_button,
        ],
    )

    return stack


def table_modification_components():
    metadata_table = dash_table.DataTable(id="example-table", editable=True)

    add_row_button = dmc.Button("Add a row", id="add-row-button")
    save_data_button = dmc.Button("Save Data", id="save-data-button")
    refresh_data_button = dmc.Button("Refresh Table", id="refresh-data-button")

    buttons_group = dmc.Group(
        position="center",
        spacing="md",
        children=[refresh_data_button, add_row_button, save_data_button],
    )

    saved_popup = dmc.Modal(title="Saved!", id="saved-popup", size="lg")

    table_components = html.Div([saved_popup, metadata_table, buttons_group])

    return table_components

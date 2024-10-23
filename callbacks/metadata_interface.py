import pandas as pd
from dash import Input, Output, State, callback

from utils.data_retrieval import (
    get_column_names,
    get_csv_file_uri,
    get_processed_experiment_names,
    tiled_read_csv,
    write_csv_from_interface,
)
from utils.metadata_utils import calculate_ratios  # generate_next_scan_name


# generating the list of experiments for the dropdown
@callback(
    Output(component_id="experiment-name-dropdown", component_property="options"),
    Input(component_id="experiment-name-dropdown", component_property="search_value"),
)
def experiment_name_retrieval(search_value):
    # Gets experiment names from tiled server under the 'processed' node
    list_of_experiments = get_processed_experiment_names()
    return list_of_experiments


@callback(
    Output(component_id="columns-name-dropdown", component_property="options"),
    Input(component_id="select-expt-button", component_property="n_clicks"),
    State(component_id="experiment-name-dropdown", component_property="value"),
    prevent_initial_call=True,
)
def column_name_retrieval(n_clicks, experiment_name):
    if experiment_name is None:
        return []
    # Gets the table data from the Tiled csv node of the experiment name
    column_names_list = get_column_names(experiment_name)
    return column_names_list


@callback(
    Output(
        component_id="example-table", component_property="data", allow_duplicate=True
    ),
    Output(component_id="example-table", component_property="columns"),
    Input(component_id="select-column-button", component_property="n_clicks"),
    State(component_id="experiment-name-dropdown", component_property="value"),
    State(component_id="columns-name-dropdown", component_property="value"),
    prevent_initial_call=True,
)
def select_experiment(n_clicks, experiment_name, uneditable_column_names):
    if experiment_name is None:
        return [], []

    # Gets the table data from the Tiled csv node of the experiment name
    csv_file_uri = get_csv_file_uri(experiment_name)
    metadata_table = tiled_read_csv(csv_file_uri)

    # Add columns
    columns = [{"name": i, "id": i} for i in metadata_table.columns]
    # column["format"] = Format(scheme=Scheme.decimal, precision=2)

    # create uneditable columns for the table:
    # uneditable_column_names = ["fraction_A", "fraction_B", "fraction_C"]
    for column in columns:
        if column["name"] in uneditable_column_names:
            column["editable"] = False
    metadata_table = metadata_table.to_dict("records")
    return metadata_table, columns


@callback(
    Output(
        component_id="example-table", component_property="data", allow_duplicate=True
    ),
    Input(component_id="add-row-button", component_property="n_clicks"),
    State(component_id="example-table", component_property="data"),
    State(component_id="example-table", component_property="columns"),
    prevent_initial_call=True,
)
def add_row(n_clicks, table_data, columns):
    # Adding an empty row to the table by getting column names from
    # the first entry in the table. It is a list of dictionaries, but
    # once the column names are added in select_experiment()
    # modify this function to use 'columns' instead of 'table_data[0]'
    # print(table_data)
    # print(type(table_data))
    # new_scan_name = generate_next_scan_name(table_data)
    new_row = {c: "" for c in table_data[0]}
    # new_row["scan_uri"] = new_scan_name
    table_data.append(new_row)
    return table_data


@callback(
    Output(component_id="example-table", component_property="data"),
    Input(component_id="example-table", component_property="data_timestamp"),
    State(component_id="example-table", component_property="data"),
    prevent_initial_call=True,
)
def calculate_table_ratios(timestamp, rows):
    # This callback is used to update the table data when the table is edited
    # print("Calculating ratios")
    for row in rows:
        # Check if any of the required values are None
        if (
            row["Step 1, 58k"] is not None
            and row["Step 1, 34k"] is not None
            and row["Swell ratio"] is not None
        ):
            (
                row["Fraction 58k"],
                row["Fraction 34k"],
                row["Fraction Additive"],
            ) = calculate_ratios(
                row["Step 1, 58k"], row["Step 1, 34k"], row["Swell ratio"]
            )
    return rows


@callback(
    Output(component_id="saved-popup", component_property="opened"),
    Input(component_id="save-data-button", component_property="n_clicks"),
    State(component_id="experiment-name-dropdown", component_property="value"),
    State(component_id="example-table", component_property="data"),
    State(component_id="saved-popup", component_property="opened"),
    prevent_initial_call=True,
)
def save_data(n_clicks, experiment_name, table_data, opened):
    write_csv_from_interface(experiment_name, pd.DataFrame(table_data))
    # send a call to the Tiled server to save the data
    # overwrite the csv on the file system
    return not opened


@callback(
    Output(
        component_id="example-table", component_property="data", allow_duplicate=True
    ),
    Input(component_id="refresh-data-button", component_property="n_clicks"),
    State(component_id="experiment-name-dropdown", component_property="value"),
    prevent_initial_call=True,
)
def refresh_data(n_clicks, experiment_name):
    if experiment_name is None:
        return []
    csv_file_uri = get_csv_file_uri(experiment_name)
    print(csv_file_uri)
    metadata_table = tiled_read_csv(csv_file_uri)
    # The conversion to dictionary is necessary to avoid a non-JSON serializable error
    metadata_table = metadata_table.to_dict("records")
    return metadata_table

from dash import Input, Output, Patch, State, callback
import pandas as pd

from utils.data_retrieval import get_processed_experiment_names, get_csv_file_uri, tiled_read_csv, write_csv_from_interface

# generating the list of experiments for the dropdown
@callback(
    Output(component_id="experiment-name-dropdown", component_property="options"),
    Input(component_id="experiment-name-dropdown", component_property="search_value"),
)
def experiment_name_retrieval(search_value):
    list_of_experiments = get_processed_experiment_names()
    return list_of_experiments

@callback(
    Output(component_id="example-table", component_property="data", allow_duplicate=True),
    Output(component_id="example-table", component_property="columns"),
    Input(component_id="select-expt-button", component_property="n_clicks"),
    State(component_id="experiment-name-dropdown", component_property="value"),
    prevent_initial_call=True,
)
def select_experiment(n_clicks, experiment_name):
    csv_file_uri = get_csv_file_uri(experiment_name)
    metadata_table = tiled_read_csv(csv_file_uri)
    # TODO: Add column names to the empty dash_table.DataTable
    columns=[{"name": i, "id": i} for i in metadata_table.columns]
    metadata_table = metadata_table.to_dict("records")
    return metadata_table, columns

@callback(
    Output(component_id="example-table", component_property="data", allow_duplicate=True),
    Input(component_id="add-row-button", component_property="n_clicks"),
    State(component_id="example-table", component_property="data"),
    State(component_id="example-table", component_property="columns"),
    prevent_initial_call=True,
)
def add_row(n_clicks, table_data, columns):
    
    #Adding an empty row to the table by getting column names from the first entry in the table
    # It is a list of dictionaries, but once the column names are added in select_experiment()
    # modify this function to use 'columns' instead of 'table_data[0]'
    print(columns)
    table_data.append({c: "" for c in table_data[0]})
    return table_data

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
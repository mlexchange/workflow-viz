# import numpy as np
from dash import Input, Output, Patch, State, callback, no_update
from dash.exceptions import PreventUpdate

from utils.data_retrieval import get_reduction_data
from utils.prefect import check_status_flow_run


@callback(
    Output("reduction-viewer", "figure", allow_duplicate=True),
    Output("compute-reduction-button", "loading", allow_duplicate=True),
    Output("prefect-flow-run", "data", allow_duplicate=True),
    Input("prefect-flow-check", "n_intervals"),
    State("prefect-flow-run", "data"),
    prevent_initial_call=True,
)
def check_flow(n_intervals, flow_run_info):
    empty_flow_run_info = {"id": None, "result_uri": None}

    if flow_run_info["id"]:
        flow_run_id = flow_run_info["id"]
        status = check_status_flow_run(flow_run_id)
        if status == "completed":
            # Retrieve results and update figure
            patched_figure = Patch()
            flow_run_result_uri = flow_run_info["result_uri"]

            x_values, y_values, x_unit = get_reduction_data(
                flow_run_result_uri,
            )

            patched_figure["data"][0]["x"] = x_values
            patched_figure["data"][0]["y"] = y_values
            patched_figure["layout"]["xaxis"]["title"] = x_unit

            return patched_figure, False, empty_flow_run_info
        elif status == "failed":
            return no_update, False, empty_flow_run_info
        else:
            return no_update, True, no_update
    else:
        raise PreventUpdate


@callback(
    Output("reduction-container", "style"),
    Input("progress-stepper", "active"),
)
def toggle_controls_reduction_visibility(current_step):
    step = current_step if current_step is not None else 0
    if step == 1:
        return {"display": "block"}
    else:
        return {"display": "none"}

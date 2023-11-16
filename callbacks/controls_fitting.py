import asyncio

from dash import Input, Output, State, callback

from utils.prefect import get_full_deployment_names, schedule_prefect_flow


@callback(
    Output("prefect-flow-run", "data"),
    Output("compute-fitting-button", "loading"),
    Input("compute-fitting-button", "n_clicks"),
    State("reduction-result-uri", "data"),
    State("fitting-peak-shape", "value"),
    prevent_initial_call=True,
)
def submit_fitting_to_compute(
    n_clicks,
    reduction_data_uri,
    peak_shape,
):
    if n_clicks:
        parameters = {
            "input_uri_data": reduction_data_uri,
            "peak_shape": peak_shape.lower(),
        }
        flow_name = "fit_peaks_simple"
        reduction_flows = asyncio.run(get_full_deployment_names())
        deployment_name = reduction_flows[flow_name]
        flow_run_id = schedule_prefect_flow(deployment_name, parameters)

        result_uri = reduction_data_uri
        last_container = result_uri.split("/")[-1]
        result_uri += f"/{last_container}_{flow_name}"
        flow_run_data = {"id": flow_run_id, "result_uri": result_uri}
        return flow_run_data, True


@callback(
    Output("controls-fitting", "style"),
    Input("progress-stepper", "active"),
)
def toggle_controls_reduction_visibility(current_step):
    step = current_step if current_step is not None else 0
    if step == 2:
        return {"display": "block"}
    else:
        return {"display": "none"}

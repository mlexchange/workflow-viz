import asyncio

from dash import Input, Output, State, callback

from utils.prefect import get_full_deployment_names, schedule_prefect_flow

REDUCTION_FLOWS = asyncio.run(get_full_deployment_names())


@callback(
    Output("prefect-flow-run", "data"),
    Output("compute-reduction-button", "loading"),
    Input("compute-reduction-button", "n_clicks"),
    State("scan-name", "value"),
    State("scan-name-uri-map", "data"),
    State("mask-name", "value"),
    State("mask-name-uri-map", "data"),
    State("num-bins-integration", "value"),
    prevent_initial_call=True,
)
def submit_reduction_to_compute(
    n_clicks,
    scan_name,
    scan_name_uri_mapper,
    mask_name,
    mask_name_uri_mapper,
    num_bins_integration,
):
    if n_clicks:
        scan_uri = scan_name_uri_mapper[scan_name]
        mask_uri = mask_name_uri_mapper[mask_name]
        parameters = {
            "input_uri_data": scan_uri,
            "input_uri_mask": mask_uri,
            "beamcenter_x": 2945,  # x-coordiante of the beam center postion in pixel
            "beamcenter_y": 900,  # y-coordiante of the beam center postion in pixel
            "sample_detector_dist": 833.8931,  # sample-detector-distance in mm
            "pix_size": 55,  # pixel size in microns
            "wavelength": 1.044,  # wavelength in Angstrom
            "polarization_factor": 0.99,
            "num_bins": num_bins_integration,
            "chi_min": -180,
            "chi_max": 180,
            "inner_radius": 1,
            "outer_radius": 2900,
            "rotation": 49.530048,  # detector rotation in degrees (Fit2D convention)
            "tilt": 1.688493,  # detector tilt in degrees (Fit2D convention)
            "output_unit": "q",  # "q"
        }
        flow_name = "integration-azimuthal"
        deployment_name = REDUCTION_FLOWS[flow_name]
        flow_run_id = schedule_prefect_flow(deployment_name, parameters)

        result_uri = scan_uri.replace("raw/", "/processed/")
        last_container = result_uri.split("/")[-1]
        result_uri += f"/{last_container}_{flow_name}"
        flow_run_data = {"id": flow_run_id, "result_uri": result_uri}
        return flow_run_data, True


@callback(
    Output("controls-reduction", "style"),
    Input("progress-stepper", "active"),
)
def toggle_controls_reduction_visibility(current_step):
    step = current_step if current_step is not None else 0
    if step == 1:
        return {"display": "block"}
    else:
        return {"display": "none"}

from dash import Input, Output, State, callback

from utils.prefect import get_full_deployment_names, schedule_prefect_flow


@callback(
    Output("prefect-flow-run", "data"),
    Output("compute-reduction-button", "loading"),
    Input("compute-reduction-button", "n_clicks"),
    State("scan-name", "value"),
    State("scan-name-uri-map", "data"),
    State("mask-name", "value"),
    State("mask-name-uri-map", "data"),
    State("beamcenter-x", "value"),
    State("beamcenter-y", "value"),
    State("wavelength", "value"),
    State("incident-angle", "value"),
    State("pix-size", "value"),
    State("sample-detector-dist", "value"),
    State("detector-rotation", "value"),
    State("detector-tilt", "value"),
    State("num-bins-integration", "value"),
    State("radial-range-min", "value"),
    State("radial-range-max", "value"),
    State("azimuthal-range-min", "value"),
    State("azimuthal-range-max", "value"),
    prevent_initial_call=True,
)
def submit_reduction_to_compute(
    n_clicks,
    scan_name,
    scan_name_uri_mapper,
    mask_name,
    mask_name_uri_mapper,
    beamcenter_x,
    beamcenter_y,
    wavelength,
    incident_angle,
    pix_size,
    sample_detector_dist,
    detector_rotation,
    detector_tilt,
    num_bins_integration,
    radial_range_min,
    radial_range_max,
    azimuthal_range_min,
    azimuthal_range_max,
):
    if n_clicks:
        scan_uri = scan_name_uri_mapper[scan_name]
        mask_uri = mask_name_uri_mapper[mask_name]
        parameters = {
            "input_uri_data": scan_uri,
            "input_uri_mask": mask_uri,
            "beamcenter_x": beamcenter_x,
            "beamcenter_y": beamcenter_y,
            "wavelength": wavelength,
            "polarization_factor": 0.99,
            "sample_detector_dist": sample_detector_dist,
            "pix_size": pix_size,
            "rotation": detector_rotation,
            "tilt": detector_tilt,
            "num_bins": num_bins_integration,
            "chi_min": azimuthal_range_min,
            "chi_max": azimuthal_range_max,
            "inner_radius": radial_range_min,
            "outer_radius": radial_range_max,
            "output_unit": "q",  # "q"
        }
        flow_name = "integration-azimuthal"
        reduction_flows = get_full_deployment_names()
        deployment_name = reduction_flows[flow_name]
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

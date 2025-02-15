from dash import Input, Output, State, callback

from app import redis_conn


@callback(
    Output("prefect-flow-run", "data"),
    Output("compute-reduction-button", "loading"),
    Input("compute-reduction-button", "n_clicks"),
    State("scan-name", "value"),
    State("scan-name-uri-map", "data"),
    State("mask-name", "value"),
    State("mask-name-uri-map", "data"),
    State("experiment-type", "value"),
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
    State("horizontal-cut-half-width", "value"),
    State("horizontal-cut-pos-y", "value"),
    State("horizontal-x-min", "value"),
    State("horizontal-x-max", "value"),
    prevent_initial_call=True,
)
def submit_reduction_to_compute(
    n_clicks,
    scan_name,
    scan_name_uri_mapper,
    mask_name,
    mask_name_uri_mapper,
    experiment_type,
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
    horizontal_cut_half_width,
    horizontal_cut_pos_y,
    horizontal_cut_x_min,
    horizontal_x_max,
):
    if n_clicks:
        scan_uri = scan_name_uri_mapper[scan_name]
        mask_uri = mask_name_uri_mapper[mask_name]
        parameters_calibration = {
            "input_uri_data": scan_uri,
            "input_uri_mask": mask_uri,
            "beamcenter_x": beamcenter_x,
            "beamcenter_y": beamcenter_y,
            "wavelength": wavelength,
            "sample_detector_dist": sample_detector_dist,
            "pix_size": pix_size,
            "output_unit": "q",  # "q"
        }
        if experiment_type is not None and experiment_type.startswith("GI"):
            parameters_cut = {
                "cut_half_width": horizontal_cut_half_width,
                "cut_pos_y": horizontal_cut_pos_y,
                "x_min": horizontal_cut_x_min,
                "x_max": horizontal_x_max,
            }
            parameters = {
                **parameters_calibration,
                **parameters_cut,
                "incident_angle": incident_angle,
            }
            flow_name = "horizontal-cut"
        else:
            parameters_integration = {
                "num_bins": num_bins_integration,
                "chi_min": azimuthal_range_min,
                "chi_max": azimuthal_range_max,
                "inner_radius": radial_range_min,
                "outer_radius": radial_range_max,
            }
            parameters = {
                **parameters_calibration,
                **parameters_integration,
                "polarization_factor": 0.99,
                "rotation": detector_rotation,
                "tilt": detector_tilt,
            }
            flow_name = "integration-azimuthal"

        reduction_flows = get_full_deployment_names()
        deployment_name = reduction_flows[flow_name]
        flow_run_id = schedule_prefect_flow(deployment_name, parameters)

        redis_conn.set(parameters)
        # flow_name = "integration-azimuthal"
        # reduction_flows = workflow.get_full_deployment_names()
        # deployment_name = reduction_flows[flow_name]
        # flow_run_id = workflow.submit_job(deployment_name, parameters)

        # result_uri = scan_uri.replace("raw/", "/processed/")
        # last_container = result_uri.split("/")[-1]
        # result_uri += f"/{last_container}_{flow_name}"
        # flow_run_data = {"id": flow_run_id, "result_uri": result_uri}
        # return flow_run_data, True


@callback(
    Output("controls-reduction", "style"),
    Output("controls-reduction-integration", "style"),
    Output("controls-reduction-cut", "style"),
    Input("experiment-type", "value"),
    Input("progress-stepper", "active"),
)
def toggle_controls_reduction_visibility(experiment_type, current_step):
    step = current_step if current_step is not None else 0
    if step == 1:
        if experiment_type is not None and experiment_type.startswith("GI"):
            # Show cut controls, hide integration
            return (
                {"display": "block"},
                {"display": "none"},
                {"display": "flex"},
            )
        else:
            # Show integration controls, hide cut
            return (
                {"display": "block"},
                {"display": "flex"},
                {"display": "none"},
            )
    else:
        return {"display": "none"}, {"display": "none"}, {"display": "none"}

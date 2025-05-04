from dash import Input, Output, callback

from utils.data_retrieval import get_mask_options, get_scan_options


@callback(
    Output("incident-angle", "disabled"),
    Input("experiment-type", "value"),
)
def toggle_incident_angle_visibility(experiment_type):
    if experiment_type is not None and experiment_type.startswith("GI"):
        return False
    else:
        return True


@callback(
    Output("controls-calibration", "style"),
    Input("progress-stepper", "active"),
)
def toggle_controls_reduction_visibility(current_step):
    step = current_step if current_step is not None else 0
    if step == 0:
        return {"display": "block"}
    else:
        return {"display": "none"}


@callback(
    Output("scan-name", "data"),
    Output("scan-name-uri-map", "data"),
    Output("mask-name", "data"),
    Output("mask-name-uri-map", "data"),
    Input("scan-list-refresh", "n_clicks"),
)
def refresh_scan_list(n_clicks):
    scans_available = get_scan_options()
    masks_available = get_mask_options()
    return (
        list(scans_available.keys()),
        scans_available,
        list(masks_available.keys()),
        masks_available,
    )

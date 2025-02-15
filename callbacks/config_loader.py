import json

from dash import Input, Output, State, callback, no_update
from dash.exceptions import PreventUpdate


@callback(
    Output("config-import-modal", "opened"),
    Input("config-import-button", "n_clicks"),
    Input("config-import-apply-button", "n_clicks"),
    State("config-import-modal", "opened"),
    prevent_initial_call=True,
)
def open_close_config_import(open, apply, opened):
    return not opened


@callback(
    Output("config-import-parmeters", "value"),
    Output("beamcenter-x", "value", allow_duplicate=True),
    Output("beamcenter-y", "value", allow_duplicate=True),
    Output("wavelength", "value"),
    Output("incident-angle", "value"),
    Output("pix-size", "value"),
    Output("sample-detector-dist", "value"),
    Output("detector-rotation", "value"),
    Output("detector-tilt", "value"),
    Output("num-bins-integration", "value"),
    Output("radial-range-min", "value"),
    Output("radial-range-max", "value"),
    Output("azimuthal-range-min", "value"),
    Output("azimuthal-range-max", "value"),
    Input("config-import-apply-button", "n_clicks"),
    State("config-import-parmeters", "value"),
    prevent_initial_call=True,
)
def apply_config_import(apply, parameters):
    print(parameters)
    if parameters:
        parameters = json.loads(parameters)
    else:
        raise PreventUpdate
    keys_to_update = [
        "beamcenter_x",
        "beamcenter_y",
        "wavelength",
        "incident_angle",
        "pix_size",
        "sample_detector_dist",
        "rotation",
        "tilt",
        "num_bins",
        "inner_radius",
        "outer_radius",
        "chi_min",
        "chi_max",
    ]

    return_vals = [None]
    for updated_key in keys_to_update:
        return_vals.append(parameters.get(updated_key, no_update))
    return tuple(return_vals)

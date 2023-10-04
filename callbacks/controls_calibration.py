from dash import Input, Output, callback


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

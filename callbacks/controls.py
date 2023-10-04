from dash import Input, Output, callback


@callback(Output("cut-direction", "label"), Input("cut-direction", "checked"))
def toggle_cut_direction(checked):
    return f"{'Horizontal' if checked else 'Vertical'} cut"


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

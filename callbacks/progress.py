from dash import Input, Output, State, callback, ctx


@callback(
    Output("progress-stepper", "active"),
    Input("progress-back", "n_clicks"),
    Input("progress-next", "n_clicks"),
    State("progress-stepper", "active"),
    State("progress-min-step", "data"),
    State("progress-max-step", "data"),
    prevent_initial_call=True,
)
def update_progress(back, next, current, min_step, max_step):
    button_id = ctx.triggered_id
    step = current if current is not None else 0
    if button_id == "progress-back":
        step = step - 1 if step > min_step else step
    else:
        step = step + 1 if step < max_step else step
    return step

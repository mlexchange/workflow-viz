from dash import Input, Output, callback


@callback(Output("cut-direction", "label"), Input("cut-direction", "checked"))
def toggle_cut_direction(checked):
    return f"{'Horizontal' if checked else 'Vertical'} cut"

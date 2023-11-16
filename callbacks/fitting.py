# import dash
# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# from dash import ALL, MATCH, callback
from dash import callback
from dash.dependencies import Input, Output  # , State

# @callback(Output("plot_data", "figure"), Input("filename", "value"))
# def display_data(filename):
#     fig = dash.no_update
#     if filename:
#         df = pd.read_csv(filename, delimiter="\t")
#         try:
#             x_data = np.array(df["# q[AA^-1]"])
#             y_data = np.array(df["I[cm^-1]"])
#         except Exception as e:
#             print(f"Data has a different schema: {e}")
#             x_data = np.array(df["# 2t"])
#             y_data = np.array(df["I"])
#         # Remove values out of boundaries
#         y_data[np.where(y_data > 100)] = 0.01
#         y_data[np.where(y_data < 0)] = 0.01
#         fig = plot_data(x_data, y_data)
#     return fig


# @callback(
#     Output("plot_data", "figure", allow_duplicate=True),
#     Output("peak_table", "data"),
#     Input("plot_data", "clickData"),
#     State("plot_data", "figure"),
#     State("peak_table", "data"),
#     prevent_initial_call=True,
# )
# def add_peak(clickdata, fig, table_data):
#     peak_y = clickdata["points"][0]["y"]
#     peak_x = clickdata["points"][0]["x"]
#     if "rangeslider" in fig["layout"]["xaxis"]:
#         del fig["layout"]["xaxis"]["rangeslider"]["yaxis"]
#     # Check that peak_x and peak_y belong to the original dataset
#     fig["data"] = list(filter(lambda d: d["name"] == "Data", fig["data"]))
#     x_data = np.array(fig["data"][0]["x"])
#     y_data = np.array(fig["data"][0]["y"])
#     distances = np.sqrt((x_data - peak_x) ** 2 + (np.array(y_data) - peak_y) ** 2)
#     closest_indx = np.argmin(distances)
#     (peak_x, peak_y) = (x_data[closest_indx], y_data[closest_indx])
#     # Update annotation of figure
#     fig = go.Figure(fig)
#     fig.add_annotation(
#         x=peak_x,
#         y=peak_y,
#         showarrow=True,
#         arrowcolor="black",
#         arrowsize=3,
#         arrowwidth=1,
#         arrowhead=1,
#     )
#     new_peak = {
#         "peak_x": peak_x,
#         "peak_y": peak_y,
#         "stddev": 0.01,
#         "fwhm_g": 0.01,
#         "fwhm_l": 0.01,
#         "fitted_peak_x": None,
#         "fitted_peak_y": None,
#         "fitted_fwhm": None,
#     }
#     if table_data:
#         table_data.append(new_peak)
#     else:
#         table_data = [new_peak]
#     return fig, table_data


# @callback(
#     Output("peak_table", "data", allow_duplicate=True),
#     Output("plot_data", "figure", allow_duplicate=True),
#     Output("modal-warning", "is_open"),
#     Input("peak_shape", "value"),
#     Input("peak_table", "data"),
#     State("peak_table", "data_previous"),
#     State("plot_data", "figure"),
#     prevent_initial_call=True,
# )
# def fit_curve(peak_shape, table_data, old_table_data, fig):
#     open_modal = False
#     if fig is not None:
#         if "rangeslider" in fig["layout"]["xaxis"]:
#             del fig["layout"]["xaxis"]["rangeslider"]["yaxis"]
#         # Gather fitting parameters and data
#         params = pd.DataFrame.from_records(table_data)
#         y_peaks = params["peak_y"].values
#         x_peaks = params["peak_x"].values
#         fwhm_l = params["fwhm_l"].values
#         fwhm_g = params["fwhm_g"].values
#         stddev = params["stddev"].values
#         # Check if a row in table has been deleted
#         if old_table_data is not None and table_data is not None:
#             if len(old_table_data) > len(table_data):
#                 deleted_indxs = [
#                     indx
#                     for indx, row in enumerate(old_table_data)
#                     if row not in table_data
#                 ]
#                 fig = go.Figure(fig)
#                 list_annotations = list(fig.layout.annotations)
#                 for indx in deleted_indxs:
#                     del list_annotations[indx - 1]
#                 fig.layout.annotations = tuple(list_annotations)
#         # Fit curve according to parameters
#         fig["data"] = list(filter(lambda d: d["name"] == "Data", fig["data"]))
#         x_data = np.array(fig["data"][0]["x"])
#         y_data = np.array(fig["data"][0]["y"])

#         fitted_model, partial_fits = curve_fitting(
#             x_data, y_data, x_peaks, y_peaks, stddev, fwhm_g, fwhm_l, peak_shape
#         )
#         fig = go.Figure(fig)
#         if fitted_model is not None:
#             fitted_x_peaks, fitted_y_peaks, fitted_fwhms = get_fitting_params(
#                 fitted_model, peak_shape
#             )
#             # Populate fitting params
#             for indx, (fitted_x_peak, fitted_y_peak, fitted_fwhm) in enumerate(
#                 zip(fitted_x_peaks, fitted_y_peaks, fitted_fwhms)
#             ):
#                 table_data[indx]["fitted_peak_x"] = fitted_x_peak
#                 table_data[indx]["fitted_peak_y"] = fitted_y_peak
#                 table_data[indx]["fitted_fwhm"] = fitted_fwhm
#             # Plot fitted curves
#             fitted_data = fitted_model(x_data)
#             mse = np.mean((fitted_data - y_data) ** 2)
#             fig.add_trace(
#                 go.Scatter(
#                     x=x_data, y=fitted_data, name=f"Fitted curve, MSE: {mse:.4f}"
#                 )
#             )
#             for ii in range(len(partial_fits)):
#                 fig.add_trace(
#                     go.Scatter(
#                         x=x_data,
#                         y=partial_fits[ii](x_data),
#                         name=f"Partial fit {x_peaks[ii]:.2f}",
#                         line=dict(dash="dash"),
#                     )
#                 )
#         else:
#             # If the model was not fitted properly, open warning
#             open_modal = True
#     else:
#         fig = dash.no_update
#     return table_data, fig, open_modal


@callback(Output("peak-table", "hidden_columns"), Input("peak-shape", "value"))
def hide_columns(peak_shape):
    if peak_shape == "gaussian":
        return ["fwhm-l", "fwhm-g"]
    else:
        return ["stddev"]

import json
import os

from dash import Input, Output, callback, no_update
from dotenv import load_dotenv
from tiled.client import from_uri

load_dotenv()

# Initialize the Tiled server
TILED_API_KEY = os.getenv("TILED_API_KEY")


def extract_info_from_reduction(reduction_update):
    reduction_update = json.loads(reduction_update["data"])
    if "reduction_uri" in reduction_update:
        reduction_uri = reduction_update["reduction_uri"]
        reduction_metadata = from_uri(reduction_uri, api_key=TILED_API_KEY).metadata
        # Get feature from the meta data
        max_intensity = reduction_metadata["max_intensity"]
        max_intensity_q = reduction_metadata["max_intensity_q"]
        # Get motor positions from the input_uri
        input_uri = reduction_metadata["input_uri"]
        input_metadata = from_uri(input_uri).metadata
        x = input_metadata["Sample X Stage"]
        y = input_metadata["Sample Y Stage"]
        return reduction_uri, input_uri, x, y, max_intensity, max_intensity_q
    return [None] * 6


@callback(
    Output("reduction_update_message", "children"),
    Input("ws-reduction-update", "message"),
    prevent_initial_call=True,
)
def update_reduction_view(
    reduction_update,
):
    if reduction_update is None:
        return no_update
    (
        reduction_uri,
        input_uri,
        x,
        y,
        max_intensity,
        max_intensity_q,
    ) = extract_info_from_reduction(reduction_update)
    message = (
        f"Received message about data at {x}, {y} with"
        + f" {max_intensity} at {max_intensity_q}."
    )
    return message

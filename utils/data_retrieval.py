import os

from dotenv import load_dotenv
from tiled.client import from_uri
from tiled.client.array import ArrayClient
from tiled.client.container import Container
from tiled.utils import path_from_uri

# from tiled.client.cache import Cache

load_dotenv()

# Initialize the Tiled server
TILED_URI = os.getenv("TILED_URI")
TILED_API_KEY = os.getenv("TILED_API_KEY")

if TILED_URI is None or TILED_API_KEY is None:
    raise ValueError("TILED_URI and TILED_API_KEY must be set in the .env file")

try:
    client = from_uri(TILED_URI, api_key=TILED_API_KEY)
    TILED_BASE_URI = client.uri
except Exception as e:
    error_message = f"Error connecting to Tiled server: {e}"
    raise ValueError(error_message)


def trim_base_from_uri(uri_to_trim):
    """
    Trim the base Tiled uri from a full uri pointing to a dataset
    """
    return uri_to_trim.replace(TILED_BASE_URI, "")


def get_processed_experiment_names():
    try:
        client = from_uri(TILED_URI, api_key=TILED_API_KEY)
        processed_list_of_experiments = client["processed"].keys()
        list_of_experiments = [
            experiment for experiment in processed_list_of_experiments
        ]
        return list_of_experiments
    except Exception as e:
        error_message = f"Error retrieving experiment names: {e}"
        print(error_message)
        return []


def get_csv_file_uri(experiment_name):
    try:
        client = from_uri(TILED_URI, api_key=TILED_API_KEY)
        processed_experiment_uri = client["processed"][experiment_name].uri
        get_csv_file_uri = processed_experiment_uri + f"/{experiment_name}"
        return get_csv_file_uri
    except Exception as e:
        error_message = f"Error retrieving csv file uri: {e}"
        print(error_message)
        return None


def tiled_read_csv(csv_file_uri):
    try:
        client = from_uri(csv_file_uri, api_key=TILED_API_KEY)
        csv_data = client.read()
        return csv_data
    except Exception as e:
        error_message = f"Error retrieving csv file: {e}"
        print(error_message)
        return None


def write_csv_from_interface(experiment_name, data):
    try:
        # TODO: optimize this with a get_csv_file_uri function later
        client = from_uri(TILED_URI, api_key=TILED_API_KEY, include_data_sources=True)
        container_client = client["processed"][experiment_name]
        csv_client = container_client[experiment_name]
        csv_file_local_uri = path_from_uri(
            csv_client.data_sources()[0]["assets"][0]["data_uri"]
        )
        data.to_csv(csv_file_local_uri, index=False)
    except Exception as e:
        error_message = f"Error writing to csv file: {e}"
        print(error_message)
        return None




def get_scan_data(trimmed_scan_uri, index=0, downsample_factor=1):
    """
    Returns the data corresponding to the trimmed scan uri
    """
    scan = from_uri(TILED_BASE_URI + trimmed_scan_uri, api_key=TILED_API_KEY)
    if len(scan.shape) == 2:
        return scan[::downsample_factor, ::downsample_factor]
    else:
        return scan[index, ::downsample_factor, ::downsample_factor]


def get_mask_data(trimmed_mask_uri, scan_height, scan_width, downsample_factor=1):
    """
    Returns the data corresponding to the trimmed mask uri
    """
    mask = from_uri(TILED_BASE_URI + trimmed_mask_uri, api_key=TILED_API_KEY)
    if mask.shape[0] == scan_height and mask.shape[1] == scan_width:
        return mask[::downsample_factor, ::downsample_factor]
    else:
        print("Mask dimensions and scan dimensions don't match.")
        return None


def get_reduction_data(trimmed_reduction_uri):
    reduction_client = from_uri(
        TILED_BASE_URI + trimmed_reduction_uri, api_key=TILED_API_KEY
    )

    output_unit = reduction_client.metadata["output_unit"]

    if "intensity" not in reduction_client.keys():
        print("Reduced data is missing 'intensity'.")
        return None
    if output_unit not in reduction_client.keys():
        print(f"Reduced data is missing '{output_unit}'.")
        return None

    x_data = reduction_client[output_unit][:]
    y_data = reduction_client["intensity"][:]

    return x_data, y_data, output_unit

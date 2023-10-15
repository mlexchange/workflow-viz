import os

import numpy as np
from dotenv import load_dotenv
from tiled.client import from_uri

# from tiled.client.cache import Cache

load_dotenv()

# Initialize the Tiled server
TILED_URI = os.getenv("TILED_URI")
TILED_API_KEY = os.getenv("TILED_API_KEY")

client = from_uri(TILED_URI, api_key=TILED_API_KEY)
TILED_BASE_URI = client.uri


def trim_base_from_uri(uri_to_trim):
    """
    Trim the base Tiled uri from a full uri pointing to a dataset
    """
    return uri_to_trim.replace(TILED_BASE_URI, "")


def get_scan_options():
    """
    Returns a list of trimmed Tiled Uris for scans
    """
    # Currently very DESY specific, looking for lmbdp03 and embl_2m
    # and inside of 'raw"
    scan_uri_map = dict()
    raw_client = client["raw"]

    for node_name in raw_client.keys():
        node_client = raw_client[node_name]
        for key in node_client:
            if key == "lmbdp03" or key == "embl_2m":
                detector_client = node_client[key]
                for key in detector_client.keys():
                    scan_uri = trim_base_from_uri(detector_client[key].uri)
                    trimmed_mask_name = scan_uri.replace("raw/", "")
                    scan_uri_map[trimmed_mask_name] = scan_uri

    return scan_uri_map


def get_scan_data(trimmed_scan_uri, index=0, downsample_factor=1):
    """
    Returns the data corresponding to the trimmed scan uri
    """
    scan = from_uri(TILED_BASE_URI + trimmed_scan_uri, api_key=TILED_API_KEY)
    if len(scan.shape) == 2:
        return scan[::downsample_factor, ::downsample_factor]
    else:
        return scan[index, ::downsample_factor, ::downsample_factor]


def get_mask_options():
    """
    Returns a list of trimmed Tiled Uris in the mask node
    """
    # Here we are still assuming all masks are in one folder,
    # if that is the case, the logic here would not yet be needed,
    # but they may not be in the future
    raw_client = client["raw"]
    masks = raw_client["masks"]
    mask_uri_mapper = dict()
    for mask_name in masks.keys():
        mask_uri = trim_base_from_uri(masks[mask_name].uri)
        trimmed_mask_name = mask_uri.replace("raw/masks/", "")
        mask_uri_mapper[trimmed_mask_name] = mask_uri
    return mask_uri_mapper


def get_mask_data(trimmed_mask_uri, scan_height, scan_width, downsample_factor=1):
    """
    Returns the data corresponding to the trimmed mask uri
    """
    mask = from_uri(TILED_BASE_URI + trimmed_mask_uri, api_key=TILED_API_KEY)
    if mask.shape[0] == scan_height and mask.shape[1] == scan_width:
        return mask[::downsample_factor, ::downsample_factor]
    # Rotated?
    elif mask.shape[0] == scan_width and mask.shape[1] == scan_height:
        return np.rot90(mask[::downsample_factor, ::downsample_factor])
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

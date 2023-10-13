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
    scan_uris = []
    raw_client = client["raw"]
    for node_name in raw_client.keys():
        node = raw_client[node_name]
        if "lmbdp03" in node.keys() or "embl_2m" in node.keys():
            trimmed_uri = trim_base_from_uri(node.uri)
            trimmed_uri = trimmed_uri.replace("raw/", "")
            scan_uris.append(trimmed_uri)

    return scan_uris


def get_scan_data(trimmed_scan_uri, index=0):
    """
    Returns the data corresponding to the trimmed scan uri
    """
    raw_client = client["raw"]
    node = raw_client[trimmed_scan_uri]
    if "lmbdp03" in node.keys():
        node = node["lmbdp03"]
    elif "embl_2m" in node.keys():
        node = node["embl_2m"]
    scan = node.values()[0]
    if len(scan.shape) == 2:
        return scan[:]
    else:
        return scan[index]


def get_mask_options():
    """
    Returns a list of trimmed Tiled Uris in the mask node
    """
    # Here we are still assuming all masks are in one folder,
    # if that is the case, the logic here would not yet be needed,
    # but they may not be in the future
    raw_client = client["raw"]
    masks = raw_client["masks"]
    mask_uris = [trim_base_from_uri(masks[mask_name].uri) for mask_name in masks.keys()]
    return [mask_uri.replace("raw/masks/", "") for mask_uri in mask_uris]


def get_mask_data(trimmed_mask_uri, scan_height, scan_width):
    """
    Returns the data corresponding to the trimmed mask uri
    """
    masks = client["raw"]["masks"]
    mask = masks[trimmed_mask_uri]
    if mask.shape[0] == scan_height and mask.shape[1] == scan_width:
        return mask[:]
    # Rotated?
    elif mask.shape[0] == scan_width and mask.shape[1] == scan_height:
        return np.rot90(mask[:])
    else:
        print("Mask dimensions and scan dimensions don't match.")
        return None


def get_reduction_data(trimmed_reduction_uri, index=0):
    reduction_client = from_uri(
        TILED_BASE_URI + trimmed_reduction_uri, api_key=TILED_API_KEY
    )

    return reduction_client["chi"][:], reduction_client["intensity"][:]

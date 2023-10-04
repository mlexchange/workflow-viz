import os

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
    scan_uris = []
    for node_name in client.keys():
        node = client[node_name]
        if "lmbdp03" in node.keys() or "embl_2m" in node.keys():
            scan_uris.append(trim_base_from_uri(node.uri))

    return scan_uris


def get_scan_data(trimmed_scan_uri, index=0):
    """
    Returns the data corresponding to the trimmed scan uri
    """
    node = client[trimmed_scan_uri]
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
    masks = client["masks"]
    mask_uris = [trim_base_from_uri(masks[mask_name].uri) for mask_name in masks.keys()]
    return [mask_uri.replace("masks/", "") for mask_uri in mask_uris]


def get_mask_data(trimmed_mask_uri):
    """
    Returns the data corresponding to the trimmed mask uri
    """
    masks = client["masks"]
    return masks[trimmed_mask_uri][:]

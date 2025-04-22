import numpy as np
from tiled.adapters.array import ArrayAdapter
from tiled.structures.core import Spec
from tiled.utils import path_from_uri
from custom.edf import parse_txt_accompanying_edf
import pathlib
import os
import logging
from logging import StreamHandler
import fabio

logger = logging.getLogger("tiled.adapters.edf")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


def read(data_uri, structure=None, metadata=None, specs=None, access_policy=None):
    """Read a detector image saved as .gb produced at ALS beamline 7.3.3

    Parameters
    ----------
    data_uri: str
        Uri of the .edf file, typically a file:// uri.
    """
    filepath = path_from_uri(data_uri)
    pixels_x = 1475
    pixels_y = 1679
    data = np.fromfile(filepath, dtype="<f4")
    expected_size = pixels_x * pixels_y
    if data.size != expected_size:
        raise ValueError(
            f"Data size ({data.size}) does not match expected size ({expected_size})."
        )
    array = data.reshape((pixels_y, pixels_x))

    additional_edf_metadata = parse_edf_accompanying_gb(filepath)
    
    # Combine the metadata dictionaries - the following method combines the 
    # metadata dictionaries but there is a potential to overwrrite the values
    # for the same keys. If same keys are present in both dictionaries, then
    # an alternate method should be used to combine the dictionaries, similar to
    # the one used in the combine_edf_metadata_for_gb method.
    metadata = {**metadata, **additional_edf_metadata} if metadata else additional_edf_metadata

    return ArrayAdapter.from_array(array, metadata=metadata, specs=[Spec("gb")])

def combine_edf_metadata_for_gb(hi_dict, lo_dict):
    """Combine two dictionaries into one.

    Parameters
    ----------
    hi_dict: dict
        Dictionary containing metadata from the hi .edf file.
    lo_dict: dict
        Dictionary containing metadata from the lo .edf file
    """
    combined_dict = dict()

    # get all the unique keys from both dictionaries
    combined_keys = set(hi_dict.keys()).union(set(lo_dict.keys()))

    # check if the values match for the same key in both dictionaries
    for key in combined_keys:
        hi_val = hi_dict.get(key)
        lo_val = lo_dict.get(key)

        if hi_val == lo_val:
            # If values are the same, keep one entry
            combined_dict[key] = hi_val
        else:
            # If values are different, add both with distinct keys
            if hi_val is not None:
                combined_dict[f"{key}_hi"] = hi_val
            if lo_val is not None:
                combined_dict[f"{key}_lo"] = lo_val

    return combined_dict


def parse_edf_accompanying_gb(file_path):
    """Parse a .edf file produced at ALS beamline 7.3.3 into a dictionary.

    Parameters
    ----------
    file_path: str or pathlib.Path
        Filepath of the .edf file.
    """

    # Generate the hi edf file path
    edf_hi_filepath = None
    if isinstance(file_path, str):
        edf_hi_filepath = file_path.replace("sfloat_2m.gb", "hi_2m.edf")
    if isinstance(file_path, pathlib.Path):
        edf_hi_filepath = file_path.with_suffix(".edf")
        edf_hi_filepath = pathlib.Path(str(edf_hi_filepath).replace("sfloat", "hi"))

    # File does not exist, set the date as None - empty metadata dictionary is 
    # returned in the parse_txt_accompanying_edf method
    if not os.path.isfile(edf_hi_filepath):
        #edf_hi_metadata_dict = dict()
        hi_date = None
    else:
        hi_file = fabio.open(edf_hi_filepath)
        hi_header = hi_file.header
        hi_date = hi_header.get("Date")
    
    edf_hi_metadata_dict = parse_txt_accompanying_edf(edf_hi_filepath)
    
    # extract the header information and import the function for edf and read the metadata
    # take the metadata from both and if the same key is present in both, keep the values of both   
    # but index it with hi and lo

    edf_lo_filepath = None
    if isinstance(file_path, str):
        edf_lo_filepath = file_path.replace("sfloat_2m.gb", "lo_2m.edf")
    if isinstance(file_path, pathlib.Path):
        edf_lo_filepath = file_path.with_suffix(".edf")
        edf_lo_filepath = pathlib.Path(str(edf_lo_filepath).replace("sfloat", "lo"))

    # File does not exist, set the date as None - empty metadata dictionary is 
    # returned in the parse_txt_accompanying_edf method
    if not os.path.isfile(edf_lo_filepath):
        #edf_lo_metadata_dict = dict()
        lo_date = None
    else: 
        lo_file = fabio.open(edf_lo_filepath)
        lo_header = lo_file.header
        lo_date = lo_header.get("Date")
    
    edf_lo_metadata_dict = parse_txt_accompanying_edf(edf_lo_filepath)

    # Combine the metadata dictionaries
    gb_dictionary = combine_edf_metadata_for_gb(edf_hi_metadata_dict, edf_lo_metadata_dict)

    # Compare two dates and select the later one
    if hi_date is not None and lo_date is not None:
        gb_dictionary["Date"] = hi_date if hi_date > lo_date else lo_date
    else:
        gb_dictionary["Date"] = hi_date if hi_date is not None else lo_date

    return gb_dictionary


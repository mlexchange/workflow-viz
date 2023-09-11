import logging
import os
import pathlib

import fabio
from tiled.adapters.array import ArrayAdapter

logger = logging.getLogger("tiled.adapters.edf")


def parse_txt_accompanying_edf(filepath):
    """Pase a .txt file produced at ALS beamline 7.3.3 into a dictionary.

    Parameters
    ----------
    filepath: str or pathlib.Path
        Filepath of the .edf file.
    """
    txt_filepath = None
    if isinstance(filepath, str):
        txt_filepath = filepath.replace(".edf", ".txt")
    if isinstance(filepath, pathlib.Path):
        txt_filepath = filepath.with_suffix(".txt")

    if os.path.isfile(txt_filepath):
        # TODO: Fill meta data with
        print("Parsing txt")
        metadata = dict()
    return metadata


def parse_edf_header(header):
    """Parse header of an edf file and return a dictionary."""
    return None


def read(filepath, metadata=None, **kwargs):
    """Read a detector image saved as .edf produced at ALS beamline 7.3.3

    Parameters
    ----------
    filepath: str or pathlib.Path
        Filepath of the .edf file.
    """

    # Should we catch any read errors here?
    file = fabio.open(filepath)
    array = file.data

    if metadata is None:
        metadata = parse_edf_header(file.header)

    # If a .txt file with the same name exists
    # extract additional meta data from it
    # TODO: parse text file
    parse_txt_accompanying_edf(filepath)
    return ArrayAdapter.from_array(array, metadata=metadata)


async def walk_edf_with_txt(
    catalog,
    path,
    files,
    directories,
    settings,
):
    """
    Possible patters:
    1-1 txt-edf
    1 log, many edfs
    1 txt - 2 edf with _hi _lo
    """
    # TODO
    unhandled_files = files
    unhandled_directories = directories
    return unhandled_files, unhandled_directories

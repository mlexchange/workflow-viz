# import re
import logging
from logging import StreamHandler

import fabio
from tiled.adapters.array import ArrayAdapter
from tiled.structures.core import Spec
from tiled.utils import path_from_uri

logger = logging.getLogger("tiled.adapters.edf")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


def parse_fio_accompanying_cbf(filepath):
    """Parse the FIO accompanying CBF file and extract relevant information.

    Parameters
    ----------
    filepath: str or pathlib.Path
        Filepath of the .cbf file.
    """
    # Implement parsing logic here
    pass


def read(data_uri, structure=None, metadata=None, specs=None, access_policy=None):
    """Read a detector image saved as .cbf produced by a Pilatus detector.

    Parameters
    ----------
    filepath: str or pathlib.Path
        Filepath of the .cbf file.
    """
    filepath = path_from_uri(data_uri)
    file = fabio.open(filepath)
    array = file.data
    if metadata is None:
        metadata = file.header
    return ArrayAdapter.from_array(array, metadata=metadata, specs=[Spec("cbf")])

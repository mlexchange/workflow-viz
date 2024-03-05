# import re
import logging
from logging import StreamHandler

import fabio
from tiled.adapters.array import ArrayAdapter
from tiled.structures.core import Spec

logger = logging.getLogger("tiled.adapters.edf")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


def parse_cbf_header(header):
    """Parse relevant information from the header of a .cbf file.

    # 2023-06-20T20:12:29.036
    """
    # TODO
    # date_pattern = re.compile()


def read(filepath, metadata=None, **kwargs):
    """Read a detector image saved as .cbf produced by a Pilatus detector.

    Parameters
    ----------
    filepath: str or pathlib.Path
        Filepath of the .cbf file.
    """

    file = fabio.open(filepath)
    array = file.data
    if metadata is None:
        metadata = parse_cbf_header(file.header)
    # return ArrayAdapter.from_array(array, metadata=metadata, **kwargs)
    return ArrayAdapter.from_array(array, metadata=metadata, specs=[Spec("cbf")])

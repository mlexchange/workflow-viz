import numpy as np
from tiled.adapters.array import ArrayAdapter
from tiled.structures.core import Spec
from tiled.utils import path_from_uri


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

    return ArrayAdapter.from_array(array, metadata=metadata, specs=[Spec("gb")])

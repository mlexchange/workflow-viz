import collections
import logging
import os
import re
from logging import StreamHandler

import h5py
import numpy as np
from tiled.adapters.array import ArrayAdapter
from tiled.client.register import create_node_or_drop_collision, dict_or_none
from tiled.server.schemas import Asset, DataSource, Management
from tiled.utils import ensure_uri

logger = logging.getLogger("tiled.adapters.lambda_nxs")
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

# Matches filename with (optional) non-digits \D followed by digits \d _m,
# then digits \d and then the file extension .nxs
NEXUS_SEQUENCE_STEM_PATTERN = re.compile(r"^(.*)_(\d*)_m(\d{2})\.nxs$")


async def walk(
    catalog,
    path,
    files,
    directories,
    settings,
):
    """
    Group NeXus files in the given directory as a group if they come from a lambda
    detector.

    We are looking for a total of 11 files:
    - with file extension .nxs
    - with file name ending in a number
    - inside of a folder named lmbdp03

    The lmbdp03 folder is inside a folder named by the sample (e.g x).
    The individiual files are called
    /../x/lmbdp03/x_00001_mxx

    We group these filed into sorted groups and make one Node for each.
    A group may have one or more items.
    """
    unhandled_directories = directories
    unhandled_files = []
    sequences = collections.defaultdict(list)
    for file in files:
        if file.is_file():
            match = NEXUS_SEQUENCE_STEM_PATTERN.match(file.name)
            if match:
                sequence_name, _, _sequence_number = match.groups()
                sequences[sequence_name].append(file)
                continue
        unhandled_files.append(file)
    mimetype = "multipart/related;type=application/x-hdf5"
    for name, sequence in sorted(sequences.items()):
        # Skip sequences that do not have exactly 11 files
        # corresponding to the 11 modules of the detector
        if len(sequence) != 11:
            logger.info(
                "    SKIPPED: Did not group %d Nexus files into a sequence '%s' since"
                + " the number of files does not match a lambda detector.",
                len(sequence),
                name,
            )
            unhandled_files.extend(sequence)
            continue
        dataset_path = "entry/instrument/detector/data"
        # Open one file and check if there is any data
        module = h5py.File(os.path.join(sequence[0]), "r")
        if len(module.get(dataset_path)) < 1:
            logger.info(
                "    SKIPPED: Did not group %d Nexus files into a sequence '%s' since"
                + " they do not contain any data.",
                len(sequence),
                name,
            )
            unhandled_files.extend(sequence)
            continue
        logger.info(
            "    Grouped %d Nexus files into a sequence '%s'", len(sequence), name
        )
        adapter_class = settings.adapters_by_mimetype[mimetype]
        key = settings.key_from_filename(name)
        try:
            adapter = adapter_class(*sequence)
        except Exception:
            logger.exception("    SKIPPED: Error constructing adapter for '%s'", name)
            return
        await create_node_or_drop_collision(
            catalog,
            key=key,
            structure_family=adapter.structure_family,
            metadata=dict(adapter.metadata()),
            specs=adapter.specs,
            data_sources=[
                DataSource(
                    mimetype=mimetype,
                    structure=dict_or_none(adapter.structure()),
                    parameters={},
                    management=Management.external,
                    assets=[
                        Asset(
                            data_uri=str(ensure_uri(str(item.absolute()))),
                            is_directory=False,
                        )
                        for item in sorted(sequence)
                    ],
                )
            ],
        )
    return unhandled_files, unhandled_directories


def read_sequence(*filepaths, metadata=None, **kwargs):
    # Stitch everything together
    num_modules = len(filepaths)
    dataset_path = "entry/instrument/detector/data"
    ff_path = "entry/instrument/detector/flatfield"
    # mask_path = "entry/instrument/detector/pixel_mask"
    trans_path = "entry/instrument/detector/translation/distance"
    size_x = 0
    size_y = 0
    lmbd_x = 516
    lmbd_y = 1556
    trans_set = {}
    dataset = [0]
    ff = [1]
    mask = [1]

    for md in range(0, num_modules):
        module_set = h5py.File(os.path.join(filepaths[md]), "r")
        trans_set[md] = []
        trans_set[md].append(list(module_set.get(trans_path))[1])  # reverse x and y
        trans_set[md].append(list(module_set.get(trans_path))[0])
        pos_x = lmbd_x + trans_set[md][0]
        pos_y = lmbd_y + trans_set[md][1]
        size_x = (
            int(pos_x) if pos_x > size_x else int(size_x)
        )  # reform if module increase size
        size_y = int(pos_y) if pos_y > size_y else int(size_y)
        dataset.append(md)
        sequence_nr = 0
        dataset[md] = np.array(
            module_set.get(dataset_path)[sequence_nr], dtype=np.float32
        )
        ff.append(md)
        ff[md] = 1
        ff[md] = np.array(module_set.get(ff_path)[0], dtype=np.float32)
        mask.append(md)
        mask[md] = 1
        # For now ignore the mask
        # mask[md] = np.array(module_set.get(mask_path)[0], dtype=numpy.float32)
        # mask[md] = np.where(mask[md] > 2147483600, 0, mask[md])
        # mask[md] = np.where(mask[md] == 0, 1, numpy.nan)
        module_set.close()
        dataset[md] *= ff[md] * mask[md]

    myimage = np.empty((size_x, size_y), dtype=np.float32)
    myimage[:] = -1.0

    for md in range(0, num_modules):
        trans_x = int(trans_set[md][0])
        trans_y = int(trans_set[md][1])
        myimage[trans_x : trans_x + lmbd_x, trans_y : trans_y + lmbd_y] = np.array(
            dataset[md], dtype=np.float32
        )

    array = myimage

    return ArrayAdapter.from_array(array, metadata=metadata)

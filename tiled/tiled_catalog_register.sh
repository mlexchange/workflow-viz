#!/bin/sh
source .env
echo $PWD
export PYTHONPATH="$PYTHONPATH:$PWD/tiled/config/"
echo $PATH_TO_DATA_CATALOG
if [ ! -f "$PATH_TO_DATA_CATALOG" ]; then
    tiled catalog init "$PATH_TO_DATA_CATALOG"
fi
if [ -d "$PATH_TO_DATA_ALS" ]; then
     tiled catalog register $PATH_TO_DATA_CATALOG --verbose \
          --ext '.edf=application/x-edf' \
          --adapter 'application/x-edf=custom.edf:read' \
          "$PATH_TO_DATA_ALS"
else
    echo "The directory $PATH_TO_DATA_ALS does not exist."
fi
if [ -d "$PATH_TO_DATA_DESY" ]; then
     tiled catalog register $PATH_TO_DATA_CATALOG --verbose \
          --ext '.cbf=application/x-cbf' \
          --adapter 'application/x-cbf=custom.cbf:read' \
          --walker 'custom.lambda_nxs:walk' \
          --adapter 'multipart/related;type=application/x-hdf5=custom.lambda_nxs:read_sequence' \
          "$PATH_TO_DATA_DESY"
else
    echo "The directory $PATH_TO_DATA_DESY does not exist."
fi
    
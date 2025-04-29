#!/bin/bash
source .env
echo "Executing Folder: $PWD"
export PYTHONPATH="$PYTHONPATH:$PWD/tiled/config/"
echo "Python Path: $PYTHONPATH"
echo "Data catalog for raw data: $PATH_TO_RAW_DATA_CATALOG"
echo "Data catalog for processed data: $PATH_TO_PROCESSED_DATA_CATALOG"

# Should no longer be needed since tiled serve comes first
if [[ ! -f "$PATH_TO_PROCESSED_DATA_CATALOG" ]]; then
    tiled catalog init $PATH_TO_PROCESSED_DATA_CATALOG
fi

if [ -d "$PATH_TO_PROCESSED_DATA" ]; then
     tiled register $TILED_URI --verbose \
            --api-key $TILED_API_KEY \
            --prefix "/processed" \
            "$PATH_TO_PROCESSED_DATA"
else
    echo "The directory for processed data ($PATH_TO_PROCESSED_DATA) does not exist."
fi

# Should no longer be needed since tiled serve comes first
if [[ ! -f "$PATH_TO_RAW_DATA_CATALOG" ]]; then
    tiled catalog init $PATH_TO_RAW_DATA_CATALOG
fi

## Will overwrite
if [ -d "$PATH_TO_RAW_DATA" ]; then
     tiled register $TILED_URI --verbose \
            --api-key $TILED_API_KEY \
            --prefix "/raw" \
            --ext '.cbf=application/x-cbf' \
            --adapter 'application/x-cbf=custom.cbf:read' \
            --ext '.edf=application/x-edf' \
            --adapter 'application/x-edf=custom.edf:read' \
            --ext '.gb=application/x-gb' \
            --adapter 'application/x-gb=custom.gb:read' \
            --walker 'custom.blacklist:walk' \
            --walker 'custom.whitelist:walk' \
            --walker 'custom.lambda_nxs:walk' \
            --adapter 'multipart/related;type=application/x-hdf5=custom.lambda_nxs:read_sequence' \
            "$PATH_TO_RAW_DATA"
else
    echo "The directory for raw data ($PATH_TO_RAW_DATA) does not exist."
fi
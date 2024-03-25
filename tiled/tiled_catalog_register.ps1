# equivalent to "source .env"
./set_env.ps1
Write-Host "Executing Folder: $PWD" 
set $Env:PYTHONPATH="$Env:PYTHONPATH;$PWD/tiled/config/"
Write-Host "PythonPath: $Env:PYTHONPATH"
Write-Host "Data catalog for raw data: $Env:PATH_TO_RAW_DATA_CATALOG"
Write-Host "Data catalog for processed data: $Env:PATH_TO_PROCESSED_DATA_CATALOG"

# Should no longer be needed since tiled serve comes first
if (-not ([string]::IsNullOrWhiteSpace($Env:PATH_TO_DATA_CATALOG)) -and -not (Test-Path "$Env:PATH_TO_DATA_CATALOG")) {
    tiled catalog init "$Env:PATH_TO_DATA_CATALOG"
}

## Will overwrite
if (-not ([string]::IsNullOrWhiteSpace("$Env:PATH_TO_RAW_DATA")) -and (Test-Path "$Env:PATH_TO_RAW_DATA" -PathType Container)){
    tiled register $Env:TILED_URI --verbose `
    --prefix "/raw" `
    --ext '.edf=application/x-edf' `
    --adapter 'application/x-edf=custom.edf:read' `
    --ext '.cbf=application/x-cbf' `
    --adapter 'application/x-cbf=custom.cbf:read' `
    --walker 'custom.lambda_nxs:walk' `
    --adapter 'multipart/related;type=application/x-hdf5=custom.lambda_nxs:read_sequence' `
    "$Env:PATH_TO_RAW_DATA"
} else {
    Write-Host "The directory for raw data ($Env:PATH_TO_RAW_DATA) does not exist."
}
    
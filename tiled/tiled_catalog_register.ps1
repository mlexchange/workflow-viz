# equivalent to "source .env"
./set_env.ps1

Write-Host "Executing Folder: $PWD" 
set $Env:PYTHONPATH="$Env:PYTHONPATH;$PWD/tiled/config/"
Write-Host "PythonPath: $Env:PYTHONPATH"
Write-Host "Data catalog: $Env:PATH_TO_DATA_CATALOG"
if (-not ([string]::IsNullOrWhiteSpace($Env:PATH_TO_DATA_CATALOG)) -and -not (Test-Path "$Env:PATH_TO_DATA_CATALOG")) {
    tiled catalog init "$Env:PATH_TO_DATA_CATALOG"
}
if (-not ([string]::IsNullOrWhiteSpace("$Env:PATH_TO_DATA_ALS")) -and (Test-Path "$Env:PATH_TO_DATA_ALS" -PathType Container)){
    tiled catalog register $Env:PATH_TO_DATA_CATALOG --verbose `
    --prefix "/" `
    --ext '.edf=application/x-edf' `
    --adapter 'application/x-edf=custom.edf:read' `
    "$Env:PATH_TO_DATA_ALS"
} else {
    Write-Host "The directory for ALS ($Env:PATH_TO_DATA_ALS) does not exist."
}
## Will overwrite
if (-not ([string]::IsNullOrWhiteSpace("$Env:PATH_TO_DATA_DESY")) -and (Test-Path "$Env:PATH_TO_DATA_DESY" -PathType Container)){
    tiled catalog register $Env:PATH_TO_DATA_CATALOG --verbose `
    --prefix "/" `
    --ext '.cbf=application/x-cbf' `
    --adapter 'application/x-cbf=custom.cbf:read' `
    --walker 'custom.lambda_nxs:walk' `
    --adapter 'multipart/related;type=application/x-hdf5=custom.lambda_nxs:read_sequence' `
    --watch `
    "$Env:PATH_TO_DATA_DESY"
} else {
    Write-Host "The directory for DESY ($Env:PATH_TO_DATA_DESY) does not exist."
}
    
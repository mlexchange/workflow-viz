
$EnvFile = ".env"

if (Test-Path $EnvFile){
    Get-Content $EnvFile | ForEach-Object {
    # Match any line with KEY=value pattern that does not start with # (using negative lookahead)
        if ($_ -match "^(?!#)([^=]+)=(.+)") {
            $key = $matches[1]
            $value = $matches[2]
            Write-Host "Setting environment variable $key to $value"
            Set-Content "Env:$key" $value
        }
    }
}
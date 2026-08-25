param([string]$Python = "python")

$ErrorActionPreference = "Stop"
& $Python (Join-Path $PSScriptRoot "verify_release.py")
if ($LASTEXITCODE -ne 0) {
    throw "Release verification failed with exit code $LASTEXITCODE"
}

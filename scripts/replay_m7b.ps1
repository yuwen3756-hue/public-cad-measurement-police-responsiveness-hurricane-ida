param([string]$Python = "python")

$ErrorActionPreference = "Stop"
$packageRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$sourceSnapshot = Join-Path $packageRoot "reproduction\repository_snapshot"
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("beland_m7b_replay_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tempRoot | Out-Null
Copy-Item -LiteralPath $sourceSnapshot -Destination (Join-Path $tempRoot "repository_snapshot") -Recurse
$work = Join-Path $tempRoot "repository_snapshot"
$script = Join-Path $work "pilot_911_dv\experiments\nola_2020-01-01_2024-12-31_beland_plus_wave4r\candidate\m7b_same_estimator_reference_geometry\independent_replicate_m7b.py"

try {
    Push-Location $work
    try {
        & $Python $script
        if ($LASTEXITCODE -ne 0) {
            throw "M7B replay failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }
    Write-Output "M7B_REPLAY_PASS"
    Write-Output "Disposable replay retained at: $tempRoot"
} catch {
    Write-Output "Failed replay retained at: $tempRoot"
    throw
}

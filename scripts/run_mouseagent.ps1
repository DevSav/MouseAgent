$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "Starting MouseAgent from $repoRoot"
Start-Process -FilePath "python" -ArgumentList "-m", "mouseagent" -WorkingDirectory $repoRoot


$ErrorActionPreference = "Stop"

$matches = Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -in @("python.exe", "pythonw.exe") -and
        $_.CommandLine -match "(-m\s+mouseagent|mouseagent\\__main__\.py)"
    }

if (-not $matches) {
    Write-Host "MouseAgent is not running."
    exit 0
}

foreach ($process in $matches) {
    Write-Host "Stopping MouseAgent process $($process.ProcessId)"
    Stop-Process -Id $process.ProcessId -Force
}


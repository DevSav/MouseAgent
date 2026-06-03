$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$stopper = Join-Path $repoRoot "stop_mouseagent.cmd"

if (-not (Test-Path $stopper)) {
    throw "Could not find stopper: $stopper"
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Stop MouseAgent.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $stopper
$shortcut.WorkingDirectory = $repoRoot
$shortcut.Description = "Stop MouseAgent"
$shortcut.Hotkey = "CTRL+ALT+Q"
$shortcut.Save()

Write-Host "Created shortcut: $shortcutPath"
Write-Host "Keyboard shortcut: Ctrl+Alt+Q"


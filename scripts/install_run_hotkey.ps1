$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$launcher = Join-Path $repoRoot "run_mouseagent.cmd"

if (-not (Test-Path $launcher)) {
    throw "Could not find launcher: $launcher"
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "MouseAgent.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $launcher
$shortcut.WorkingDirectory = $repoRoot
$shortcut.Description = "Start MouseAgent"
$shortcut.Hotkey = "CTRL+ALT+M"
$shortcut.Save()

Write-Host "Created shortcut: $shortcutPath"
Write-Host "Keyboard shortcut: Ctrl+Alt+M"


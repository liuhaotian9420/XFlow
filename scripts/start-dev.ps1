param(
    [ValidateSet("demo", "real")]
    [string]$Mode = "demo",
    [string]$ApiBaseUrl = "http://127.0.0.1:8000",
    [int]$FrontendPort = 8501,
    [switch]$NoReload,
    [switch]$SkipSync
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "launch-common.ps1")

Write-Host "start-dev.ps1 is deprecated. Use start-demo.ps1 or start-real.ps1."

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$scriptPath = if ($Mode -eq "real") {
    Join-Path $PSScriptRoot "start-real.ps1"
} else {
    Join-Path $PSScriptRoot "start-demo.ps1"
}
$shellCommand = Get-LauncherShellCommand

$args = @("-ApiBaseUrl", $ApiBaseUrl, "-FrontendPort", $FrontendPort)
if ($NoReload.IsPresent) {
    $args += "-NoReload"
}
if ($SkipSync.IsPresent) {
    $args += "-SkipSync"
}

& $shellCommand -ExecutionPolicy Bypass -File $scriptPath @args

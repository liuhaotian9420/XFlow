param(
    [ValidateSet("demo", "real")]
    [string]$Mode = "demo",
    [string]$ApiBaseUrl = "http://127.0.0.1:8000",
    [switch]$NoReload,
    [switch]$SkipSync
)

$ErrorActionPreference = "Stop"

Write-Host "start-dev.ps1 is deprecated. Use start-demo.ps1 or start-real.ps1."

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$scriptPath = if ($Mode -eq "real") {
    Join-Path $PSScriptRoot "start-real.ps1"
} else {
    Join-Path $PSScriptRoot "start-demo.ps1"
}

$args = @("-ApiBaseUrl", $ApiBaseUrl)
if ($NoReload.IsPresent) {
    $args += "-NoReload"
}
if ($SkipSync.IsPresent) {
    $args += "-SkipSync"
}

& powershell -ExecutionPolicy Bypass -File $scriptPath @args

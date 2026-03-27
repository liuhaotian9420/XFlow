param(
    [string]$ApiBaseUrl = "http://127.0.0.1:8000",
    [int]$FrontendPort = 8501,
    [switch]$NoReload,
    [switch]$SkipSync
)

$ErrorActionPreference = "Stop"

. (Join-Path $PSScriptRoot "launch-common.ps1")

function Invoke-RequiredToolCheck {
    $pythonVersion = Assert-MinimumVersion -Name "python" -MinimumVersion ([Version]"3.12.0") -InstallHint "Install Python 3.12+ first."
    Install-UvIfMissing | Out-Null
    $uvVersion = Assert-MinimumVersion -Name "uv" -MinimumVersion ([Version]"0.4.0") -InstallHint "Install uv first."
    Write-Host "[ok] python $pythonVersion"
    Write-Host "[ok] uv $uvVersion"
}

function Invoke-UvSyncIfNeeded {
    param(
        [string]$ProjectRoot,
        [bool]$Skip
    )
    if ($Skip) {
        Write-Host "[skip] uv sync"
        return
    }
    Write-Host "[step] uv sync"
    & uv sync
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed. Check network access or dependency resolution and retry."
    }
}

function Start-WindowProcess {
    param(
        [string]$ProjectRoot,
        [string]$ApiBaseUrl,
        [string]$ShellCommand,
        [string]$BackendHost,
        [int]$BackendPort,
        [int]$FrontendPort,
        [bool]$Reload,
        [string]$Target
    )

    $reloadFlag = ""
    if ($Reload) {
        $reloadFlag = " --reload"
    }

    if ($Target -eq "backend") {
        $command = @"
Set-Location '$ProjectRoot'
`$env:APP_MODE='real'
`$env:API_BASE_URL='$ApiBaseUrl'
uv run python scripts/run_uvicorn_windows.py --host '$BackendHost' --port $BackendPort$reloadFlag
"@
    } else {
        $command = @"
Set-Location '$ProjectRoot'
`$env:APP_MODE='real'
`$env:API_BASE_URL='$ApiBaseUrl'
uv run streamlit run app/streamlit_app.py --server.port $FrontendPort
"@
    }

    Start-Process $ShellCommand -ArgumentList "-NoExit", "-Command", $command | Out-Null
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$reload = -not $NoReload.IsPresent
$apiEndpoint = Resolve-ApiEndpoint -ApiBaseUrl $ApiBaseUrl
$shellCommand = Get-LauncherShellCommand

Write-Host "xyf-competition-mvp real launcher"
Write-Host "project root: $projectRoot"
Write-Host "mode: real"
Write-Host "api base url: $ApiBaseUrl"
Write-Host "launcher shell: $shellCommand"
Write-Host "frontend port: $FrontendPort"

Set-Location $projectRoot
Invoke-RequiredToolCheck
Initialize-EnvFile -ProjectRoot $projectRoot -RequireRealSettings $true | Out-Null
Assert-PortAvailable -Port $apiEndpoint.Port -Label "Backend"
Assert-PortAvailable -Port $FrontendPort -Label "Frontend"

Invoke-UvSyncIfNeeded -ProjectRoot $projectRoot -Skip $SkipSync.IsPresent

Write-Host "[step] preflight"
& uv run python scripts/preflight.py --mode real
if ($LASTEXITCODE -ne 0) {
    throw "Preflight failed. Fix the reported Codex or ODPS configuration before retrying."
}

Start-WindowProcess -ProjectRoot $projectRoot -ApiBaseUrl $ApiBaseUrl -ShellCommand $shellCommand -BackendHost $apiEndpoint.Host -BackendPort $apiEndpoint.Port -FrontendPort $FrontendPort -Reload $reload -Target "backend"
Start-WindowProcess -ProjectRoot $projectRoot -ApiBaseUrl $ApiBaseUrl -ShellCommand $shellCommand -BackendHost $apiEndpoint.Host -BackendPort $apiEndpoint.Port -FrontendPort $FrontendPort -Reload $reload -Target "frontend"

Write-Host "Launched real mode."
Write-Host "Backend:  $ApiBaseUrl"
Write-Host "Frontend: http://localhost:$FrontendPort"

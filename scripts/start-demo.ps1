param(
    [string]$ApiBaseUrl = "http://127.0.0.1:8000",
    [switch]$NoReload,
    [switch]$SkipSync
)

$ErrorActionPreference = "Stop"

function Test-CommandExists {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-RequiredToolCheck {
    if (-not (Test-CommandExists "python")) {
        throw "Python is not installed or not on PATH. Install Python 3.12+ first."
    }
    if (-not (Test-CommandExists "uv")) {
        throw "uv is not installed or not on PATH. Install uv first."
    }
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
        [string]$AppMode,
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
`$env:APP_MODE='$AppMode'
`$env:API_BASE_URL='$ApiBaseUrl'
uv run python scripts/run_uvicorn_windows.py$reloadFlag
"@
    } else {
        $command = @"
Set-Location '$ProjectRoot'
`$env:APP_MODE='$AppMode'
`$env:API_BASE_URL='$ApiBaseUrl'
uv run streamlit run app/streamlit_app.py
"@
    }

    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command | Out-Null
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$reload = -not $NoReload.IsPresent

Write-Host "xyf-competition-mvp demo launcher"
Write-Host "project root: $projectRoot"
Write-Host "mode: demo"
Write-Host "api base url: $ApiBaseUrl"

Set-Location $projectRoot
Invoke-RequiredToolCheck
Invoke-UvSyncIfNeeded -ProjectRoot $projectRoot -Skip $SkipSync.IsPresent

Start-WindowProcess -ProjectRoot $projectRoot -ApiBaseUrl $ApiBaseUrl -AppMode "mock" -Reload $reload -Target "backend"
Start-WindowProcess -ProjectRoot $projectRoot -ApiBaseUrl $ApiBaseUrl -AppMode "mock" -Reload $reload -Target "frontend"

Write-Host "Launched demo mode."
Write-Host "Backend:  $ApiBaseUrl"
Write-Host "Frontend: http://localhost:8501"

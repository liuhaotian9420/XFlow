param(
    [string]$ApiBaseUrl = "http://127.0.0.1:8000",
    [string]$CodexMock = "true",
    [string]$CodexModel = "",
    [string]$CodexReasoningEffort = ""
)

$ErrorActionPreference = "Stop"

Write-Host "Starting xyf-competition-mvp dev stack..."
Write-Host "API_BASE_URL=$ApiBaseUrl"
Write-Host "CODEX_MOCK=$CodexMock"
if ($CodexModel) { Write-Host "CODEX_MODEL=$CodexModel" }
if ($CodexReasoningEffort) { Write-Host "CODEX_REASONING_EFFORT=$CodexReasoningEffort" }

$env:CODEX_MOCK = $CodexMock
$env:API_BASE_URL = $ApiBaseUrl
if ($CodexModel) { $env:CODEX_MODEL = $CodexModel }
if ($CodexReasoningEffort) { $env:CODEX_REASONING_EFFORT = $CodexReasoningEffort }

$projectRoot = (Get-Location).Path

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
Set-Location '$projectRoot'; `$env:CODEX_MOCK='$CodexMock'; `$env:API_BASE_URL='$ApiBaseUrl'; `$env:CODEX_MODEL='$CodexModel'; `$env:CODEX_REASONING_EFFORT='$CodexReasoningEffort'; uv run uvicorn backend.main:app --reload --loop backend.loop_factory:proactor_loop_factory
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
Set-Location '$projectRoot'; `$env:CODEX_MOCK='$CodexMock'; `$env:API_BASE_URL='$ApiBaseUrl'; `$env:CODEX_MODEL='$CodexModel'; `$env:CODEX_REASONING_EFFORT='$CodexReasoningEffort'; uv run streamlit run app/streamlit_app.py
"@

Write-Host "Backend and Streamlit launched in separate terminals."

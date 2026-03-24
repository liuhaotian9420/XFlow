param(
    [string]$ApiBaseUrl = "http://127.0.0.1:8000",
    [string]$CodexMock = "true"
)

$ErrorActionPreference = "Stop"

Write-Host "Starting xyf-competition-mvp dev stack..."
Write-Host "API_BASE_URL=$ApiBaseUrl"
Write-Host "CODEX_MOCK=$CodexMock"

$env:CODEX_MOCK = $CodexMock
$env:API_BASE_URL = $ApiBaseUrl

$projectRoot = (Get-Location).Path

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
Set-Location '$projectRoot'; `$env:CODEX_MOCK='$CodexMock'; `$env:API_BASE_URL='$ApiBaseUrl'; uv run uvicorn backend.main:app --reload
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
Set-Location '$projectRoot'; `$env:CODEX_MOCK='$CodexMock'; `$env:API_BASE_URL='$ApiBaseUrl'; uv run streamlit run app/streamlit_app.py
"@

Write-Host "Backend and Streamlit launched in separate terminals."

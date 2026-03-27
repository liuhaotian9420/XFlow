function Test-CommandExists {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-LauncherShellCommand {
    foreach ($candidate in @("pwsh", "powershell")) {
        if (Test-CommandExists $candidate) {
            return $candidate
        }
    }
    throw "Neither pwsh nor powershell is available on PATH."
}

function Get-CommandVersion {
    param(
        [string]$Name,
        [string[]]$VersionArguments = @("--version")
    )

    $output = & $Name @VersionArguments 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to read version from '$Name'."
    }
    if ($output -match "(\d+\.\d+(?:\.\d+)?)") {
        return [Version]$matches[1]
    }
    throw "Could not parse version from '$Name' output: $output"
}

function Assert-MinimumVersion {
    param(
        [string]$Name,
        [Version]$MinimumVersion,
        [string[]]$VersionArguments = @("--version"),
        [string]$InstallHint
    )

    if (-not (Test-CommandExists $Name)) {
        throw "$Name is not installed or not on PATH. $InstallHint"
    }

    $currentVersion = Get-CommandVersion -Name $Name -VersionArguments $VersionArguments
    if ($currentVersion -lt $MinimumVersion) {
        throw "$Name $currentVersion found, but $MinimumVersion or newer is required. $InstallHint"
    }

    return $currentVersion
}

function Install-UvIfMissing {
    if (Test-CommandExists "uv") {
        return $false
    }

    Write-Host "[step] uv not found, attempting automatic install"

    try {
        & python -m pip --version *> $null
        $pipReady = $LASTEXITCODE -eq 0
    } catch {
        $pipReady = $false
    }

    if (-not $pipReady) {
        Write-Host "[step] bootstrapping pip with ensurepip"
        & python -m ensurepip --upgrade
        if ($LASTEXITCODE -ne 0) {
            throw "uv is not installed and pip bootstrap failed. Install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
        }
    }

    & python -m pip install --upgrade uv
    if ($LASTEXITCODE -ne 0) {
        throw "Automatic uv install failed. Install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
    }

    $pythonDir = Split-Path ((Get-Command python).Source) -Parent
    $userScriptDir = Join-Path $env:APPDATA "Python\Scripts"
    foreach ($candidate in @($pythonDir, $userScriptDir)) {
        if ($candidate -and (Test-Path $candidate) -and ($env:PATH -notlike "*$candidate*")) {
            $env:PATH = "$candidate;$env:PATH"
        }
    }

    if (-not (Test-CommandExists "uv")) {
        throw "uv was installed but is still not on PATH for this session. Reopen the terminal or install uv manually."
    }

    Write-Host "[ok] uv installed automatically"
    return $true
}

function Initialize-EnvFile {
    param(
        [string]$ProjectRoot,
        [bool]$RequireRealSettings
    )

    $envFile = Join-Path $ProjectRoot ".env"
    if (Test-Path $envFile) {
        return $false
    }

    $envExample = Join-Path $ProjectRoot ".env.example"
    if (-not (Test-Path $envExample)) {
        throw ".env is missing and .env.example was not found."
    }

    Copy-Item $envExample $envFile
    Write-Host "[init] Created .env from .env.example"

    if ($RequireRealSettings) {
        throw ".env was initialized from .env.example. Fill in CODEX_* and ODPS_* settings, then retry."
    }

    return $true
}

function Resolve-ApiEndpoint {
    param([string]$ApiBaseUrl)

    $uri = $null
    if (-not [Uri]::TryCreate($ApiBaseUrl, [UriKind]::Absolute, [ref]$uri)) {
        throw "ApiBaseUrl must be an absolute URL, for example http://127.0.0.1:8000."
    }
    if ($uri.Scheme -notin @("http", "https")) {
        throw "ApiBaseUrl must use http or https."
    }

    return [pscustomobject]@{
        Uri  = $uri
        Host = $uri.Host
        Port = $uri.Port
    }
}

function Test-LocalPortAvailable {
    param([int]$Port)

    $listener = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
        $listener.Start()
        return $true
    } catch {
        return $false
    } finally {
        if ($null -ne $listener) {
            $listener.Stop()
        }
    }
}

function Get-PortConflictHint {
    param([int]$Port)

    if (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue) {
        $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
            Select-Object -First 1
        if ($null -ne $connection) {
            $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
            if ($null -ne $process) {
                return "Port $Port is already in use by PID $($process.Id) ($($process.ProcessName))."
            }
            return "Port $Port is already in use by PID $($connection.OwningProcess)."
        }
    }

    return "Port $Port is already in use."
}

function Assert-PortAvailable {
    param(
        [int]$Port,
        [string]$Label
    )

    if (-not (Test-LocalPortAvailable -Port $Port)) {
        $hint = Get-PortConflictHint -Port $Port
        throw "$Label cannot start. $hint"
    }
}

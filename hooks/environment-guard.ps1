# ==============================================================================
# Environment Guard Hook (PowerShell / Windows)
# Thin wrapper around canonical Python engine (hooks/environment_guard.py)
# ==============================================================================

[CmdletBinding()]
param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$EnginePath = Join-Path $ScriptDir "environment_guard.py"

# Try Python in .venv first, then system python
$PythonCmd = $null
if (Test-Path ".venv\Scripts\python.exe") {
    $PythonCmd = ".venv\Scripts\python.exe"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCmd = "py"
}

if ($PythonCmd -and (Test-Path $EnginePath)) {
    & $PythonCmd $EnginePath
    exit $LASTEXITCODE
} else {
    Write-Host "[Environment Guard] Running standalone PowerShell fallback..." -ForegroundColor Cyan
    $ExitCode = 0
    if ((Test-Path "pyproject.toml") -or (Test-Path "requirements.txt")) {
        if (-not (Test-Path ".venv") -and -not (Test-Path "venv")) {
            Write-Host "  ❌ ERROR: No project-local virtual environment (.venv/) found!" -ForegroundColor Red
            $ExitCode = 1
        }
    }
    exit $ExitCode
}

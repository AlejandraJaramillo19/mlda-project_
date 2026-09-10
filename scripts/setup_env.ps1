$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
        Write-Error "No se encontró Python en PATH. Instálalo antes de ejecutar este script."
        exit 1
    }
    $pythonCmd = "py"
} else {
    $pythonCmd = "python"
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual en .venv..."
    & $pythonCmd -m venv .venv
} else {
    Write-Host "El entorno virtual ya existe en .venv."
}

. ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Entorno listo y activado."

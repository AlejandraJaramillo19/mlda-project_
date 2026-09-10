#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

case "$OSTYPE" in
  darwin*|linux-gnu*)
    PYTHON_BIN="${PYTHON_BIN:-python3}"
    ;;
  *)
    echo "Este script está diseñado para macOS/Linux. En Windows usa: scripts/setup_env.ps1"
    exit 1
    ;;
 esac

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "No se encontró Python en PATH. Usa 'python3' o instala Python antes de continuar."
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Creando entorno virtual en .venv..."
  "$PYTHON_BIN" -m venv .venv
else
  echo "El entorno virtual ya existe en .venv."
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ""
echo "Entorno listo y activado."
echo "Puedes continuar con el proyecto en esta terminal."

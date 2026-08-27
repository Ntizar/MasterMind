#!/bin/bash
# Wrapper para ejecutar explorar-stars.py (Windows/git-bash compatible)
# Usa gh CLI para el token (no expone secrets en prompts de cron)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Token: variable de entorno si existe, si no gh auth (keyring de Windows)
if [ -z "$GITHUB_TOKEN" ]; then
  GITHUB_TOKEN=$(gh auth token 2>/dev/null)
  export GITHUB_TOKEN
fi

# Registry: ruta WINDOWS NATIVA (python.exe nativo no entiende /c/Users/...)
export STARS_REGISTRY="${STARS_REGISTRY:-C:/Users/d_ant/Projects/MasterMind/data/stars-registry.json}"

cd "$SCRIPT_DIR"
python explorar-stars.py "$@"

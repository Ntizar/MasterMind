#!/bin/bash
# Wrapper para ejecutar explorar-stars.py con el token correcto
# Evita exponer el patrón de lectura de secrets en prompts de cron

source /hermes-home/.env 2>/dev/null
export GITHUB_TOKEN
export NAN_API

cd /hermes-home/scripts
python3 explorar-stars.py "$@"

#!/bin/bash
# Wrapper para ejecutar indexar-skills.py con el token correcto
# Evita exponer el patrón de lectura de secrets en prompts de cron

source /hermes-home/.env 2>/dev/null
export NAN_API

cd /hermes-home/scripts
python3 indexar-skills.py "$@"

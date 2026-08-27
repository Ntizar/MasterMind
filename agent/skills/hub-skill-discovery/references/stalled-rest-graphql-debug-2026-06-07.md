# Incidente: rest-graphql-debug atascado (2026-06-07)

## Síntoma
El cron `mastermind-autoconfig` intentó instalar `rest-graphql-debug` (índice 4/118) 6 veces consecutivas entre el 06-07 de junio sin avanzar el índice.

## Causa raíz
Timeout de 120s en el script `skill-learning.sh`. Cuando el script timeout:
- El skill se descarga a `.hub/quarantine/rest-graphql-debug` (directorio)
- **Ni** el path de éxito **ni** el de error se ejecutan
- El `current_index` NO se incrementa
- Resultado: bucle infinito reintentando el mismo skill

## Reparo aplicado
1. Limpiar cuarentena: `rm -rf agent/skills/.hub/quarantine/rest-graphql-debug`
2. Avanzar índice de 4 a 5 en `.skill-learning-state.json`
3. Marcar `rest-graphql-debug` como skipped

## Lección
- El timeout del script es el enemigo silencioso: no produce error visible, solo bucle
- El script diagnóstico `scripts/diagnose-stalled-skill.sh` detecta estos casos automáticamente
- Considerar aumentar timeout del cron a 180s para skills pesados

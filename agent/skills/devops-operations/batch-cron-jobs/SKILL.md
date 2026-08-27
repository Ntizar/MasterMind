---
name: batch-cron-jobs
description: Patrón para fragmentar cron jobs de larga duración en unidades pequeñas con progreso JSON
---

# Batch Cron Jobs — Patrón de procesamiento fragmentado

## Cuándo aplicar

Un cron job falla por timeout (horas corriendo, 9009, OOMKill) porque ejecuta un script de larga duración que procesa TODO de golpe.

Señales:
- Cron con `schedule: "once in 30m"` ejecutando un script de scrapers/batch downloads
- Error "el script lleva ~7 horas corriendo", timeout, OOMKill
- Script que itera sobre una lista grande (países, años, ciudades, archivos)

## Patrón: Wrapper grupo por ejecución

### Paso 1: Crear wrapper en shell

```bash
#!/usr/bin/env bash
# wrapper-por-grupo.sh — Procesa un grupo por ejecución de cron
set -euo pipefail

DATA_DIR="/ruta/al/proyecto/Data"
SCRIPT_PRINCIPAL="/ruta/al/script.py"
PROGRESS_FILE="$DATA_DIR/progress.json"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- Listar grupos ---
GRUPOS=()
for d in "$DATA_DIR"/*/; do
    nombre=$(basename "$d")
    [[ "$nombre" == *progress* ]] && continue
    GRUPOS+=("$nombre")
done

# --- Cargar progreso ---
CURRENT_INDEX=0
COMPLETADO=False
if [ -f "$PROGRESS_FILE" ]; then
    CURRENT_INDEX=$(python3 -c "import json; d=json.load(open('$PROGRESS_FILE')); print(d.get('actual', 0))" 2>/dev/null || echo 0)
    COMPLETADO=$(python3 -c "import json; d=json.load(open('$PROGRESS_FILE')); print(str(d.get('completado', False)).lower())" 2>/dev/null || echo "false")
fi

# --- Si completado, salir ---
if [ "$COMPLETADO" = "true" ]; then
    echo -e "${GREEN}✅ Completado. ${#GRUPOS[@]} grupos procesados.${NC}"
    exit 0
fi

# --- Determinar grupo actual ---
if [ "$CURRENT_INDEX" -ge "${#GRUPOS[@]}" ]; then
    CURRENT_INDEX=0
fi

GRUPO_ACTUAL="${GRUPOS[$CURRENT_INDEX]}"
SIGUIENTE=$((CURRENT_INDEX + 1))

echo -e "${GREEN}▶️ Próximo grupo: $GRUPO_ACTUAL (${SIGUIENTE}/${#GRUPOS[@]})${NC}"

# --- Ejecutar con --filtro para ese grupo ---
START=$(date +%s)
set +e
OUTPUT=$(python3 "$SCRIPT_PRINCIPAL" --filtro "$GRUPO_ACTUAL" 2>&1)
EC=$?
set -e
ELAPSED=$(( $(date +%s) - START ))

echo "$OUTPUT"

# --- Guardar progreso ---
cat > "$PROGRESS_FILE" <<EOF
{
  "grupos": [$(printf '"%s",' "${GRUPOS[@]}" | sed 's/,$//')],
  "actual": $SIGUIENTE,
  "completado": $([ "$SIGUIENTE" -ge "${#GRUPOS[@]}" ] && echo "true" || echo "false"),
  "ultima_ejecucion": "$(date -u '+%Y-%m-%d %H:%M UTC')",
  "grupo_procesado": "$GRUPO_ACTUAL",
  "status": "$([ $EC -eq 0 ] && echo SUCCESS || echo ERROR)",
  "duracion_seg": $ELAPSED
}
EOF

# --- Resumen para cron ---
if [ $SIGUIENTE -lt "${#GRUPOS[@]}" ]; then
    echo -e "🔄 Siguiente: ${GRUPOS[$SIGUIENTE]}"
else
    echo -e "${GREEN}🎉 ¡Todos completados!${NC}"
fi
```

### Paso 2: Cron configuration

```
job_id: batch-procesamiento
no_agent: true          ← CRUCIAL: sin LLM, ejecuta directo
script: wrapper-por-grupo.sh
schedule: every 1h      ← cada hora procesa 1 grupo
repeat: N               ← número de grupos + margen (ej: 20 grupos → 25)
deliver: local          ← guarda resultado en archivos
enabled_toolsets: []    ← sin toolsets, solo filesystem
```

### Paso 3: Script principal con soporte de filtro

El script original necesita un flag de filtro (ej: `--pais`, `--año`, `--grupo`). Si no lo tiene, añadirlo. Ejemplo:

```python
# En el script original:
if "--pais" in sys.argv and i + 1 < len(sys.argv):
    SOLO_PAIS = sys.argv[i + 1]
```

## Estructura de archivos de progreso

```json
{
  "grupos": ["AT", "BE", "BG", "CH", "CZ", "DE"],
  "actual": 3,
  "completado": false,
  "ultima_ejecucion": "2026-07-08 14:00 UTC",
  "grupo_procesado": "BG",
  "status": "SUCCESS",
  "duracion_seg": 247
}
```

## Pitfalls

- **Sin `no_agent: true`** → el cron pasa por LLM cada ejecución → lento, caro, innecesario
- **Repeat mayor que grupos** → no pasa nada, al llegar a "completado: true" el wrapper sale 0
- **Script sin soporte de filtro** → añadir el parámetro de filtro al script original
- **Progreso en `completed=true`** → el wrapper debe detectar esto y salir sin hacer nada
- **Bash arrays con nombres con espacios** → usar `IFS= read -r` en loops
- **🔥 Script path resolution** → el cron solo encuentra scripts en `~/.hermes/scripts/`. Si el script está en `scripts/`, crear symlink: `ln -sf scripts/foo.sh ~/.hermes/scripts/foo.sh`
- **🔥 JSON booleans en bash** → `True`/`False` (Python) generan JSON inválido. Usar `true`/`false` (minúsculas). Ejemplo: `echo "true"` NO `echo "True"`.
- **🔥 `pipefail` + `find` en directorio inexistente** → Con `set -euo pipefail`, `find` en directorio que no existe da exit code 1. `2>/dev/null` suprime el error pero NO el código de salida. Con `pipefail` se propaga por `| wc -l` y mata el script. Fix: `find "$DIR" -name "*.pdf" 2>/dev/null | wc -l || true`. Clásico en batch downloads donde el primer ítem aún no tiene carpeta.

## Comparación: cron antiguo vs cron con wrapper

| Aspecto | Cron antiguo | Cron con wrapper |
|---------|-------------|-----------------|
| Ejecución | 1 → todo el lote | N → 1 grupo por ejecución |
| Duración | 7+ horas, timeout | 5-30 minutos |
| Reinicio tras crash | Pierde todo, empieza de 0 | Reanuda desde progreso |
| Coste LLM | Sí (si no es no_agent) | No (no_agent: true) |
| Visibilidad | Un fallo, no sabes dónde | Logs por grupo |

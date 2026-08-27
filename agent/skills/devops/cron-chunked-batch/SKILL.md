---
name: cron-chunked-batch
version: "1.0.0"
description: "Patrón para dividir tareas batch masivas en chunks procesados por cron jobs individuales con tracking de progreso."
tags: [cron, batch, chunking, progress-tracking, automation]
---

# Cron Chunked Batch — Batch dividido en chunks por cron jobs

## Resumen

Cuando una tarea batch (descarga, scraping, procesamiento) tarda demasiado para ejecutarse de una vez (horas, timeout), dividirla en **chunks pequeños** (país, archivo, entidad) y procesar un chunk por ejecución de cron. Cada ejecución lee el progreso, procesa un chunk, guarda progreso y termina.

## Cuándo aplicar

- Una tarea batch tarda **>10 minutos** en ejecutarse
- El cron tiene **timeout** o la ejecución se queda colgada
- Los items del batch son **independientes** entre sí (no hay orden estricto)
- Hay **progreso parcial** que se quiere preservar entre ejecuciones

## Estructura de archivos

```
project/
├── scripts/
│   ├── batch-worker.py        # Procesa UN solo item/chunk
│   └── batch-wrapper.sh       # Lee progreso, determina chunk siguiente, llama al worker
├── data/
│   ├── batch_index.json       # Índice de todos los items (URLs, metadatos)
│   └── batch_progress.json    # Estado de progreso (chunk actual, completado)
```

## Paso a paso

### 1. Crear el worker (procesa 1 item)

El worker debe:
- Recibir un parámetro de identificación del item (`--item XX` o `--pais CC`)
- Usar un **índice pre-existente** (no re-scrapear/re-calcular)
- Detectar items ya procesados y saltarlos
- Ser **idempotente** (re-ejecutar no daña nada)
- Terminar en **minutos**, no horas

Ejemplo mínimo:
```python
# batch-worker.py
import sys
import json
from pathlib import Path

ITEM_ID = sys.argv[1] if len(sys.argv) > 1 else None
INDEX = json.load(open("batch_index.json"))
DATA_DIR = Path("data")

if ITEM_ID not in INDEX:
    print(f"❌ {ITEM_ID} no está en el índice")
    sys.exit(1)

# Procesar solo este item
for año, urls in INDEX[ITEM_ID].items():
    dir_path = DATA_DIR / ITEM_ID / año
    dir_path.mkdir(parents=True, exist_ok=True)
    for url in urls:
        dest = dir_path / url.split("/")[-1]
        if dest.exists():
            continue  # Saltar si ya existe
        # Descargar/procesar...
```

### 2. Crear el wrapper (gestiona progreso)

El wrapper:
1. Lee `batch_progress.json` para saber qué chunk toca
2. Verifica si el chunk actual ya está completo (saltar)
3. Ejecuta el worker para el chunk actual
4. Guarda nuevo progreso
5. Termina (el próximo cron ejecutará el siguiente chunk)

Ejemplo mínimo:
```bash
#!/usr/bin/env bash
# batch-wrapper.sh
set -euo pipefail
cd "$(dirname "$0")/.."

PROGRESS_FILE="data/batch_progress.json"
WORKER="scripts/batch-worker.py"

# Cargar progreso
if [ -f "$PROGRESS_FILE" ]; then
    CURRENT=$(python3 -c "import json; print(json.load(open('$PROGRESS_FILE')).get('actual', 0))")
    DONE=$(python3 -c "import json; print(json.load(open('$PROGRESS_FILE')).get('completado', False))")
else
    CURRENT=0
    DONE=False
fi

# Verificar completado
if [ "$DONE" = "True" ]; then
    echo "✅ Todo completado"
    exit 0
fi

# Leer lista de chunks del índice
CHUNKS=($(python3 -c "import json; print('\n'.join(sorted(json.load(open('data/batch_index.json').keys()))))"))
TOTAL=${#CHUNKS[@]}

# Verificar índice
if [ "$CURRENT" -ge "$TOTAL" ]; then
    echo "⚠️ Índice fuera de rango, reiniciando"
    CURRENT=0
fi

CHUNK="${CHUNKS[$CURRENT]}"
NEXT=$((CURRENT + 1))

echo "▶️ Chunk: $CHUNK ($NEXT/$TOTAL)"

# Verificar si ya completo
EXISTENTES=$(find "data/$CHUNK" -name "*.pdf" 2>/dev/null | wc -l)
TOTAL_INDICE=$(python3 -c "import json; d=json.load(open('data/batch_index.json')); print(sum(len(v) for v in d.get('$CHUNK',{}).values()))")

if [ "$EXISTENTES" -ge "$TOTAL_INDICE" ] && [ "$TOTAL_INDICE" -gt 0 ]; then
    echo "✅ $CHUNK ya completo"
else
    # Ejecutar worker
    python3 "$WORKER" "$CHUNK"
fi

# Guardar progreso
cat > "$PROGRESS_FILE" <<EOF
{
  "chunks": [$(printf '"%s",' "${CHUNKS[@]}" | sed 's/,$//')],
  "actual": $NEXT,
  "completado": $([ "$NEXT" -ge "$TOTAL" ] && echo "True" || echo "False"),
  "ultima_ejecucion": "$(date -u '+%Y-%m-%d %H:%M UTC')",
  "chunk_procesado": "$CHUNK"
}
EOF

echo "💾 Progreso: $NEXT/$TOTAL"
```

### 3. Configurar el cron

```
no_agent: true           # Ejecuta directo, sin LLM
schedule: "every 1h"     # Frecuencia entre chunks
repeat: N                # Máximo de ejecuciones (>= número de chunks)
deliver: local           # Resultados a archivos
script: batch-wrapper.sh # El wrapper
```

**Importante con `no_agent: true`:**
- El cron ejecuta desde `/hermes-home/scripts/` (no el workspace)
- Usar **paths absolutos** en el wrapper
- Hacer `cd` al directorio del proyecto al inicio

## Progreso (formato JSON)

```json
{
  "chunks": ["AT", "BE", "BG", "CH", "CZ", "DE"],
  "actual": 3,
  "completado": false,
  "ultima_ejecucion": "2026-07-08T12:30:00Z",
  "chunk_procesado": "BG",
  "pdfs_existentes": 57,
  "status": "SUCCESS"
}
```

## Pitfalls

- **Re-scrapear es lento:** El wrapper NO debe volver a scrapear. Solo debe usar el índice existente y descargar/procesar. Si el worker re-scrapea, pierde la ventaja del chunking.
- **`no_agent: true` cambia el working directory:** El cron ejecuta desde `/hermes-home/scripts/`, no desde el workspace. Siempre usar paths absolutos y hacer `cd` al inicio del wrapper.
- **Idempotencia:** El worker debe detectar items ya procesados y saltarlos. Re-ejecutar no debe causar duplicados ni errores.
- **Índice vs directorios:** El wrapper debe comparar lo que hay en disco vs lo que dice el índice. Si disco >= índice, saltar el chunk.
- **Chunking granularity:** Elegir chunks que tengan **tiempo de ejecución consistente** (5-30 min cada uno). Si un chunk es 10x más grande que otros, considerar dividirlo más.
- **Error handling:** Si un chunk falla, el wrapper debe guardar el progreso (sin avanzar) para que el próximo cron re-intente el mismo chunk.

## Ejemplo real: ERAVisor

- **Problema:** Descarga de 4715 PDFs de ERA → 7 horas → timeout del cron
- **Solución:** Wrapper que procesa 1 país por ejecución, usa índice pre-existente, salta los ya descargados
- **Resultado:** 6 países en ~6 horas (1 por hora), cada ejecución <5 minutos
- **Files:** `scripts/descargar_todos_era.py` (worker), `scripts/eravisor-wrapper.sh` (wrapper), `Data/indice_era.json` (índice), `Data/eravisor_progress.json` (progreso)

## Variaciones

- **Por año en vez de por país:** Si un país tiene 1000 PDFs, dividir por año (cada año = un chunk)
- **Por página web:** Scraping de múltiples páginas, una por ejecución
- **Por archivo de datos:** Procesamiento de grandes datasets, archivo por archivo
- **Con backoff:** Si un chunk falla, esperar más tiempo antes de reintentar

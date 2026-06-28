# Diagnóstico de ejecuciones de cron sin cambios reales

## Problema

El cron `inventario-apis` puede ejecutarse pero no producir cambios reales. El timestamp de `estado.json` cambia pero el contenido es idéntico al anterior.

## Diagnóstico

### 1. Comparar estado.json con HEAD

```bash
cd /opt/hermes-work/inventario-apis
git show HEAD:estado.json | diff - estado.json
```

Si no hay diferencia → **no hubo progreso real**, solo un touch del timestamp.

### 2. Verificar cola de APIs nuevas

El script procesa 5 APIs por ejecución. Si no hay APIs nuevas en el catálogo, la cola está vacía:

```bash
# Contar directorios reales vs estado.json
python3 -c "
import os, json
base = '/opt/hermes-work/inventario-apis'
total = sum(len([d for d in os.listdir(os.path.join(base,c)) if os.path.isdir(os.path.join(base,c,d))]) for c in ['agentes-ia','automatizacion','ia'])
with open(f'{base}/estado.json') as f:
    estado = json.load(f)
print(f'Directorios: {total}, estado.json: {estado[\"procesadas\"]}')
"
```

### 3. Verificar si el catálogo cambió

El catálogo API-mega-list puede no tener APIs nuevas desde la última ejecución. Verificar el hash del README remoto:

```bash
TOKEN=$(grep '^GITHUB_TOKEN=' /hermes-home/.env | cut -d= -f2-)
curl -s -u "$TOKEN:" https://api.github.com/repos/cporter202/API-mega-list/contents/README.md | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha','unknown'))"
```

### 4. Verificar commits sin push

```bash
cd /tmp/inventario-apis
git log origin/main..HEAD --oneline  # commits locales sin push
git log --since="24 hours ago" --oneline  # commits recientes
```

## Causas comunes

1. **Cola vacía**: No hay APIs nuevas en el catálogo desde la última ejecución
2. **Duplicados**: El parser encuentra las mismas APIs que ya procesó (sin `seen_names` set)
3. **Timestamp solo**: El script hace `touch estado.json` sin cambios reales
4. **Divergencia de repos**: `/tmp/` y `/opt/hermes-work/` tienen estados diferentes

## Solución

Si no hay progreso real después de 3 ejecuciones consecutivas:
- Verificar que el catálogo remoto tenga cambios
- Revisar logs del cron para ver si el script está fallando silenciosamente
- Considerar pausar el cron hasta que haya APIs nuevas que procesar

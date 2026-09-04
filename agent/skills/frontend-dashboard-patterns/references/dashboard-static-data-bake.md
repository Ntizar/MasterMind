# Dashboard Static Data Bake — Referencia Completa

## Resumen

Patrón para crear dashboards HTML estáticos que muestran el estado de múltiples subsistemas. Un script Python recopila datos de fuentes heterogéneas y los "bakea" en el HTML como un objeto JavaScript embebido.

## Archivos de referencia

### Generador Python
- **Ruta:** `/hermes-home/scripts/generate-dashboard.py`
- **Función:** Lee ChromaDB (curl), skill-priority.json, knowledge-graph.json, skill-lifecycle-report.json, filesystem (notes, SOUL.md), y genera el objeto DATA embebido en el HTML.

### Plantilla HTML
- **Ruta:** `/root/workspace/Mastermind/dashboard/mastermind-status.html`
- **Función:** HTML autocontenido con CSS dark theme, grid de tarjetas, y renderizado del objeto DATA.

## Componentes típicos

| Componente | Fuente | Fallback |
|---|---|---|
| ChromaDB | `curl localhost:8000/api/v1/collections` | `{"status":"offline","count":0}` |
| Skills | `config/skill-priority.json` | `{"total":0,"high":0,"medium":0,"low":0}` |
| Notas | `glob notes/*.md` | `{"total":0,"archived":0}` |
| Crons | `systemctl list-timers` | `{"active":0,"paused":0,"once":0}` |
| Grafo | `learning/knowledge-graph.json` | `{"nodes":0,"edges":0,"orphans":0}` |
| SOUL.md | `os.path.getsize()` | `{"size":"error","status":"error"}` |

## Patrón de fallback robusto

Cada función de estado debe tener try/except con valores por defecto:

```python
def get_component_status():
    try:
        return {"status": "ok", "data": "..."}
    except Exception:
        return {"status": "error", "data": "unknown"}
```

Esto garantiza que el HTML nunca muestre `undefined` o `null`.

## Verificación

```bash
python3 -c "
import re, json
html = open('/root/workspace/Mastermind/dashboard/mastermind-status.html').read()
match = re.search(r'const DATA = (\{.*?\});', html, re.DOTALL)
data = eval(match.group(1))
print(json.dumps(data, indent=2))
"
```

## Historial de cambios

- **2026-06-10:** Primera creación — Mastermind Status Dashboard con 6 componentes + lifecycle

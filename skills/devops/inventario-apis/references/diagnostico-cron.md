# Diagnóstico de cron sin cambios reales

## Problema

El cron `inventario-apis` se ejecuta diariamente pero `estado.json` puede tener timestamp nuevo sin contenido cambiado ni commits. Esto genera confusión: parece que hubo actividad pero no la hubo.

## Causa

`procesar-apis.py` reescribe `estado.json` al inicio/final de cada ejecución, actualizando el timestamp incluso cuando no procesa APIs nuevas (cola vacía).

## Diagnóstico

```bash
# 1. Verificar si estado.json cambió realmente
cd /opt/hermes-work/inventario-apis
git show HEAD:estado.json | diff - estado.json
# Si no hay salida → mismo contenido, sin cambios reales

# 2. Verificar si hay commits hoy
git log --since="$(date -d 'today' +%Y-%m-%d) 00:00:00" --oneline
# Si no hay commits → no hubo progreso

# 3. Verificar si hay APIs nuevas en disco
find . -type d -newer estado.json | grep -v '.git' | head -20
# Si no hay resultados → no se crearon directorios nuevos
```

## Interpretación

| Estado | Significado |
|--------|-------------|
| Timestamp nuevo + mismo contenido + sin commits | Cron ejecutado, cola vacía (normal) |
| Timestamp nuevo + contenido cambiado + commits | Progreso real (APIs procesadas) |
| Timestamp viejo + contenido cambiado | estado.json no se actualizó (bug) |
| Timestamp nuevo + contenido cambiado + sin commits | Progreso pero no se hizo push (pendiente) |

## Referencia

- `../SKILL.md` — Procedimiento principal de lectura y resumen
- `./lectura-estado.py` — Script de parsing de estado.json

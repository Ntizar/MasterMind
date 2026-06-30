# PVPC — 5 Zonas Geográficas (Verificado 2026-05-28)

## El problema

El indicador **PVPC 2.0TD (ID 1001)** con `time_trunc=hour` devuelve **120 valores** (24h × 5 geo_ids).
La mayoría de scripts y el propio dashboard NO filtran por zona, lo que produce datos incorrectos.

## Mapeo de zonas

| geo_id | Zona | Típicamente igual a Península |
|--------|------|:---:|
| 8741 | **Península** | — (referencia) |
| 8742 | Canarias | Mayoría horas sí |
| 8743 | Baleares | Mayoría horas sí |
| 8744 | Ceuta | Mayoría horas sí |
| 8745 | Melilla | Mayoría horas sí |

## Impacto en scripts

### Dashboard (`normalizeHourlyValues`)
Itera sobre los 120 valores y sobrescribe cada hora con el último geo_id procesado. Como la API ordena por geo_id ascendente (8741→8745), **Melilla (8745) gana siempre**.

### Solución
Filtrar explícitamente por `geo_id=8741` (Península):

```javascript
const filtered = data.indicator.values.filter(v => v.geo_id === 8741);
// filtered tiene 24 valores, solo Península
```

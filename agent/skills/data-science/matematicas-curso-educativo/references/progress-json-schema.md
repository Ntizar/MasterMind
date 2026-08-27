# Schema de progress.json

Estructura del archivo de estado del sistema de mejora continua de DeSumarIntegrar.

## Estructura completa

```json
{
  "last_improved": "s01-1primaria.html",
  "last_run": "2026-06-09",
  "total_runs": 1,
  "topics": {
    "s01-1primaria.html": {
      "status": "improved_1",
      "level": "1º Primaria",
      "priority": 1,
      "category": "primaria_base",
      "improvements": [
        {
          "run": 1,
          "date": "2026-06-09",
          "added": "7 ejercicios interactivos con emojis, 3 explicaciones vida real"
        }
      ],
      "scores": {
        "exercises": 10,
        "text": 8,
        "visual": 3,
        "real_world": 4,
        "connections": 0,
        "difficulty_range": 2
      },
      "last_improved": "2026-06-09",
      "improvement_count": 1
    }
  }
}
```

## Campos del topic

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `status` | string | `"pending"`, `"improved_N"`, o `"complete"` |
| `level` | string | Nivel educativo: "1º Primaria", "ESO 1º", "Bachiller", etc. |
| `priority` | int | 1 = alta (primaria base), 2 = media, 3 = baja |
| `category` | string | Grupo: `primaria_base`, `primaria_2`, `primaria_3`, `eso`, `bachiller`, `universidad` |
| `improvements` | array | Historial de mejoras aplicadas |
| `scores` | object | Métricas del contenido actual (ver abajo) |
| `last_improved` | string | Fecha YYYY-MM-DD de última mejora |
| `improvement_count` | int | Número de rondas de mejora aplicadas (0-4) |

## Campos de scores

| Campo | Qué cuenta | Rango típico |
|-------|-----------|-------------|
| `exercises` | Divs con clase `exercise` | 3-15 |
| `text` | Suma de `box-teoria` + `box-ejemplo` | 5-20 |
| `visual` | Canvas/Plotly elements reales | 1-5 |
| `real_world` | Casos de vida real explicados | 1-5 |
| `connections` | Conexiones con otros temas | 0-3 |
| `difficulty_range` | Rango de dificultad | 1-3 |

## Estados de improvement_count

| count | status | Significado |
|-------|--------|-------------|
| 0 | `pending` | Sin mejorar |
| 1-3 | `improved_N` | Mejorado N veces |
| 4+ | `complete` | Nivel máximo alcanzado |

## Pitfall: conteo de canvas

El atributo `canvas` en HTML aparece tanto en elementos `<canvas>` como en el JS embebido (`getContext('2d')`, `canvas.width`, etc.). Para scores precisos:
- No usar `html.count('canvas')` — infla el resultado
- Contar manualmente o usar regex: `re.findall(r'<canvas[^>]*>', html)`

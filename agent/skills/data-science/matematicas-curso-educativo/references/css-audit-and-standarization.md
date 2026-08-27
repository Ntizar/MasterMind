# Estandarización CSS — DeSumarIntegrar

## Contexto

El proyecto DeSumarIntegrar tiene **4 niveles** con CSS de cobertura desigual:

| Nivel | Clases CSS | Estado |
|-------|-----------|--------|
| Primaria | ~47 clases | ✅ Completo (mejor) |
| ESO | ~34 clases | ⚠️ Faltaban feedback, connection-box, step-indicator, chart-container... |
| Bachiller | ~28 clases | ⚠️ Faltaban connection-box, step-indicator, real-world-badge, svg-container |
| Universidad | ~42 clases | ⚠️ Similar a Bachiller, con colores púrpura |

## Clases CSS esenciales (20)

Estas clases deben estar definidas en el CSS de **CADA** archivo de lección:

```
box-teoria, box-ejemplo, box-error, box-idea, box-success,
interactive, exercise, feedback, quiz-options, quiz-btn,
nav, footer, chapter, summary,
connection-box, step-indicator, real-world-badge, svg-container,
exercise-input, chart-container
```

## Bloques CSS por nivel

### ESO — Bloques faltantes típicos
```css
/* Feedback */
.feedback{display:inline-block;padding:.3rem .8rem;border-radius:6px;font-weight:600;margin-top:.5rem}
.feedback.correct{color:#065f46;background:var(--verde-claro)}
.feedback.incorrect{color:#991b1b;background:var(--rojo-claro)}

/* Connection box */
.connection-box{background:var(--pura-claro);border:2px dashed var(--pura);border-radius:10px;padding:1rem;margin:1rem 0}
.connection-box strong{color:var(--pura)}

/* Step indicator */
.step-indicator{display:inline-flex;align-items:center;gap:.3rem;background:var(--azul-claro);padding:.2rem .6rem;border-radius:12px;font-size:.8rem;font-weight:600;color:var(--azul);margin:.2rem}
.step-dot{width:8px;height:8px;border-radius:50%;background:var(--azul);display:inline-block}

/* Real world badge */
.real-world-badge{display:inline-block;background:var(--naranja);color:#fff;padding:.2rem .6rem;border-radius:12px;font-size:.75rem;font-weight:600}

/* SVG container */
.svg-container{background:#f8fafc;border-radius:12px;padding:1.5rem;margin:1rem 0;text-align:center}

/* Exercise input focus */
.exercise-input input:focus{outline:none;border-color:var(--azul)}

/* Chart container */
.chart-container{background:#f8fafc;border-radius:12px;padding:1rem;margin:1.5rem 0;border:1px solid #e2e8f0}
.chart-container h3{color:var(--azul);margin-bottom:.8rem;font-size:1.05rem}
.chart-container .chart-desc{font-size:.85rem;color:#64748b;margin-bottom:.8rem}
.chart-plot{width:100%;height:350px;border-radius:8px}
.chart-controls{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.8rem}
.chart-controls button{background:var(--azul);color:#fff;border:none;padding:.4rem 1rem;border-radius:6px;cursor:pointer;font-size:.85rem;font-weight:600}
.chart-controls button:hover{background:#1d4ed8}
.chart-controls button.active{background:var(--naranja)}

/* Interactive zone */
.interactive{background:#f1f5f9;border-radius:12px;padding:1.5rem;margin:1.5rem 0}
.interactive h3{color:var(--azul);margin-bottom:1rem;font-size:1.1rem}
```

### Bachiller/Universidad — Bloques faltantes típicos
Mismos bloques que ESO, pero sin `chart-container` si no usan Plotly. Universidad usa `#6366f1` en vez de `var(--azul)` para algunos elementos.

## Patrón de auditoría

Para verificar rápidamente la cobertura CSS de un archivo:

```python
import os, re

essential = [
    'box-teoria', 'box-ejemplo', 'box-error', 'box-idea', 'box-success',
    'interactive', 'exercise', 'feedback', 'quiz-options', 'quiz-btn',
    'nav', 'footer', 'chapter', 'summary',
    'connection-box', 'step-indicator', 'real-world-badge', 'svg-container',
    'exercise-input', 'chart-container',
]

with open(path) as f:
    content = f.read()

missing = [cls for cls in essential if cls not in content]
# missing == [] → CSS completo
```

## Tipos de archivos

- **Lecciones** (`eso1-1-numeros-enteros.html`, `s09-1-bachiller-limites.html`, etc.): necesitan TODAS las clases CSS
- **Índices** (`s07-1eso.html`, `s08-2-3eso.html`, `s10-1carrera.html`): tienen su propio CSS de tarjetas, no necesitan las mismas clases que las lecciones
- **Primaria**: tienen CSS completo pero les faltan `chart-container` y `exercise-input` que son para elementos que NO usan (no es un problema visual)

## Resultado post-estandarización (2026-06-12)

- **ESO**: 11/13 OK (85%) — 2 índices
- **Bachiller**: 9/11 OK (82%) — 1 índice + 1 con 1 clase
- **Universidad**: 8/11 OK (73%) — 2 índices + 2 con 2 clases
- **Primaria**: 3/70 OK — mayoría tiene 7 clases "extra" que no usan

## Commit

`7b5fcaf` — fix: estandarizar CSS en ESO, Bachiller y Universidad

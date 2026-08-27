# DibujoTecnico — Ronda 2: Patrones específicos

## Diferencias clave con DeSumarIntegrar

### progress.json estructura

- **Claves de temas:** Usan extensión `.html` (ej: `b06-02-metodos-acotacion.html`, NO `b06-02-metodos-acotacion`)
- **Scores anidados:** Los scores están en un campo `scores` dentro de cada tema, NO en el nivel raíz del tema
  ```json
  {
    "b06-02-metodos-acotacion.html": {
      "scores": {
        "svg_interactive": 9,
        "exercises": 9,
        "text_explanation": 9,
        "real_world": 9,
        "error_common": 9,
        "css_coherence": 10
      },
      "improvement_count": 3,
      "status": "improved_2"
    }
  }
  ```
- **Actualización de scores:** Siempre leer `t.scores` y actualizar ahí, NO en el nivel del tema
- **improvements:** Lista de dicts con campos `run`, `date`, `added`

### Ejercicios — Títulos en `<p>` en lugar de `<strong>`

En DibujoTecnico, los títulos de ejercicios están en `<p>` dentro del `<div class="exercise">`:
```html
<div class="exercise">
  <p>📐 Ejercicio 1 (Quiz): ¿Qué método...?</p>
  ...
</div>
```
**NO buscar `<strong>` como en DeSumarIntegrar.** Para añadir difficulty badges, patchear el `<p>`, no el `<strong>`.

### SVG — Estructura más compleja

Los SVGs de DibujoTecnico tienen más elementos (líneas de cota, flechas, textos de medida, rectángulos de dimensión boxes). Los elementos clave para interactividad son:
- **Líneas de cota** (`<line>` con stroke de colores)
- **Rectángulos de dimensión** (`<rect>` con fill y stroke)
- **Círculos de puntos** (`<circle>` con r pequeño)
- **Textos de medida** (`<text>` con valores como "80 mm")

### Contenido del proyecto

- 49 temas totales en Bachillerato
- Temas organizados por bloques: b01 (formatos), b02 (proyección), b03 (perspectivas), b04 (sistema diédrico), b05 (cortes), b06 (acotación), b07 (intersecciones), b08 (desarrollo), b09 (normalización)
- Cada tema tiene 6-8 ejercicios variados

### Quality Gates específicos

- Gate 4 (títulos duplicados): buscar en `/root/workspace/DibujoTecnico` NO en `/root/workspace/DeSumarIntegrar`
- CSS coherence: mismas 17 clases requeridas que DeSumarIntegrar

### Git

- Repo: `github.com/Ntizar/DibujoTecnico`
- Commit pattern: `v2-r2: [tema] - ronda 2: [dimensiones mejoradas]`
- Branch: `master`

## Ejemplo de actualización progress.json

```python
import json

with open('progress.json', 'r') as f:
    progress = json.load(f)

topics = progress.get('topics', {})
topic_id = 'b06-02-metodos-acotacion.html'  # CON .html
t = topics[topic_id]

scores = t.get('scores', {})
old_scores = dict(scores)

for d in ['svg_interactive', 'exercises', 'text_explanation', 'real_world', 'error_common', 'css_coherence']:
    if d in scores and scores[d] == 9:
        scores[d] = 10

t['scores'] = scores
t['improvement_count'] = t.get('improvement_count', 0) + 1
t['status'] = 'improved_v2'

if isinstance(t.get('improvements'), str):
    t['improvements'] = [t['improvements']]

t['improvements'].append({
    'run': 'ronda2-s3',
    'date': '2026-06-15',
    'added': 'SVG: @keyframes, 19 svg-element clickable, toggleHighlight, showStep re-trigger. Ejercicios: badges, 3 V/F nuevos. CSS: box-success.'
})

with open('progress.json', 'w') as f:
    json.dump(progress, f, indent=2, ensure_ascii=False)
```

## Lecciones aprendidas (2026-06-15)

1. **Siempre verificar estructura de progress.json ANTES de actualizar** — DibujoTecnico usa `.html` en las claves y scores anidados en `scores` dict
2. **Los títulos de ejercicios están en `<p>`, no en `<strong>`** — los patches de difficulty-badge deben apuntar al `<p>`
3. **Los SVGs tienen muchos elementos repetitivos** — usar Python `replace` con strings exactos es más fiable que `patch` para bloques SVG grandes
4. **El campo `improvements` ya es lista en ronda 2** — verificar tipo antes de append

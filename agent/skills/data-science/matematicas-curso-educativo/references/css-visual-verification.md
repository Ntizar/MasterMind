# Verificación Visual CSS Completa — DeSumarIntegrar

## Problema

La estandarización CSS (añadir clases faltantes) es un **parche funcional**, no una solución visual. Cuando David dice "el CSS está roto" o "igualarlo todo", necesita:

1. **Verificar visualmente** cada tema, no solo verificar que las clases existen en el HTML
2. **Asegurar consistencia visual** entre niveles (colores, bordes, espaciado, tipografía)
3. **Detectar temas con CSS mínimo o inexistente** que no se ven afectados por la estandarización

## Cuándo usar

- David dice "está roto", "igualarlo", "darle una vuelta completa"
- Después de cualquier cambio en el CSS base
- Cuando se detectan temas con cobertura CSS < 30%
- Antes de dar por terminada cualquier tarea de mejora visual

## Procedimiento

### 1. Auditoría programática

```python
import os, re

essential = [
    'box-teoria', 'box-ejemplo', 'box-error', 'box-idea', 'box-success',
    'interactive', 'exercise', 'feedback', 'quiz-options', 'quiz-btn',
    'nav', 'footer', 'chapter', 'summary',
    'connection-box', 'step-indicator', 'real-world-badge', 'svg-container',
    'exercise-input', 'chart-container',
]

def css_coverage(path):
    with open(path) as f:
        content = f.read()
    found = [cls for cls in essential if cls in content]
    return len(found) / len(essential)
```

### 2. Verificación visual por navegador

Para CADA nivel, navegar a 2-3 archivos representativos y usar `browser_vision()`:

```
https://ntizar.github.io/DeSumarIntegrar/eso1-1-numeros-enteros.html
https://ntizar.github.io/DeSumarIntegrar/s09-1-bachiller-limites.html
https://ntizar.github.io/DeSumarIntegrar/s10-1-carrera-limites-multivariable.html
```

**Preguntar a vision AI:**
- "¿Los colores son consistentes con el tema azul/naranja?"
- "¿Las cajas de teoría/ejemplo/error tienen bordes y fondos diferenciados?"
- "¿Los botones de quiz tienen estilos hover/correct/wrong?"
- "¿La navegación inferior se ve correctamente?"
- "¿Hay elementos sin estilo (texto plano donde debería haber caja)?"

### 3. Umbral de aceptación

| Nivel | Clases mínimas | Verificación visual |
|-------|---------------|---------------------|
| Primaria | 35+ | ✅ Sí (emojis, colores vivos) |
| ESO | 40+ | ✅ Sí (cajas diferenciadas, KaTeX) |
| Bachiller | 38+ | ✅ Sí (KaTeX, Plotly, colores) |
| Universidad | 40+ | ✅ Sí (púrpura, KaTeX, Plotly) |

**Si un archivo tiene < 30 clases → es visualmente defectuoso, aunque las clases que tiene funcionen.**

### 4. Priorización de reparación

1. **CRÍTICO:** Archivos con < 20 clases CSS → CSS roto visible
2. **ALTO:** Archivos con 20-30 clases → visual inconsistente
3. **MEDIO:** Archivos con 30-35 clases → faltar detalles
4. **BAJO:** Archivos con 35+ clases → OK

## Resultados históricos

- 2026-06-12: ESO tenía 34 clases (85% OK), Bachiller 28 (82% OK), Universidad 42 (73% OK)
- Tras estandarización: ESO 11/13 OK, Bachiller 9/11 OK, Universidad 8/11 OK
- **Pero David sigue viendo CSS roto** → significa que la estandarización no fue suficiente, se necesita verificación visual completa

## Pitfall

No confundir "las clases CSS existen en el archivo" con "el archivo se ve bien". Un archivo puede tener todas las clases definidas en CSS pero:
- Colores incorrectos (ej: `--azul-claro` no definido → color por defecto)
- Espaciado inconsistente
- Tipografía sin estilo
- Botones sin estados hover/correct/wrong
- Layout roto en móvil

**Siempre verificar con `browser_vision()` antes de dar por terminado.**

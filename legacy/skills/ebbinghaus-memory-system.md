---
name: ebbinghaus-memory-system
description: Sistema de memoria con decaimiento de Ebbinghaus para learnings. Fórmula R(t) = a/(log(t+1))^b + c. Carga bajo demanda, archivado automático.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [memoria, ebbinghaus, decay, aprendizaje, archivado, carga-bajo-demanda]
---

# Sistema de Memoria con Decaimiento de Ebbinghaus

## Qué es

Sistema de gestión de conocimiento que aplica la **curva de olvido de Ebbinghaus** para decidir qué learnings cargar en el contexto de cada sesión. Cada learning tiene un índice de relevancia `R(t)` que decae con el tiempo. Solo los learnings con `R(t) > 0.3` se cargan. Los que permanecen por debajo de `0.2` durante 60+ días se archivan automáticamente.

### La fórmula

```
R(t) = a / (log(t + 1))^b + c
```

Donde:
- `t` = días desde la última interacción con el learning
- `a`, `b`, `c` = parámetros según el tipo de decay

### 4 tipos de decay

| Tipo | a | b | c | Comportamiento | Uso |
|------|---|---|---|----------------|-----|
| **Permanente** | — | — | — | R = 1.0 (no decae) | Reglas del sistema, config, misiones |
| **Lento** | 0.7 | 0.8 | 0.25 | Decaimiento gradual, nunca baja de 0.25 | Conocimiento fundamental del proyecto |
| **Normal** | 0.8 | 1.2 | 0.15 | Decaimiento moderado, base en 0.15 | Learnings de proyectos pasados |
| **Rápido** | 0.9 | 1.5 | 0.05 | Decaimiento rápido, base en 0.05 | Detalles temporales, tareas resueltas |

### Ejemplo de cálculo

Para un learning con decay **normal** (`a=0.8, b=1.2, c=0.15`) a los 30 días:

```
R(30) = 0.8 / (log(31))^1.2 + 0.15
      = 0.8 / (3.434)^1.2 + 0.15
      = 0.8 / 4.93 + 0.15
      = 0.162 + 0.15
      = 0.312
```

A los 30 días, el learning aún se cargaría (R > 0.3). A los 90 días:

```
R(90) = 0.8 / (log(91))^1.2 + 0.15
      = 0.8 / (4.51)^1.2 + 0.15
      = 0.8 / 6.44 + 0.15
      = 0.124 + 0.15
      = 0.274
```

A los 90 días, ya no se cargaría (R < 0.3).

### Índice inteligente

El índice (`learnings/_index.md`) mantiene una tabla de **32+ entradas** con señales de relevancia:

```markdown
| Archivo | Decay | R(t) | Última interacción | Clusters | Señal |
|---------|-------|------|--------------------|----------|-------|
| auth-patterns.md | lento | 0.62 | 2026-05-28 | [seguridad, auth] | proyecto activo |
| deploy-shared.md | normal | 0.38 | 2026-04-15 | [deploy, hosting] | revisado recientemente |
| css-grid-fix.md | rápido | 0.12 | 2026-01-10 | [css, layout] | sin señales |
```

### Señales de relevancia

Las señales incrementan `R(t)` artificialmente:

| Señal | Incremento | Cuándo aplicar |
|-------|-----------|----------------|
| `proyecto activo` | +0.2 | El learning está en clusters de un proyecto en curso |
| `revisado recientemente` | +0.15 | Se interaccionó con el learning en los últimos 7 días |
| `referenciado` | +0.25 | Otro learning o skill lo referencia con wikilink |
| `crítico` | +0.3 | El learning contiene información crítica para el proyecto |
| `sin señales` | 0 | Sin señales de relevancia detectadas |

## Cuándo usar

- Al arrancar el sistema: el librarian carga solo los learnings con `R(t) > 0.3`
- Al crear un nuevo learning: asignar el tipo de decay apropiado
- Al revisar un learning: actualizar `última_interacción` para resetear parcialmente el decay
- Al archivar: mover learnings con `R(t) < 0.2` durante 60+ días a `learnings/archived/`

## Pasos

### Paso 1 — Crear un learning con decay

```markdown
---
nombre: "Patrón de autenticación con JWT"
fecha_creación: 2026-06-03
ultima_interaccion: 2026-06-03
decay: lento  # permanente, lento, normal, rápido
clusters: [seguridad, auth, backend]
senales: [proyecto activo, critico]
---

# Patrón de Autenticación con JWT

Contenido del learning...
```

### Paso 2 — Calcular R(t)

El librarian (o el orchestrator) calcula `R(t)` para cada learning:

```python
import math

def ebbinghaus_decay(t, a, b, c):
    """Calcula R(t) = a / (log(t+1))^b + c"""
    if t < 0:
        t = 0
    return a / (math.log(t + 1) ** b) + c

# Ejemplo: decay normal, 30 días
r_30 = ebbinghaus_decay(30, a=0.8, b=1.2, c=0.15)
# r_30 = 0.312
```

### Paso 3 — Aplicar señales de relevancia

```python
def relevancia_final(r_t, senales):
    """Aplica incrementos por señales de relevancia"""
    bonus = {
        "proyecto activo": 0.2,
        "revisado recientemente": 0.15,
        "referenciado": 0.25,
        "critico": 0.3
    }
    for senal in senales:
        r_t += bonus.get(senal, 0)
    return min(r_t, 1.0)  # No puede exceder 1.0
```

### Paso 4 — Carga bajo demanda

Al arrancar, el librarian carga solo los learnings con `R(t) > 0.3`:

```
[LIBRARIAN]
cargando_learnings:
  - auth-patterns.md (R=0.62) ✓
  - deploy-shared.md (R=0.38) ✓
  - css-grid-fix.md (R=0.12) ✗ (no cargar)
  - routing-patterns.md (R=0.45) ✓

total_cargados: 3/32
tokens_ahorrados: ~42%
```

### Paso 5 — Actualizar al interactuar

Cada vez que se lee o referencia un learning, actualizar `ultima_interaccion`:

```
[LIBRARIAN]
actualizado: css-grid-fix.md
ultima_interaccion: 2026-06-03 (antes: 2026-01-10)
nuevo_decay: 0.41 (antes: 0.12)
```

### Paso 6 — Archivado automático

Los learnings con `R(t) < 0.2` durante **60+ días continuos** se archivan:

```
[ARCHIVER]
archivando:
  - old-css-hack.md (R=0.08, 95 días sin interacción)
  - deprecated-api.md (R=0.11, 72 días sin interacción)

moviendo a: learnings/archived/
```

## Pitfalls

- **Decay demasiado agresivo:** No usar decay rápido para conocimiento fundamental. Si un learning es importante para el proyecto, usar lento o permanente.
- **No actualizar última_interacción:** Si se referencia un learning pero no se actualiza la fecha, el decay seguirá calculándose sobre la fecha antigua.
- **Señales incorrectas:** No marcar como `proyecto activo` un learning de un proyecto que ya terminó. Las señales deben reflejar la realidad actual.
- **Archivar prematuramente:** Un learning con `R(t) < 0.2` solo se archiva si lleva 60+ días consecutivos por debajo. Un pico temporal de interacción resetea el contador.
- **Permanente para todo:** No marcar todo como permanente. Solo reglas del sistema, config y misiones deben ser permanentes. Los learnings de proyectos específicos deben decaer.
- **Ignorar el archivado:** Los learnings archivados ocupan espacio en el índice. Archivarlos mantiene el índice limpio y eficiente.

## Verificación

1. ✅ Cada learning tiene un tipo de decay asignado (permanente, lento, normal, rápido)
2. ✅ Cada learning tiene `ultima_interaccion` actualizada
3. ✅ Cada learning tiene `clusters` y `senales` en el frontmatter
4. ✅ Solo se cargan learnings con `R(t) > 0.3`
5. ✅ Los learnings con `R(t) < 0.2` durante 60+ días están en `learnings/archived/`
6. ✅ El índice `_index.md` tiene las 32+ entradas actualizadas
7. ✅ Las señales de relevancia reflejan el estado actual del proyecto

---
name: project-spec-workflow
version: "1.0.0"
description: "Flujo obligatorio de spec antes de código. Cuando el usuario pide un proyecto nuevo o feature grande, el agente hace preguntas estructuradas, propone arquitectura modular, y genera SPEC.md antes de escribir una sola línea de código."
tags: [mastermind, spec, architecture, workflow, planning, project-init]
---

# Project Spec Workflow — Spec antes que código

## Cuándo se activa

**AUTOMÁTICAMENTE** cuando el usuario pide:
- Un proyecto nuevo ("hazme un visor de X", "crea un dashboard de Y")
- Una feature grande (>3 archivos, nueva pestaña, nuevo módulo)
- Un "rewrite" o reestructuración

**NO se activa** para:
- Fixes puntuales (1-2 archivos)
- Preguntas o consultas
- Cambios de estilo/contenido
- Tareas que el usuario ya ha especificado completamente

## Principio fundamental

> **Sin spec, no codeas.** Si el usuario no puede describir qué quiere en 5 minutos, el agente no puede construirlo en 5 horas.

## Fase 1 — Detección y propuesta inicial

Cuando el usuario pide algo nuevo, el agente **NO empieza a codear**. En su lugar:

1. **Busca en memoria** si hay proyectos similares del usuario (GTFSSpain, DataHubEspana, GBFSSpain, etc.)
2. **Busca en ChromaDB** skills relevantes para el dominio
3. **Propone una visión inicial** basándose en lo que ya sabe

### Plantilla de propuesta inicial

```
He detectado que quieres [X]. Basándome en tu historial ([proyectos similares]),
propongo:

🎯 **Qué será:** [1 frase]
📊 **Datos:** [fuentes probables]
🗺️ **Pantallas:** [lista inicial]
⚡ **Stack:** [tecnologías]
🚫 **No incluye:** [non-goals iniciales]

Antes de construir nada, necesito que confirmes o ajustes estas decisiones:
```

## Fase 2 — Preguntas estructuradas (NO abiertas)

El agente hace preguntas **estructuradas con opciones**, nunca preguntas abiertas tipo "¿qué quieres?". El usuario responde rápido, no tiene que pensar desde cero.

### Bloque A — Alcance (qué hace y qué no)

```
A1. ¿Qué problema resuelve?
   [ ] Panel de visualización de datos
   [ ] Herramienta interactiva/análisis
   [ ] Visor cartográfico
   [ ] Otro: _____

A2. ¿Cuál es la pantalla principal?
   [ ] Mapa a pantalla completa + panel lateral
   [ ] Dashboard con tabs/pestañas
   [ ] Lista/tabla + detalle
   [ ] Otro: _____

A3. ¿Qué NO hace? (non-goals — tan importante como qué sí hace)
   [ ] No tiene backend (todo client-side)
   [ ] No tiene login/usuarios
   [ ] No tiene modo offline
   [ ] No guarda datos de usuario
   [ ] Otro: _____
```

### Bloque B — Datos

```
B1. ¿De dónde vienen los datos?
   [ ] APIs públicas (cuáles: _____)
   [ ] JSON estático (tamaño aproximado: _____)
   [ ] Mixto (algunos estáticos + APIs en vivo)
   [ ] No lo sé, propón tú

B2. ¿Cada cuánto se actualizan?
   [ ] Tiempo real (segundos/minutos)
   [ ] Diario
   [ ] Estático (no cambia)
   [ ] Mixto

B3. ¿Volumen de datos?
   [ ] Pequeño (< 100 registros)
   [ ] Medio (100-10K registros)
   [ ] Grande (10K-1M registros)
   [ ] No lo sé
```

### Bloque C — Arquitectura y stack

```
C1. ¿Frontend, backend, o ambos?
   [ ] Solo frontend (estático, GitHub Pages)
   [ ] Frontend + proxy backend mínimo
   [ ] Full-stack (backend con DB)

C2. ¿Tecnologías preferidas?
   [ ] Vanilla JS (sin framework) ← recomendado para visores
   [ ] React/Vue (si hay mucha interactividad)
   [ ] Three.js (si hay 3D)
   [ ] Lo que propongas tú

C3. ¿Deploy dónde?
   [ ] GitHub Pages (estático)
   [ ] NaN.builders (con backend)
   [ ] No lo sé todavía
```

### Bloque D — Lo que el usuario ya sabe

```
D1. ¿Hay algo que YA sabes cómo quieres que sea?
    (colores, estilo, disposición, comportamiento específico)
    → El usuario describe. El agente anota como REQUISITOS.

D2. ¿Hay algo que HAYAS VISTO que te guste como referencia?
    (URLs, proyectos, diseños)
    → El agente busca referencias visuales si hace falta.

D3. ¿Hay algo que TE HAYA PASADO antes que quieras evitar?
    (bugs recurrentes, patrones que no funcionan)
    → El agente anota como ANTI-PATRONES.
```

## Fase 3 — Generación de SPEC.md

Con las respuestas, el agente genera un documento `SPEC.md` en el repo del proyecto con esta estructura:

```markdown
# [Nombre del proyecto] — SPEC

## Visión
[1 frase: qué es y para qué]

## Alcance

### Sí hace
- [lista de features]

### NO hace (non-goals)
- [lista explícita de lo que no]

## Pantallas
1. [Pantalla 1]: [descripción]
2. [Pantalla 2]: [descripción]

## Datos
| Fuente | Tipo | Actualización | Volumen |
|--------|------|---------------|---------|
| [fuente] | [API/JSON] | [frecuencia] | [tamaño] |

## Arquitectura

### Capas
| Capa | Archivo | Responsabilidad |
|------|---------|----------------|
| Datos | data/*.json | Datos estáticos |
| Estado | js/state.js | Estado global + carga |
| API | js/api.js | Fetch de APIs |
| UI | js/ui.js | Tabs, panels, eventos |
| Render | js/render.js | Gráficos, mapa, tablas |

### Estado global
[Diagrama de qué estado existe y quién lo posee]

### Interfaces entre módulos
[Qué funciones expone cada módulo]

## Stack
- Frontend: [tecnologías]
- Deploy: [plataforma]

## Criterios de éxito
- [métrica 1: ej, carga en < 3s]
- [métrica 2: ej, click → respuesta < 500ms]
- [métrica 3]

## Anti-patrones (lo que evitamos)
- [patrón 1: ej, no usar estado global esparcido]
- [patrón 2]

## Referencias
- [proyectos similares del usuario]
- [links de inspiración]
```

## Fase 4 — Propuesta de arquitectura modular

El agente propone la estructura de archivos **antes de codear**:

```
proyecto/
├── SPEC.md              ← La spec generada
├── index.html           ← Solo estructura DOM, sin lógica
├── css/
│   └── styles.css       ← Solo estilos
├── js/
│   ├── state.js         ← Estado global + funciones de carga
│   ├── api.js           ← Fetch de APIs externas
│   ├── map.js           ← Solo mapa (init, markers, layers)
│   ├── charts.js        ← Solo gráficos
│   ├── ui.js            ← Tabs, panels, eventos de UI
│   └── main.js          ← Orquestador: init + wiring
├── data/
│   └── *.json           ← Datos estáticos
└── README.md            ← Docs generadas desde SPEC
```

**Regla de oro:** Un archivo = una responsabilidad. Si el agente va a tocar 3+ archivos en una iteración simple, para y replantea.

## Fase 5 — Human loop (aprobación obligatoria)

```
1. Agente presenta SPEC.md + arquitectura propuesta
2. Usuario revisa: ✅ o ajustes
3. Solo DESPUÉS del ✅ → empezar a codear
```

**El agente NUNCA empieza a codear sin SPEC aprobada.**

## Fase 6 — Iteración segura (en cada cambio posterior)

Para cada feature nueva o cambio grande:

```
1. IMPACTO: ¿Qué archivos toca? ¿Qué no toca?
2. ¿Actualiza SPEC.md? (si el alcance cambia)
3. Implementar
4. Verificar que lo anterior sigue funcionando
5. Commit
```

### Plantilla de iteración

```markdown
## Iteración: [nombre]

### Qué quiero
[1 frase]

### Archivos que toca
- js/ui.js: [qué cambio]
- js/state.js: [qué cambio]

### Archivos que NO toca
- js/map.js
- js/charts.js
- data/*.json

### Verificación
- [ ] Lo anterior sigue funcionando
- [ ] Lo nuevo funciona
- [ ] No hay console errors
```

## Detección automática

El agente debe detectar automáticamente cuándo activar este flujo. Señales:

- "hazme", "crea", "construye", "quiero un" + nombre de proyecto → **proyecto nuevo**
- "añade", "agrega", "ponle" + feature grande → **iteración con spec**
- "arregla", "cambia", "modifica" + cosa pequeña → **fix directo, sin spec**

Si hay duda, el agente pregunta: *"¿Es un proyecto nuevo o un cambio en algo existente?"*

## Integración con memoria

El agente consulta memoria antes de proponer:
- ¿Hay proyectos similares del usuario? → usar como referencia
- ¿Hay preferencias de diseño? → aplicar (Aurora, colores, etc.)
- ¿Hay anti-patrones conocidos? → evitar

## Referencias

- **Template copiable:** `templates/SPEC-template.md` — starter file para generar SPEC.md en nuevos proyectos
- **Demo real:** `references/datahubespana-spec-demo.md` — ejemplo aplicado a DataHubEspana (monolito 11K líneas → modular)
- **SPEC.md completa de ejemplo:** `references/datahubespana-SPEC.md` — spec real generada para DataHubEspana
- **Skill relacionado:** `spec-driven-development` (toolkit externo GitHub spec-kit) — `project-spec-workflow` es la adaptación interna del mismo concepto
- **Skill umbrella:** `software-development` → sección "Spec-Driven Development" apunta a este skill
- **Orquestación:** `mastermind-orchestration` → paso 0 del flujo activa este skill para proyectos nuevos

## Pitfalls

- **No sobre-preguntar:** Si el usuario ya dio suficiente contexto en el primer mensaje, no hacer 20 preguntas. Hacer solo las que falten.
- **No spec sin código:** La spec no es un ensayo. Si pasa de 2 páginas, es demasiado. Specs ejecutables, concisas.
- **No ignorar la spec:** Una vez aprobada, la spec es el contrato. Si el agente se desvía, el usuario lo puede frenar con "vuelve a la spec".
- **No codear sin ✅:** El human loop es obligatorio. Sin aprobación, no hay código.
- **Proyectos de 1 archivo:** Si es algo pequeño (un solo HTML), la spec puede ser un comentario en el top del archivo. No necesita SPEC.md completo.
- **Iteración sobre monolitos:** Si el proyecto ya existe como monolito (ej: index.html de 11K líneas), la spec debe incluir un PLAN DE EXTRACCIÓN: qué sacar a archivos separados y en qué orden.

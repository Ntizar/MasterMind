---
id: "skill-02"
nombre: learning-template-pattern
tipo: skill
rol: patrón para destilar aprendizaje estructurado
version: "1.0.0"
autor: comunidad nan.builders
licencia: MIT
plataformas: [nan.builders, github-pages, local]
tags: [learning, template, destilación, conocimiento, clusters, decay, ebbinghaus]
creado: 2026-06-03
actualizado: 2026-06-03
---

# Patrón: Learning Template (v2)

## Qué es

Un patrón para destilar aprendizaje estructurado de cada ciclo completado.
Cada learning es un archivo en `agents/learnings/YYYY-MM-DD-[nombre-tarea].md`
que captura lo esencial para reutilización futura, con clusters dinámicos
y decay Ebbinghaus para carga bajo demanda.

### Formato v2 con frontmatter

```yaml
---
fecha: YYYY-MM-DD
tarea: [nombre-kebab]
tipo: [software/research/escritura/operaciones/conocimiento/creatividad/analisis/mixta]
complejidad: [baja/media/alta]
clusters: [cluster1, cluster2]
proyecto: [nombre-hub o "ninguno"]
patron: [nombre-patron o "ninguno"]
decay: [permanente/lento/normal/rapido]
---
```

### Estructura del cuerpo

```
# [Nombre legible de la tarea]

## Decisión clave
[La decisión más importante. 1 oración precisa y generalizable.]

## Patrón reutilizable
**Nombre:** [nombre-del-patron o "ninguno"]
**Descripción:** [cómo aplicarlo en futuras tareas similares]

## Qué funcionó
- [bullet: acción concreta que generó resultado positivo]
- [bullet]

## Qué evitar
- [bullet: acción concreta que generó resultado negativo]
- [bullet o "nada detectado"]

## Skills usados
- [skill o "ninguno"]

## Criterios que validaron el éxito
[descripción breve de los criterios que confirmaron que la tarea fue exitosa]

## Contexto de la tarea
- Flujo ejecutado: [agentes que participaron]
- Reintentos necesarios: [número o "ninguno"]
- Tiempo estimado: [corto/medio/largo]

## Conexiones
**Clusters:** #[cluster1] · #[cluster2]
**Proyecto:** [[nombre-hub]]  ← omitir si proyecto es "ninguno"
**Aprendizajes relacionados:** [[fecha-tarea]] · [[fecha-otra-tarea]]
```

### Ejemplo real

```yaml
---
fecha: 2026-06-03
tarea: landing-nan-builders
tipo: software
complejidad: baja
clusters: [web-static, nan-builders]
proyecto: nan.builders
patron: static-deploy-pattern
decay: lento
---
```

```
# Landing para nan.builders

## Decisión clave
Usar CSS inline en lugar de archivo separado redujo los entregables de 2 a 1
y eliminó un punto de fallo en el deploy.

## Patrón reutilizable
**Nombre:** static-deploy-pattern
**Descripción:** Para deploys estáticos en plataformas con límites de recursos,
minimizar el número de archivos reduce la superficie de fallo. CSS inline
es preferible a archivos separados cuando el contenido es menor a 50KB.

## Qué funcionó
- Escribir la spec antes de implementar (cero preguntas del implementer)
- CSS inline en lugar de archivo separado (1 entregable en vez de 2)
- Validar HTML5 antes de entregar (detecté tag sin cerrar en revisión)

## Qué evitar
- Intentar incluir service worker en la primera iteración (fuera de scope)
- Usar fuentes externas (fallan en subdominios nan.builders)

## Skills usados
- spec-template-pattern
- nan-builders-deploy

## Criterios que validaron el éxito
- index.html pasa validación HTML5 sin errores
- Archivo pesa 32KB (límite 50KB)
- Deploy verificado en GitHub Pages

## Contexto de la tarea
- Flujo ejecutado: classifier → planner → spec-writer → implementer → reviewer
- Reintentos necesarios: 1 (el reviewer encontró tag sin cerrar)
- Tiempo estimado: corto

## Conexiones
**Clusters:** #web-static · #nan-builders
**Proyecto:** [[nan.builders]]
**Aprendizajes relacionados:** [[2026-05-15-github-pages-setup]] · [[2026-05-20-static-css-pattern]]
```

## Cuándo usar

- **Después de cada ciclo completado con PASS** — solo se archivan tareas aprobadas.
- **Cuando el humano da ✅ final** — el archiver solo se activa con aprobación humana.
- **Para patrones que se esperan reutilizar** — si el patrón tiene valor futuro, merece un learning.
- **Para soluciones a problemas recurrentes** — si el mismo problema aparece 2+ veces, destilar el learning.

## Pasos

### Paso 1: Extraer la Decisión clave

Identificar la decisión más importante de la tarea. Debe ser:
- **1 oración**
- **Generalizable** a otras tareas
- **Precisa** (sin ambigüedad)

**Mal:** "Se decidió hacer la landing"
**Bien:** "Usar CSS inline en lugar de archivo separado redujo los entregables de 2 a 1 y eliminó un punto de fallo en el deploy."

### Paso 2: Definir el Patrón reutilizable

Si hay un patrón que se puede reutilizar:
- **Nombre:** descriptivo y corto (kebab-case)
- **Descripción:** cómo aplicarlo en tareas futuras similares

Si no hay patrón reutilizable, escribir "ninguno".

### Paso 3: Listar Qué funcionó y Qué evitar

Cada bullet debe ser una **acción concreta**, no una opinión.

**Mal:** "El CSS se ve bien"
**Bien:** "CSS inline en lugar de archivo separado (1 entregable en vez de 2)"

**Mal:** "El reviewer fue estricto"
**Bien:** "Validar HTML5 antes de entregar (detecté tag sin cerrar en revisión)"

### Paso 4: Asignar Clusters dinámicos

Los clusters son dinámicos — no hay lista cerrada. Procedimiento:

1. Leer `agents/projects/_clusters.md` — ver qué clusters existen
2. Asignar los clusters existentes que correspondan (puede ser 1 o varios)
3. Si el dominio no encaja en ninguno existente → crear uno nuevo:
   - Nombre: minúsculas, sin espacios, kebab si es compuesto (`#saas`, `#youtube`, `#excel`)
   - Añadir fila en la tabla de `_clusters.md`
4. Si hay proyecto hub existente → enlazar con `[[nombre-hub]]`
5. Si el proyecto es nuevo → crear hub en `agents/projects/nombre-hub.md`

**Ejemplos de clusters:**
- `#web-static` — deploys estáticos, HTML/CSS/JS sin backend
- `#nan-builders` — todo lo relacionado con nan.builders
- `#github-pages` — deploys a GitHub Pages
- `#saas` — productos SaaS
- `#api-design` — diseño de APIs

### Paso 5: Asignar Decay type

El campo `decay` determina la velocidad de olvido del learning según la fórmula
de Ebbinghaus. Usar esta guía:

| Tipo de learning | Decay recomendado | Ejemplo |
|-----------------|-------------------|---------|
| Regla del sistema / patrón fundamental | **permanente** | verify-before-deliver, iterative-development |
| Patrón técnico reutilizable | **lento** | static-deploy-pattern, dual-proxy-cors-pattern |
| Solución a problema específico | **normal** | subdomain-to-path-apache, simplify-and-retry |
| Fix puntual / contexto temporal | **rápido** | start-bat-v2-browser-auto, feature-archived |

**Cómo decidir:**
- ¿Este aprendizaje se espera usar en los próximos 30 días? → **lento** o **permanente**
- ¿Es una regla del sistema que nunca debe olvidarse? → **permanente**
- ¿Es una solución a un problema que puede no repetirse pronto? → **normal**
- ¿Es un fix puntual de contexto temporal? → **rápido**

### Paso 6: Documentar el Contexto de la tarea

- **Flujo ejecutado:** qué agentes participaron (classifier, planner, spec-writer, implementer, reviewer)
- **Reintentos necesarios:** cuántas veces el reviewer devolvió el trabajo
- **Tiempo estimado:** corto (<15 min), medio (15-60 min), largo (>1 hora)

### Paso 7: Crear Conexiones

- **Clusters:** #[cluster1] · #[cluster2]
- **Proyecto:** [[nombre-hub]] (omitir si "ninguno")
- **Aprendizajes relacionados:** [[fecha-tarea]] · [[fecha-otra-tarea]]

Conectar con aprendices anteriores del mismo cluster o proyecto.

### Paso 8: Actualizar índices

1. Añadir fila en `agents/learnings/_index.md` con: fecha, tarea, tipo, patrón, clusters, proyecto, señal de relevancia, cuándo cargar, **decay**, archivo.
2. Actualizar `agents/projects/_clusters.md` si hay clusters nuevos.
3. Crear `agents/projects/nombre-hub.md` si hay proyecto nuevo.

## Pitfalls

| Pitfall | Consecuencia | Cómo evitar |
|---------|-------------|-------------|
| Decisión clave con más de 1 oración | El learning pierde foco | Escribir exactamente 1 oración |
| Clusters inventados | El learning no se carga bajo demanda | Verificar clusters en `_clusters.md` antes de asignar |
| Decay incorrecto | El aprendizaje se olvida o persiste innecesariamente | Usar la tabla de guía de decay |
| "Qué funcionó" con opiniones | No es accionable en futuras tareas | Usar acciones concretas, no opiniones |
| Omitir conexiones | El aprendizaje queda aislado en el grafo | Siempre incluir al menos 1 aprendizaje relacionado |
| Archivar sin reviewer PASS | Se pierde calidad del conocimiento | Solo archivar con veredicto PASS del reviewer |

## Verificación

Antes de archivar un learning, el archiver debe verificar:

1. **Frontmatter**: ¿fecha, tarea, tipo, complejidad, clusters, proyecto, patrón, decay están presentes?
2. **Decisión clave**: ¿Es exactamente 1 oración? ¿Es generalizable?
3. **Patrón reutilizable**: ¿Tiene nombre y descripción? ¿Es "ninguno" si no aplica?
4. **Clusters**: ¿Existen en `_clusters.md`? ¿Son relevantes?
5. **Decay**: ¿Corresponde al tipo de learning? ¿Usa la tabla de guía?
6. **Contexto**: ¿Flujo, reintentos y tiempo están documentados?
7. **Conexiones**: ¿Hay al menos 1 aprendizaje relacionado?
8. **Índices**: ¿Se actualizó `_index.md` y `_clusters.md` si es necesario?

Si algún punto falla → el learning vuelve al archiver para corrección.

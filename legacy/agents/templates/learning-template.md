# Learning Template

```
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

# [Nombre legible de la tarea]

## Decisión clave
[La decisión más importante. 1 oración precisa y generalizable.]

## Patrón reutilizable
**Nombre:** [nombre-del-patron o "ninguno"]
**Descripción:** [cómo aplicarlo en futuras tareas similares]

## Qué funcionó
- [bullet]

## Qué evitar
- [bullet o "nada detectado"]

## Skills usados
- [skill o "ninguno"]

## Criterios que validaron el éxito
[descripción breve]

## Contexto de la tarea
- Flujo ejecutado: [agentes que participaron]
- Reintentos necesarios: [número o "ninguno"]
- Tiempo estimado: [corto/medio/largo]

## Conexiones
**Clusters:** #[cluster1] · #[cluster2]
**Proyecto:** [[nombre-hub]]  ← omitir si proyecto es "ninguno"
**Aprendizajes relacionados:** [[fecha-tarea]] · [[fecha-otra-tarea]]
```

## Cómo asignar clusters

Los clusters son dinámicos. No hay lista cerrada.
Para asignar clusters a un learning nuevo:
1. Leer `agents/projects/_clusters.md` — ver qué clusters existen
2. Asignar los clusters existentes que correspondan (puede ser 1 o varios)
3. Si el dominio no encaja en ninguno existente → crear uno nuevo:
   - Nombre: minúsculas, sin espacios, kebab si es compuesto (`#saas`, `#youtube`, `#excel`)
   - Añadir fila en la tabla de `_clusters.md`
4. Si hay proyecto hub existente → enlazar con `[[nombre-hub]]`
5. Si el proyecto es nuevo → crear hub en `agents/projects/nombre-hub.md` usando el template

## Asignación de decay type

El campo `decay` determina la velocidad de olvido del learning. Usar esta guía:

| Tipo de learning | Decay recomendado | Ejemplo |
|-----------------|-------------------|---------|
| Regla del sistema / patrón fundamental | permanente | verify-before-deliver, iterative-development |
| Patrón técnico reutilizable | lento | dual-proxy-cors-pattern, async-loading-flags |
| Solución a problema específico | normal | subdomain-to-path-apache, simplify-and-retry |
| Fix puntual / contexto temporal | rápido | start-bat-v2-browser-auto, feature-archived |

Ver fórmula de Ebbinghaus y tabla de parámetros en `agents/state/_system-config.md`.

## También actualiza [[_index|learnings/_index]]
Añade fila con: fecha, tarea, tipo, patrón, clusters, proyecto, señal de relevancia, cuándo cargar, **decay**, archivo.

## También actualiza [[_clusters]]
Si hay clusters nuevos o proyectos nuevos — añadir las filas correspondientes.

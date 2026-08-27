# Patrones de Sistemas Multi-Agente — Banco de Conocimiento

## Arquitectura de Dos Capas

**Patrón:** Separar `agents/` (documental/Obsidian) de `.opencode/agents/` (ejecutable).

**Beneficio:** Cero duplicación. La capa ejecutable referencia la documental. Reducción de tokens del ~42%.

**Implementación:**
- `agents/XX-nombre.md` → fuente de verdad, contexto rico, wikilinks, legible por humanos
- `.opencode/agents/ntizar-XX.md` → frontmatter YAML mínimo, instrucciones operativas, referencia a doc
- Regla: cambios en doc primero, luego ejecutar solo si cambia comportamiento

**Señal de éxito:** El archivo ejecutable dice "Lee agents/XX.md para contexto completo" en vez de duplicar.

## Índice Inteligente con Decay

**Patrón:** Un índice central (`_index.md`) con tabla de learnings que el orchestrator lee para decidir qué cargar.

**Beneficio:** En el 80% de casos no se abren archivos individuales. Carga bajo demanda filtrada por relevancia + decay.

**Implementación:**
- Tabla con columnas: fecha, tarea, tipo, patrón, clusters, señal de relevancia, cuándo cargar, decay
- Orchestrator calcula R(t) mentalmente al leer el índice
- Solo carga si R(t) > 0.3 (o > 0.5 bajo presión de tokens)

**Fórmula de Ebbinghaus:** `R(t) = a / (log(t+1))^b + c`

**Parámetros típicos:**
| Tipo | a | b | c | R(30d) | R(90d) | R(180d) |
|------|---|---|---|--------|--------|---------|
| permanente | — | — | 1.0 | 1.0 | 1.0 | 1.0 |
| lento | 0.7 | 0.8 | 0.25 | ~0.71 | ~0.58 | ~0.48 |
| normal | 0.8 | 1.2 | 0.15 | ~0.52 | ~0.37 | ~0.29 |
| rápido | 0.9 | 1.5 | 0.05 | ~0.30 | ~0.18 | ~0.12 |

## Flujo Adaptativo

**Patrón:** 3 flujos según complejidad (corto/medio/largo), todos obligatorios.

**Regla de oro:** Ningún agente se salta silenciosamente. Si no tiene trabajo, emite "PASS SIN HALLAZGOS" con motivo.

**Flujos:**
- Corto (4 agentes): CLASSIFY → IMPLEMENT → REVIEW → SYNTHESIZE
- Medio (7 agentes): + EXPLORE → PLAN → ARCHIVE
- Largo (10 agentes): + SPEC → CRITICIZE

## Agente Critic como Diferenciador

**Patrón:** Agente dedicado que valida "contra el mundo real", no contra la spec.

**Diferencia con Reviewer:**
- Reviewer: valida contra la spec (¿cumple lo que se pidió?)
- Critic: valida contra el mundo real (¿es lo que realmente necesitaba?)

**Política de degradación:** "Omitir antes que degradar" — si no hay modelo alto disponible, se omite el Critic en vez de ejecutarlo con un modelo inferior.

**Activación objetiva (patrón replicable):** 6 criterios automáticos:
1. Complejidad ≥ 4 (según clasificación)
2. ≥ 3 reintentos en cualquier fase del flujo
3. Entregables ≥ 3 archivos en tareas de tipo software
4. Tarea de tipo "software" con impacto alto
5. El reviewer emite WARNINGs (aunque el veredicto sea PASS)
6. El humano solicita explícitamente revisión profunda

Si ≥1 criterio se cumple → Critic activado automáticamente.
Si ninguno se cumple → Critic omitido con notificación al humano ("⚠️ CRÍTIC OMITIDO — Ningún criterio objetivo se cumplió").

**Regla de implementación:** El orchestrator evalúa los criterios al diseñar el flujo. Si el Critic se activa pero no hay modelo alto disponible → omitir, no degradar.

## Agente Librarian con Reaprendizaje Activo

**Patrón:** Agente de mantenimiento que detecta automáticamente cuándo actualizar skills basándose en learnings acumulados.

**Mecanismo:**
- Skills con sección `## Ciclo de reaprendizaje` se revisan automáticamente
- El librarian lee learnings de tipo `datos` en el índice
- Cuando ≥ 2 entradas del mismo tipo → ejecuta protocolo de actualización
- Actualiza tablas de patrones en el skill con nuevas filas

**Señal de que funciona:** El librarian reporta "Skills con reaprendizaje revisados: N" con filas añadidas.

**Señal de que no funciona:** El mecanismo existe pero ningún skill tiene la sección de ciclo de reaprendizaje.

## Portabilidad — Qué buscar

**Señal de alerta:** Rutas absolutas en archivos de configuración (`C:\Users\...`, `/home/usuario/...`)

**Señal de alerta:** Verificador de instalación que solo funciona en un SO

**Señal de alerta:** Variables de entorno hardcodeadas en el repo

**Buena señal:** Rutas relativas, placeholders, configuración que funciona en cualquier máquina

## Estado de Sesión — Limpieza

**Problema común:** Tareas "pendientes de archivar" que llevan meses sin actualizarse.

**Solución:** El orchestrator debería limpiar el estado al inicio de cada sesión o al completar ciclos.

**Señal de alerta:** `_session-state.md` con tareas pendientes desde hace 60+ días.

## Métricas de Sistema

**Lo que falta en la mayoría de sistemas:**
- Tokens gastados por ciclo
- Ratio PASS/FAIL del reviewer
- Reintentos promedio por fase
- Qué agentes son más/menos útiles
- Coste estimado por tipo de tarea

**Sin métricas, no hay forma de optimizar.**

## Templates — Qué hacer bien

**Spec template:**
- Límite de 700 tokens (si se supera, dividir la tarea)
- Verbos prohibidos en criterios ("mejorar", "optimizar" sin métrica)
- FUERA DE SCOPE obligatorio
- Criterios verificables sin interpretación subjetiva

**Learning template:**
- Estructura fija: decisión clave, patrón, qué funcionó, qué evitar
- Clusters dinámicos (no lista cerrada)
- Decay asignado con justificación
- Conexiones con otros learnings

## Multi-Skill Creation via Parallel Delegation

**Patrón:** Cuando hay que crear N archivos independientes (skills, configs, docs), usar `delegate_task` con 3 subagentes en paralelo, cada uno creando un batch de archivos.

**Cuándo usar:** N ≥ 6 archivos independientes, cada uno de extensión media (100-300 líneas), sin dependencias entre sí.

**Implementación:**
- Dividir el trabajo en 3 lots (máx paralelismo permitido por Hermes)
- Cada subagente recibe: carpeta destino, formato exacto del archivo, contenido específico
- Dar contexto suficiente pero no duplicado: los subagentes no tienen memoria del chat

**Beneficio:** 3x speedup vs secuencial. En este caso, 15 skills (2,867 líneas) creados en ~200s vs los ~600s que habría tomado secuencialmente.

**Riesgo:** Subagentes pueden divergir en estilo si el formato no está suficientemente especificado. Dar un template exacto en el `context` de cada tarea.

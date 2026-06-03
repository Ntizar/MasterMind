# Ntizar Mastermind v4.0 — Architecture Deep Dive

> **Framework de orquestación multi-agente con skills especializados por dominio.**
> Ejecutándose en Hermes Agent sobre NaN.builders con GitHub como repositorio.

---

## Overview

Ntizar Mastermind v4.0 es un sistema de orquestación multi-agente construido sobre:

- **Hermes Agent** — motor de ejecución, memoria persistente, `delegate_task` nativo
- **GitHub** — fuente de verdad, repositorio de código y documentación
- **NaN.builders** — infraestructura (MicroVM 1vCPU/2GB/20GB)

El sistema maneja cualquier tipo de tarea: software, investigación, estrategia, escritura, operaciones, conocimiento, creatividad y análisis de datos.

## Cambios clave respecto a v3.1

La versión anterior (v3.1) se construyó sobre **OpenCode + Obsidian**. Ambas plataformas son externas y no están disponibles en la VM actual. v4.0 es 100% Hermes-native:

| Aspecto | v3.1 (Legacy) | v4.0 (Actual) |
|---------|---------------|----------------|
| Motor de ejecución | OpenCode (Task tool) | **Hermes `delegate_task`** |
| Documentación | Obsidian (wikilinks) | **GitHub (Markdown plano)** |
| Agentes | 11 agentes genéricos | **1 orquestador + 143 skills** |
| Memoria | Ebbinghaus decay manual | **`memory` + `session_search`** |
| Arquitectura | 2 capas (docs + exec) | **1 capa (GitHub repo)** |
| Skills | 15 skills propios | **143 skills Hermes** |
| Comandos | 4 slash commands | **Lenguaje natural** |

## El Modelo de Especialización

### El problema con los agentes genéricos

En v3.1, cada agente era un **rol genérico**:

```
Orchestrator → Explorer → Planner → Spec-Writer → Implementer → Reviewer → Critic → Synthesizer → Archiver → Librarian
```

El Implementer no sabía de frontend, backend ni infra. Hacía todo y mal porque no tenía conocimiento especializado de ningún dominio.

### La solución: Skills especializados

En v4.0, cada skill es un **especialista en un dominio concreto**:

```
Koldo clasifica tarea → dominio: "frontend-dashboard"
  → Carga: aurora-design-system (especialista en CSS)
  → Carga: frontend-dashboard-patterns (especialista en APIs y fetch)
  → delegate_task con contexto completo
```

**Resultado:** Cada skill tiene conocimiento profundo de su dominio (APIs, unidades, pitfalles, patrones), no conocimiento genérico.

### Por qué funciona

1. **Conocimiento especializado** — Cada skill sabe todo sobre su dominio: endpoints, unidades de medida, errores comunes, patrones probados
2. **Carga bajo demanda** — No se cargan 143 skills indiscriminadamente, solo los del dominio relevante
3. **Actualización independiente** — Actualizar un skill no afecta a los demás
4. **Reutilización** — Un skill se usa en múltiples proyectos sin duplicación

## La Arquitectura en Capas

### Capa 1: Orquestador (Koldo)

Koldo es el orquestador principal, definido en `SOUL.md`. Su trabajo:

1. **Clasificar** — Dominio (software, github, frontend, etc.) + complejidad (1-4)
2. **Cargar skills** — `skill_view()` para los del dominio relevante
3. **Decidir flujo** — Directo (N1), simple (N2), paralelo (N3), orquestación (N4)
4. **Delegar** — `delegate_task` con contexto completo
5. **Integrar** — Verificar resultados, resolver conflictos
6. **Sintetizar** — Presentar resultados con human loop si aplica
7. **Archivar** — `memory` + `skill_manage` para aprendizaje

### Capa 2: Skills Especializados (143)

Organizados en 33 categorías, con prioridad de carga:

| Prioridad | Categoría | Skills | Cuándo cargar |
|-----------|-----------|--------|---------------|
| 🔥 Core | software-development | 17 | Siempre |
| 📦 Dominio | github, frontend, backend, infra, devops, data-science, creative | 56 | Cuando toca el dominio |
| 🗄️ Archivo | vision, mlops, stem, media, etc. | 70 | Solo si el usuario los pide |

### Capa 3: Memoria Persistente (Hermes-native)

| Sistema | Función | Reemplaza |
|---------|---------|-----------|
| `memory` | Hechos duraderos entre sesiones | Ebbinghaus decay + learnings |
| `session_search` | Búsqueda de sesiones pasadas | Índice de learnings |
| `skill_manage` | Crear/actualizar skills | Librarian + Archiver |

### Capa 4: GitHub (Fuente de verdad)

```
NtizarBrainMasterMind/
├── SOUL.md              ← Orquestador + principios
├── AGENTS.md            ← Arquitectura
├── skills/SKILLS-INDEX.md ← Índice de skills
├── human-loop-control/  ← Sistema de control
├── legacy/              ← v3.1 (referencia)
├── projects/            ← Proyectos activos
├── notes/               ← Notas de sesión
└── docs/                ← Documentación
```

## Flujo de Ejecución Detallado

### Nivel 1 — Directo

```
Tarea: "Busca errores en el último log"
→ Koldo usa terminal directamente
→ Presenta resultado
→ Fin
```

### Nivel 2 — Delegación Simple

```
Tarea: "Refactoriza el módulo de API del dashboard"
→ Koldo clasifica: dominio=frontend-dashboard, complejidad=2
→ Carga: frontend-dashboard-patterns, fetch-paralelo-fallos-parciales
→ Human loop: presenta plan → espera ✅
→ delegate_task(goal="refactorizar", context="...", toolsets=["terminal","file"])
→ Verifica resultado
→ Presenta resultado
```

### Nivel 3 — Delegación Paralela

```
Tarea: "Añade tests, refactoriza frontend y optimiza backend"
→ Koldo clasifica: dominios=múltiples, complejidad=3
→ Carga skills de cada dominio
→ Human loop: presenta plan → espera ✅
→ delegate_task(tasks=[
    {"goal": "frontend", ...},
    {"goal": "tests", ...},
    {"goal": "backend", ...}
  ])
→ Integra resultados
→ Verifica
→ Presenta
```

### Nivel 4 — Orquestación Completa

```
Tarea: "Crea feature completa: backend + frontend + docs + tests"
→ Koldo clasifica: complejidad=4
→ Human loop obligatorio: plan detallado → espera ✅
→ Planner subagent diseña estrategia
→ delegate_task paralelo para implementar
→ Reviewer valida
→ Koldo integra y merge
→ Presenta resultado
```

## Human Loop — Sistema de Control

### Cuándo se activa

| Criterio | Acción |
|----------|--------|
| >5 archivos modificados | Human loop obligatorio |
| Decisiones de arquitectura | Human loop obligatorio |
| Deploy a producción | Human loop obligatorio |
| Migraciones | Human loop obligatorio |
| Usuario lo solicita | Human loop obligatorio |

### El patrón exacto

```
FASE 1 — PLANIFICAR
Koldo:
  "📋 PLAN: [nombre del cambio]
   ARCHIVOS: [lista]
   CAMBIOS: [resumen]
   RIESGOS: [posibles problemas]
   ROLLBACK: [cómo revertir]
   
   ¿Aprobado? ✅ o feedback"

Humano: ✅

FASE 2 — IMPLEMENTAR
Koldo ejecuta con diffs visibles:
  "🔧 IMPLEMENTANDO
   ARCHIVO 1: cambio A → B
   ARCHIVO 2: cambio C → D
   
   ¿Aprobado? ✅ o feedback"

Humano: ✅

FASE 3 — VERIFICAR
Koldo verifica:
  "✅ VERIFICADO
   ARCHIVOS: N
   TESTS: PASS/FAIL
   BUILD: OK/FAIL
   
   ¿Aprobado? ✅"

Humano: ✅

FASE 4 — SINTETIZAR
Koldo presenta resultado final:
  "📊 RESULTADO
   HECHO: [resumen]
   SIGUIENTE: [próximos pasos]"
```

### Reglas del Human Loop

1. **Nunca silenciar** — terminar fase, presentar resultado, continuar inmediatamente
2. **Máximo 2 reintentos** — si falla 2x, escalar al humano
3. **Rollback siempre disponible** — `git reset --hard` si algo va mal
4. **Diffs siempre visibles** — nunca commit sin mostrar cambios
5. **Aprobación explícita** — ✅ o feedback, nunca asumir

## Memoria y Aprendizaje Continuo

### Cómo aprende Koldo

Después de cada tarea compleja (5+ tool calls):

1. **¿Merece skill?** → `skill_manage` para crear nuevo skill
2. **¿Merece nota?** → `notes/YYYY-MM-DD-titulo.md`
3. **¿Merece memoria?** → `memory` tool para hechos duraderos

### Qué guardar en memory

- Preferencias del usuario
- Datos del entorno (OS, herramientas instaladas)
- Convenciones del proyecto
- Patrones que funcionan

### Qué NO guardar en memory

- Progreso de tareas
- Resultados de sesiones
- IDs de PRs/commits/issues
- Datos que caducan en 7 días

## Diferencias con v3.1

### Flujo v3.1 (Legacy)

```
11 agentes genéricos:
Orchestrator → Explorer → Planner → Spec-Writer → Implementer → Reviewer → Critic → Synthesizer → Archiver → Librarian
         ↑                                                                                             ↑
    Checkpoints humanos (3)                                                                      Ebbinghaus decay
```

**Problemas:**
- Cada agente necesita su propio modelo (caro)
- Flujo lineal lento (cada agente espera al anterior)
- Checkpoints humanos rompen el flow
- Spec-Writer y Planner hacen trabajo duplicado
- Ebbinghaus decay es manual y frágil

### Flujo v4.0 (Actual)

```
1 orquestador + 143 skills:
Koldo → skill_view(dominio) → delegate_task → verifica → sintetiza
   ↑                              ↑                    ↑
Human loop (solo crítico)    Paralelo cuando        memory/skill_manage
                             es posible              para aprender
```

**Ventajas:**
- Un modelo para todo (qwen3.6)
- Delegación paralela cuando es posible
- Human loop solo en cambios críticos
- Sin espec-writer ni planner redundantes
- Memoria nativa de Hermes (más fiable)

## Stack Técnico

| Componente | Tecnología |
|------------|-----------|
| Modelo | qwen3.6 vía NaN (api.nan.builders/v1) |
| Infraestructura | MicroVM 1vCPU/2GB/20GB, NaN.builders |
| Repositorio | GitHub (https://github.com/Ntizar/NtizarBrainMasterMind) |
| Framework | Hermes Agent |
| Git auth | Token HTTPS (`GITHUB_TOKEN` en .env) |
| TTS | Álvaro (es-ES-AlvaroNeural) |
| CSS | Aurora Design System (Esios style) |
| Lenguaje | Español (castellano) |
| Deploy | NaN.builders + GitHub Pages |

---

**Autor:** David Antizar  
**Versión:** 4.0.0  
**Fecha:** 2026-06-03  
**Stack:** Hermes Agent + NaN.builders + GitHub

---
name: software-development
version: "2.0.0"
description: "Ecosistema completo de patrones de desarrollo de software: TDD, especificaciones, refactorización segura, code review, debugging sistemático, experimentos throwaway, documentación, optimización de datasets y patrones de código reutilizables."
tags: [software, development, tdd, refactoring, debugging, code-review, specification, spike, documentation, dataset]
---

# Software Development — Patrones Completos

## Resumen

Ecosistema completo de patrones de desarrollo de software organizado en 4 categorías:

### Método de Desarrollo
| Patrón | Descripción |
|--------|-------------|
| **Spec-Driven** | Construir software desde specs (PRD, planes, constituciones) |
| **TDD** | RED-GREEN-REFACTOR, tests antes que código |
| **Spike** | Experimentos throwaway para validar ideas antes de construir |
| **Multi-Iteration** | Mejoras 9009 en múltiples iteraciones, batches de 20 |

### Refactorización y Calidad
| Patrón | Descripción |
|--------|-------------|
| **Safe Refactoring** | Auditoría y refactorización segura sin romper producción |
| **Code Review** | Pre-commit: security scan, quality gates, auto-fix |
| **Google Eng Practices** | Code review profesional, cultura de code health |
| **Systematic Debugging** | 4-phase root cause debugging |

### Documentación y Traspaso
| Patrón | Descripción |
|--------|-------------|
| **Codebase Handoff** | Guías de mantenimiento para que cualquier persona trabaje en código |
| **Agent Skills Standard** | Formato y patrón para skills reutilizables de agentes IA |

### Patrones de Código y Datos
| Patrón | Descripción |
|--------|-------------|
| **Hash Index** | Índice hash para acceso O(1) en datasets grandes |
| **Lazy Loading** | Carga progresiva: solo lo que el usuario necesita, cuando lo necesita |
| **Sparse JSON** | 40-60% menos de tamaño en datasets grandes |
| **TopoJSON** | Compresión geográfica: 70% menos que GeoJSON |
| **Delegar no Comprimir** | Paralelizar tareas en subagentes en vez de compresiones contextuales |
| **Subagent Driven** | Ejecutar planes via delegate_task con review 2-etapas |
| **Geospatial Asset** | Plataformas SaaS de gestión de activos georreferenciados |
| **Leaflet Choropleth** | Mapa interactivo con miles de polígonos sin lag |
| **Map Optimization** | Optimización combinatoria (p-median, TSP) sobre mapas |
| **Pin Auth NodeJS** | Autenticación PIN + SQLite para apps Node.js |
| **Rebranding** | Rebranding sistemático de proyectos web completos |
| **Refactor NodeJS** | Monolítico → arquitectura modular por dominios |
| **TypeScript Cross-Module** | Tipos flexibles para engine+tests+frontend multi-módulo |

## Decision Guide

```
¿Qué necesitas?
├── ¿Nuevo proyecto? → Spec-Driven Development
├── ¿Calidad de código? → TDD + Code Review + Google Eng Practices
├── ¿Cambiar idea? → Spike (experimento throwaway)
├── ¿Mejorar código existente? → Safe Refactoring
├── ¿Debug? → Systematic Debugging (4 phases)
├── ¿Múltiples iteraciones? → 9009 Multi-Iteration
├── ¿Documentar? → Codebase Handoff
├── ¿Optimizar datos? → Hash Index + Lazy Loading + Sparse JSON
├── ¿Mapas? → Leaflet Choropleth + TopoJSON + Map Optimization
└── ¿Arquitectura? → Refactor NodeJS + TypeScript Cross-Module + Pin Auth
```

## Subsecciones Detail

### Spec-Driven Development
Basado en spec-kit de GitHub (113K⭐). Construir software desde specs (PRD, plans, constituciones) en vez de "vibe coding".

### TDD
Enforce RED-GREEN-REFACTOR. Tests antes que código. Ciclo: Write failing test → Make it pass → Refactor.

### Spike
Throwaway experiments para validar una idea antes de construir. No dejar rastro en el codebase principal.

### Safe Refactoring
Auditar y refactorizar proyectos existentes sin romperlos. Capturado del incidente MasterFit v3 donde la extracción de JS eliminó CDNs de Chart.js y Three.js.

### Code Review
Pre-commit review con security scan, quality gates y auto-fix. Verifica: seguridad, calidad, rendimiento, consistencia.

### Google Engineering Practices
Code review profesional, buenas prácticas de ingeniería, cultura de code health. 22.6K⭐ en GitHub.

### Systematic Debugging
4-phase root cause debugging: understand bugs before fixing. Phase 1: Reproduce. Phase 2: Isolate. Phase 3: Root cause. Phase 4: Fix + verify.

### Multi-Iteration (9009)
Patrón genérico para ejecutar mejoras en múltiples iteraciones. Análisis rápido, plan, implementación directa, verificación. Batches de 20.

### Codebase Handoff
Documentación de traspaso: leer codebase completo, explicar qué hace cada bloque, esquemas de datos, scripts, despliegue, errores conocidos.

### Agent Skills Standard
Formato y patrón para skills reutilizables de agentes IA. Inspirado en K-Dense-AI/scientific-agent-skills (26K⭐) con 142 skills científicas.

### Delegar no Comprimir
Paralelizar tareas en subagentes en vez de hacer compresiones de contexto con secuencias largas de herramientas.

### Subagent Driven Development
Ejecutar planes via delegate_task con 2-stage review. Planificar → Delegar → Review resultado → Iterar.

### Hash Index
Índice hash para acceso O(1) a registros en datasets grandes. Patrón IDX: array → objeto hash por key, merge de datasets, precomputación de métricas.

### Lazy Dataset Loading
Carga progresiva: solo lo que el usuario necesita, cuando lo necesita. Patrón con ensureDataset, cache de estado, merge en hash index, precarga idle. Reduce carga de 10s a 250ms.

### Sparse JSON
Formato JSON sparse para datasets grandes: 40-60% menos de tamaño. Clave-valores en arrays en vez de objetos repetidos.

### TopoJSON
Compresión geográfica: 70% menos de tamaño que GeoJSON, conversión en runtime, liberación de memoria. Para países, municipios, barrios.

### Leaflet Canvas Choropleth
Mapa choropleth interactivo con Leaflet + Canvas renderer. Miles de polígonos sin lag. 4 escalas de color, pane system, lazy dataset switching.

### Map Optimization
Herramientas de optimización combinatoria sobre mapas: p-median, p-center, TSP, problema de transporte. Heurísticas JS, integración ORS/OSRM.

### Geospatial Asset Platform
Plataformas SaaS de gestión de activos georreferenciados: municipal, hospitalario, logístico. PostgreSQL+PostGIS, Three.js, optimistic locking, audit trail.

### Pin Auth NodeJS
Autenticación con PIN para apps Node.js + SQLite (sql.js). Migración de BD, login con creación de usuario, PIN siempre visible.

### Rebranding
Rebranding sistemático de proyectos web: búsqueda y reemplazo en HTML, JS, server, README, Docker, favicon. Checklist + verificación post-cambio.

### Refactor NodeJS
Refactorizar proyecto Node.js monolítico a arquitectura modular por dominios. Separar por responsabilidad, crear límites claros.

### TypeScript Cross-Module
Tipos flexibles para engine+tests+frontend en proyectos multi-módulo. Declaration files, typecheck antes de push, prevención de errores CI.

## Referencias Cruzadas

- `web-research-fallback` → Cuando todas las búsquedas fallan
- `github-workflow` → GitHub auth, repos, PR lifecycle, code review

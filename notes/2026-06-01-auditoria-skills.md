# Auditoría Skills Mastermind — 2026-06-01

## Resumen Ejecutivo

Auditoría completa del ecosistema de skills de Hermes Agent en dos fases.

### Estado Final

| Métrica | Valor |
|---------|-------|
| Total skills | 155 |
| Categorías | 31 |
| Con tags | 155 (100%) |
| Sin tags | 0 (0%) |
| Sin versión | 3 |
| Sin description | 0 (0%) |
| >10KB | 37 (24%) |
| Con "Cuándo usar" | 48 (31%) |
| Sin "Cuándo usar" | 107 (69%) |
| Tamaño total | 5.6 MB |

### Evolución

| Fase | Skills | Tamaño | Eliminados |
|------|--------|--------|------------|
| Inicio | 205 | ~7.7 MB | — |
| Fase 1 | 153 | 5.7 MB | 52 |
| Fase 2 | 155 | 5.6 MB | 7 |
| **Total** | **155** | **5.6 MB** | **50 (24%)** |

### Reducción de tamaño: 2.1 MB (28%)

---

## Fase 1 — Eliminación de ruido

**Criterio:** Eliminar skills que NO enseñan patrones de diseño reutilizables.

### Eliminados (52):

**Project READMEs puros (14):**
- awesome-design-systems, data, devops, esios-dashboard, frontend, gis, ia, irpf-dibujitos, markitdown, metabase, nango, ntizar-aurora, ntizar-mastermind, orbitmixer, sistema-electrico-futuro, solmad, vibevoice

**CLI wrappers sin valor educativo (3):**
- (ver Fase 2)

**Skills duplicados o redundantes:**
- (ver Fase 2)

---

## Fase 2 — Mejora de calidad

**Criterio:** Cada skill debe enseñar un PATRÓN, no documentar APIs.

### Eliminados (7):

| Skill | Razón |
|-------|-------|
| software-development/debugging-hermes-tui-commands | Guía específica de proyecto Hermes |
| software-development/hermes-agent-skill-authoring | Meta-skill, documenta comandos |
| software-development/node-inspect-debugger | Wrapper CLI |
| software-development/python-debugpy | Wrapper CLI |
| software-development/plan | Demasiado delgado (2KB), solo trigger |
| frontend/knockstrap | Documentación librería específica |
| infraestructura/agent-skill-security | CLI wrapper |
| infraestructura/api-credentials | README/inventario |

### Renombrados a patrón genérico (4):

| Antes | Después |
|-------|---------|
| api-cliente-http-robusto | cliente-http-robusto |
| cache-multicapa-memoria-disco | cache-multicapa |
| env-validacion-estricta | validacion-config-estricta |
| seguridad-helmet-cors | seguridad-web-helmet-cors |

### Mejorados (frontend — 3):
- frontend-debugging-patterns → reestructurado con patrones, cuándo usar/NO usar
- frontend-error-boundaries → añadido cuándo usar/NO usar
- frontend-service-worker-pwa → código completado con estrategias de caché reales

### Creados como patrones (7):
- frontend-api-client-errores — patrón con reintentos, circuit breaker, timeouts
- frontend-config-mapa-colores — sistema de diseño con variables CSS semánticas
- frontend-estado-persistencia — clase PersistStore con serialización y expiración
- frontend-fechas-timezone-local — patrón de normalización UTC→local
- frontend-orquestacion-carga — clase DataOrchestrator con carga paralela
- frontend-sparklines-plotly — mini-gráficos con Plotly.js optimizados
- frontend-tabs-navegacion — clase TabController con lazy-loading y deep-linking

### Mejorados (software-development — 6):
- requesting-code-review — más conciso, añadido cuándo NO usar
- spike — añadido cuándo NO usar
- subagent-driven-development — comprimido a <10KB, añadido cuándo NO usar
- systematic-debugging — añadido cuándo NO usar
- test-driven-development — añadido cuándo NO usar
- writing-plans — añadido cuándo NO usar

### Mejorados (infraestructura — 6):
- cliente-http-robusto — factory function reutilizable, tabla de configuración
- cache-multicapa — clases MemoryCache, DiskCache, MultiLayerCache
- docker-multistage-produccion — añadido cuándo usar/NO usar
- validacion-config-estricta — factory function con JSDoc
- health-checks-metrics — diagrama arquitectónico de endpoints
- seguridad-web-helmet-cors — código en 4 bloques claros

---

## Problemas Detectados

### 🔴 Críticos (requieren atención inmediata):

1. **69% de skills sin "Cuándo usar"**: Solo 48/155 skills tienen sección de cuándo usar/no usar. Esto es el criterio principal de calidad.
2. **37 skills >10KB**: Suponen ruido excesivo en el prompt del agente. Los más grandes:
   - `autonomous-ai-agents/hermes-agent` — 49KB (DEBE refactorizarse con refs)
   - `autonomous-ai-agents/claude-code` — 34KB
   - `creative/humanizer` — 30KB
3. **3 skills sin versión**: Frontmatter incompleto.

### 🟡 Medios:

4. **Skills duplicados por categoría**: Algunas categorías tienen skills que se superponen (ej: `esios/esios-api` y `esios-complete`).
5. **37 skills >10KB**: Muchos podrían beneficiarse del patrón de refs (SKILL.md + references/).

### 🟢 Positivos:

6. **100% con tags**: Todos los skills son descubribles.
7. **0 sin description**: Todos tienen descripción.
8. **Reducción de 28% en tamaño**: De 7.7 MB a 5.6 MB.
9. **Eliminados 50 skills (24%)**: Todo ruido eliminado.

---

## Recomendaciones para Fase 3

1. **Prioridad alta:** Añadir sección "Cuándo usar / Cuándo NO usar" a los 107 skills que la tienen.
2. **Prioridad alta:** Refactorizar los 5 skills >20KB usando patrón de refs.
3. **Prioridad media:** Revisar duplicados entre `esios/esios-api` y `esios-complete`.
4. **Prioridad media:** Añadir versión a los 3 skills sin version.
5. **Prioridad baja:** Revisar que las categorías con 1 skill solo tengan sentido allí o deban migrarse.

---

## Cron de Mantenimiento

- **Frecuencia:** Mensual
- **Job:** `skill-maintenance`
- **Script:** `aurora-nightly` (jobs 1-4)

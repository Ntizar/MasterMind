# Ntizar Mastermind v4.0 — Índice de Skills Especializados

> **Carga bajo demanda.** Koldo identifica el dominio de la tarea y carga SOLO los skills relevantes.
> No se cargan todos los 143 skills indiscriminadamente.

## Cómo funciona

```
Tarea recibida → Koldo clasifica dominio → Carga skills del dominio → delegate_task
```

**Ejemplo:** "Refactoriza el frontend del dashboard"
1. Koldo clasifica → dominio: `frontend-dashboard-patterns`
2. Carga: `aurora-design-system`, `frontend-dashboard-patterns`
3. Delega: `delegate_task` con esos skills cargados

## Especialización por Dominio

### 🔥 Software Development (17 skills) — HIGH Priority

Skills que se cargan automáticamente en cada sesión de desarrollo.

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `subagent-driven-development` | Planificar → delegar → 2-stage review | Cualquier feature |
| `delegar-no-comprimir` | Paralelizar vs comprimir contexto | Tareas >5 tool calls |
| `9009-multi-iteration` | Mejoras iterativas en cualquier proyecto | Refactor, optimización |
| `systematic-debugging` | 4-phase root cause debugging | Bugs, errores |
| `google-eng-practices` | Code review profesional, cultura de código | Code review |
| `requesting-code-review` | Pre-commit: security scan, quality gates | Antes de commit |
| `test-driven-development` | RED-GREEN-REFACTOR | Features nuevas |
| `refactor-nodejs-monolith` | Modular por dominios | Refactor de monolito |
| `typescript-cross-module-patterns` | Tipos flexibles multi-módulo | TypeScript projects |
| `iterative-algorithm-refinement` | Prototipar → testear → refinar | Algoritmos |
| `spike` | Experimentos throwaway | Validar ideas |
| `web-audit` | Auditoría web completa | Análisis de web apps |
| `technical-audit-remediation` | Hallazgos por severidad | Corrección de bugs |
| `agent-skills-standard` | Formato y patrón de skills | Crear nuevos skills |
| `web-research-fallback` | Búsqueda sin CAPTCHA | Investigación web |

### 📦 GitHub (7 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `github-auth` | Token HTTPS, SSH keys | Setup, migración |
| `github-pr-workflow` | Branch, commit, PR, CI, merge | Cualquier PR |
| `github-code-review` | Diffs, inline comments | Review de PRs |
| `github-issues` | Crear, triage, label, assign | Gestión de issues |
| `github-repo-management` | Clone, fork, releases | Gestión de repos |
| `github-trending-research` | Exploración de GitHub Trending | Investigación |

### 📦 Frontend Dashboard (3 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `frontend-dashboard-patterns` | Cliente API robusto, orquestación de carga | Dashboards |
| `aurora-design-system` | CSS puro, 11 packs, 5 skins, 321 clases | UI con Aurora |
| `static-digest-pipeline` | Fetch API → normalizar → HTML estático | Digests estáticos |

### 📦 Backend (6 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `endpoints-dashboard-rest` | Summary, indicator, monthly, yearly | APIs REST |
| `fetch-paralelo-fallos-parciales` | Promise.all con fallos parciales | Múltiples endpoints |
| `servicio-resumen-consolidado` | Merge, stats, degradación de datos | Resúmenes |
| `node-esm-interop` | Cargar módulos legacy en ESM | Node.js projects |
| `conversion-unidades-api-externa` | Conversión de valores API | APIs externas |
| `forecast-montecarlo-escenarios` | Simulación Monte Carlo heurística | Análisis financiero |

### 📦 Infraestructura (6 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `cliente-http-robusto` | Reintentos, backoff exponencial, jitter | Consumir APIs |
| `docker-multistage-produccion` | Node.js non-root, health checks | Docker |
| `health-checks-metrics` | Readiness probes, Prometheus | Apps en producción |
| `seguridad-web-helmet-cors` | CSP, HSTS, CORS whitelist | Apps web |
| `validacion-config-estricta` | Env vars, exit early, defaults tipados | Configuración |
| `cache-multicapa` | Memoria + disco, TTL, hit rate | Caché |

### 📦 DevOps (10 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `devops-operations` | Deploy NaN, cron jobs, scripts | Operaciones NaN |
| `aurora-nightly` | Mejora continua nocturna | Pipeline Aurora |
| `koldo-setup` | Sincronización repos, config | Setup Koldo |
| `static-digest-pipeline` | Fetch → normalizar → HTML | Digests |
| `inventario-apis-procesamiento` | Procesar 10K+ APIs | Análisis de APIs |
| `layered-agent-architecture` | Patrón L0-pure → L3-system | Arquitectura de agentes |
| `nango-integrations` | 800+ APIs integrations | Integraciones |
| `postgres-mcp-pro` | PostgreSQL como MCP server | Bases de datos |
| `aurora-nightly-pipeline` | Lint, format, deploy automático | Pipeline |
| `koldo-setup` | Configura y mantiene Koldo | Setup |

### 📦 Data Science (8 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `sistemaelectricofuturo-v2` | Simulador eléctrico 2026-2035 | Análisis energético |
| `sistemaelectricofuturo` | Simulador horario eléctrico | Análisis energético |
| `sistema-electrico-simulador` | Simulador interactivo | Análisis energético |
| `solar-shadow-computation` | Sombras solares con Web Workers | Análisis solar |
| `monte-carlo-stock-simulator` | Simulación Monte Carlo bursátil | Análisis financiero |
| `geoai-city2graph-pattern` | City2Graph para datos geoespaciales | GeoAI |
| `rail-lidar-qa-mvp` | Validación calidad LiDAR | QA LiDAR |
| `jupyter-live-kernel` | Python iterativo con kernel live | Análisis interactivo |

### 📦 Creative (22 skills) — MEDIUM Priority

| Skill | Especialización | Cuándo cargar |
|-------|----------------|---------------|
| `liquid-glass-css` | Efecto glass Aurora | UI con glass |
| `architecture-diagram` | Diagramas dark SVG/HTML | Documentación |
| `ascii-art` | Pyfiglet, cowsay, ASCII | Arte ASCII |
| `excalidraw` | Diagramas hand-drawn JSON | Diagramas |
| `popular-web-designs` | 54 design systems reales | Diseño web |
| `manim-video` | Animaciones 3Blue1Brown | Videos |
| `p5js` | Sketches gen art, shaders | Arte generativo |
| `humanizer` | Humanizar texto, quitar AI-isms | Redacción |

### 📦 Otros dominios (cargar bajo demanda)

| Dominio | Skills | Cuándo cargar |
|---------|--------|---------------|
| **ESIOS** | 3 skills | Análisis mercado eléctrico |
| **Vision** | 4 skills | Computer vision, satélites |
| **MLOps** | 9 skills | ML training, serving, evaluation |
| **STEM** | 30+ skills | Educación STEM |
| **Media** | 6 skills | TTS, YouTube, música |
| **Productividad** | 2 skills | Calendar, Yuanbao |
| **Herramientas** | 5 skills | PDF, video, OCR |

## Carga de Skills

### Patrón estándar

```python
# 1. Koldo identifica el dominio
# 2. Carga los skills MEDIUM del dominio
skill_view(name='frontend-dashboard-patterns')
skill_view(name='aurora-design-system')

# 3. Delega con esos skills cargados
delegate_task(
    goal="Refactorizar frontend",
    context="Contexto completo del proyecto",
    toolsets=["terminal", "file"]
)
```

### Prioridad de carga

1. **HIGH (Core)** — Se cargan automáticamente en cada sesión
   - `subagent-driven-development`
   - `delegar-no-comprimir`
   - `koldo-orchestration`
   - `github-workflow`
   - `systematic-debugging`

2. **MEDIUM (Dominio)** — Se cargan con `skill_view()` cuando toca ese tema
   - Todos los skills de los dominios listados arriba

3. **LOW (Archivo)** — Solo se cargan si el usuario los pide
   - Skills nicho, especializados

## Reglas de Carga

1. **NUNCA cargar todos los 143 skills** — solo los del dominio relevante
2. **Cargar MEDIUM con `skill_view()`** — no cargar HIGH (ya están en SOUL.md)
3. **Cargar LOW solo si el usuario los pide** — no adivinar
4. **Un skill por sesión como máximo** — si hay conflicto, cargar el más relevante
5. **Actualizar skill si está desactualizado** — `skill_manage(action='patch')` inmediatamente

## Migración desde v3.1

| v3.1 Legacy | v4.0 Hermes-Native |
|---|---|
| `agents/00-orchestrator.md` | `SOUL.md` (Koldo) |
| `agents/02-explorer.md` | `file` + `search_files` tools |
| `agents/03-planner.md` | `delegate_task` con Planner |
| `agents/05-implementer.md` | `delegate_task` con Implementer |
| `agents/06-reviewer.md` | `delegate_task` con Reviewer |
| `agents/07-critic.md` | `delegate_task` con Critic |
| `agents/learnings/` | `memory` + `session_search` |
| `skills/nan-builders-deploy.md` | `devops-operations` skill |
| `skills/multi-agent-orchestration.md` | `koldo-orchestration` skill |
| `skills/intelligent-index-loading.md` | Prioridad de carga (esta tabla) |

---

**Autor:** David Antizar  
**Versión:** 4.0.0  
**Fecha:** 2026-06-03

# Auditoría del Sistema Mastermind — Skills & Hermes Agent
**Fecha:** 2026-06-01  
**Versión:** 1.0  
**Objetivo:** Evaluar calidad, ruido y escalabilidad del ecosistema de 205 skills

---

## 1. Resumen Ejecutivo

| Métrica | Valor | Estado |
|---------|-------|--------|
| Total de skills | 205 | ⚠️ Alto para agente personal |
| Skills sin frontmatter | 0 | ✅ |
| Skills sin versión | 0 | ✅ |
| Skills con descripción vacía | 0 | ✅ |
| Skills duplicados (nombre) | 0 | ✅ |
| Skills >50KB | 1 | ⚠️ hermes-agent (49KB) |
| Skills >30KB | 4 | ⚠️ |
| Skills con rutas de proyecto | 13 | ⚠️ |
| Skills que no son patrones reutilizables | ~12 | 🔴 |
| Skills sin tags | 81 (39%) | ⚠️ |

**Puntuación global: 6/10** — El sistema funciona pero tiene problemas de calidad y ruido que impedirán escalar a miles de skills.

---

## 2. Problemas Críticos 🔴

### 2.1. Skills que NO son patrones reutilizables (12 skills)

Estos son **READMEs de proyectos específicos** disfrazados de skills. Un skill debe contener un patrón reutilizable, no la documentación de un proyecto concreto.

| Skill | Problema | Acción recomendada |
|-------|----------|-------------------|
| `esios-dashboard` | README del proyecto esios-work (47KB) | Mover a notes/, eliminar como skill |
| `nan-dashboard-deploy` | Deploy específico de nan-dashboard (20KB) | Mover a notes/, eliminar como skill |
| `nan-spaces-portfolio` | Deploy específico de nan-dashboard (14KB) | Mover a notes/, eliminar como skill |
| `9009-mejora-continua` | Pipeline específico (37KB) | Ya existe `9009-multi-iteration` como patrón genérico |
| `market-electric-report` | Script específico (14KB) | Mover a notes/, eliminar como skill |
| `bicimad-api` | API específica de Bicimad | Mover a notes/, eliminar como skill |
| `familia-tree-editor` | Editor específico | Mover a notes/, eliminar como skill |
| `empleady-employee-profitability` | Simulador específico | Mover a notes/, eliminar como skill |
| `irpf-calculator-visual` | Calculadora específica | Mover a notes/, eliminar como skill |
| `orbitmixer-satellite-compare` | Comparador específico | Mover a notes/, eliminar como skill |
| `metalhoverlab-cursor-relief` | Efecto visual específico | Mover a notes/, eliminar como skill |
| `voynich-structural-analysis` | Análisis específico de manuscrito | Mover a notes/, eliminar como skill |

**Impacto:** Estos 12 skills ocupan ~180KB de contexto innecesario y contaminan la búsqueda de skills relevantes.

### 2.2. Skills duplicados / redundantes

#### Grupo ESIOS (5 skills → 1 skill)
- `esios-api` — Guía de API
- `esios-dashboard` — README del proyecto (ver 2.1)
- `esios-indicators-correct` — IDs correctos
- `esios-dashboard-troubleshooting` — Troubleshooting
- `esios-nan-deploy` — Deploy en NaN

**Propuesta:** Unificar en un solo skill `esios-complete` con secciones claras.

#### Grupo NaN Deploy (4 skills → 1 skill)
- `nan-deploy` — Guía general
- `nan-deploy-guide` — Guía de inicio
- `nan-dashboard-deploy` — Deploy específico (ver 2.1)
- `nan-spaces-portfolio` — Portfolio específico (ver 2.1)

**Propuesta:** Unificar en `nan-deploy-guide` + eliminar los específicos.

#### Grupo GitHub (6 skills → 2 skills)
- `github-auth`, `github-repo-management`, `github-knowledge-repo`, `github-pr-workflow`, `github-issues`, `github-code-review`

**Propuesta:** Unificar en `github-workflow` (general) + `github-knowledge-repo` (específico).

#### Grupo Frontend (7 skills → 2 skills)
- `frontend-api-client-errores`, `frontend-orquestacion-carga`, `frontend-estado-persistencia`, `frontend-fechas-timezone-local`, `frontend-tabs-navegacion`, `frontend-sparklines-plotly`, `frontend-config-mapa-colores`

**Propuesta:** Unificar en `frontend-dashboards` (patrón completo) + `frontend-utilities` (utilidades sueltas).

#### Grupo Infraestructura (6 skills → 2 skills)
- `docker-multistage-produccion`, `env-validacion-estricta`, `health-checks-metrics`, `seguridad-helmet-cors`, `api-cliente-http-robusto`, `cache-multicapa-memoria-disco`

**Propuesta:** Unificar en `nodejs-production` (patrón completo) + `security-hardening` (seguridad específica).

### 2.3. Skills con contenido excesivo (>30KB)

Estos skills inflan el contexto del agente y ralentizan la búsqueda:

| Skill | Tamaño | Líneas | Problema |
|-------|--------|--------|----------|
| `hermes-agent` | 49KB | 1096 | Skill del framework, debería usar refs pattern |
| `esios-dashboard` | 47KB | 877 | README de proyecto (ver 2.1) |
| `9009-mejora-continua` | 37KB | 745 | Pipeline específico (ver 2.1) |
| `claude-code` | 34KB | 612 | Delegación específica |
| `humanizer` | 30KB | 578 | Demasiados ejemplos |

**Propuesta:** Aplicar el patrón de refs para skills >20KB.

---

## 3. Problemas de Calidad ⚠️

### 3.1. SOUL.md vs Memory duplicación

6 de los 11 items en Memory ya están en SOUL.md:
- ESIOS / convertEsiosValue / buildSummary / charts / SOUL.md / 9009 multi-iteration

**Impacto:** El agente recibe la misma información dos veces, desperdiciando tokens del prompt.

**Propuesta:** Quitar de SOUL.md lo que ya está en Memory, o viceversa. SOUL.md debería contener solo identidad y reglas fundamentales.

### 3.2. mastermind/SKILL.md demasiado grande (22KB)

El archivo `mastermind/SKILL.md` es un umbrella de 22KB con 256 líneas. Contiene descripciones de todos los skills propios de Mastermind. Esto es innecesario — el sistema de skills de Hermes ya indexa los nombres y descripciones individualmente.

**Propuesta:** Reducir a un índice mínimo de 200-300 líneas con solo nombres y descripciones cortas.

### 3.3. 81 skills sin tags (39%)

Los tags ayudan al sistema de skills a filtrar y cargar solo los relevantes. Nearly 40% de skills no tienen tags, lo que reduce la precisión de la carga.

**Propuesta:** Añadir tags a todos los skills sin tags. Mínimo 3 tags por skill.

### 3.4. Skills con rutas de proyecto hardcodeadas

13 skills contienen rutas absolutas de proyecto (`/persist/nan-dashboard/`, `/root/workspace/esios-work`, etc.). Esto los hace no reutilizables y contaminan el contexto con información de un proyecto específico.

**Propuesta:** Eliminar las rutas absolutas y reemplazarlas por variables de entorno o referencias genéricas.

---

## 4. Análisis de Categorías

| Categoría | Skills | Calidad |
|-----------|--------|---------|
| creative | 20 | ⚠️ Muchas son project-readmes |
| software-development | 12 | ✅ Buena calidad |
| mlops | 10 | ✅ Buena calidad |
| productivity | 10 | ⚠️ Muchas son CLI wrappers |
| frontend | 9 | ⚠️ Fragmentadas, deberían unificarse |
| github | 8 | ⚠️ Demasiadas, deberían unificarse |
| media | 7 | ✅ Buena calidad |
| infraestructura | 7 | ⚠️ Fragmentadas |
| devops | 6 | ✅ Buena calidad |
| backend | 6 | ⚠️ Fragmentadas |
| mastermind | 16 (con subdirs) | ⚠️ Mezcla propios y externos |
| vision | 3 | ✅ Buena calidad |
| data-science | 4 | ⚠️ `sistemaelectricofuturo` es proyecto específico |

---

## 5. Skills que NO deberíamos tener

### 5.1. Project READMEs como skills (eliminar)
Estos son documentación de proyectos, no patrones reutilizables. Deberían estar en `notes/` o en el README del repo, no como skills.

### 5.2. CLI Wrappers (eliminar o fusionar)
Skills que solo documentan cómo usar una CLI con `curl` no aportan valor como skills. El agente ya sabe usar curl. Ejemplos:
- `airtable` — solo curl commands
- `himalaya` — solo CLI usage
- `linear` — solo GraphQL + curl
- `notion` — solo ntn CLI
- `spotify` — solo CLI usage
- `xurl` — solo CLI usage
- `gif-search` — curl + jq
- `arxiv` — solo API calls
- `blogwatcher` — solo CLI usage
- `polymarket` — solo API calls
- `maps` — solo API calls
- `nano-pdf` — solo CLI usage
- `powerpoint` — solo CLI usage
- `obsidian` — solo CLI usage
- `caldav-calendar` — solo CLI usage
- `google-workspace` — solo CLI usage
- `teams-meeting-pipeline` — solo CLI usage
- `ocr-and-documents` — solo CLI usage
- `openhue` — solo CLI usage
- `minecraft-modpack-server` — solo CLI usage
- `pokemon-player` — solo CLI usage
- `huggingface-hub` — solo CLI usage
- `llama-cpp` — solo CLI usage
- `metabase` — solo descripción
- `nango` — solo descripción
- `vibevoice` — solo descripción

**Propuesta:** Estos skills no añaden valor. El agente ya sabe usar curl y las CLIs. Eliminarlos o fusionar en un skill genérico `cli-tools-reference`.

### 5.3. Skills de autores externos (evaluar)
81 skills tienen autores externos (Orchestra Research, Hermes Agent + Teknium, comunidad, etc.). Estos fueron importados automáticamente de repos de skills abiertos. Muchos son útiles, pero algunos son:
- Demasiado genéricos (no añaden nada sobre lo que el agente ya sabe)
- Demasiado específicos de un framework (solo útiles si el agente usa ese framework)
- Mal mantenidos (descripciones obsoletas)

**Propuesta:** Revisar manualmente cada skill externo y eliminar los que no aporten valor.

---

## 6. Plan de Acción

### Fase 1: Limpieza rápida (1-2h)
1. **Eliminar 12 project-readmes** → mover a `notes/`
2. **Eliminar ~25 CLI wrappers** → no aportan valor
3. **Resultado esperado:** 205 → ~170 skills, -180KB de contexto

### Fase 2: Unificación (2-3h)
4. **Unificar grupo ESIOS** (5 → 1)
5. **Unificar grupo NaN Deploy** (4 → 1)
6. **Unificar grupo GitHub** (6 → 2)
7. **Unificar grupo Frontend** (7 → 2)
8. **Unificar grupo Infraestructura** (6 → 2)
9. **Resultado esperado:** 170 → ~155 skills

### Fase 3: Optimización (2-3h)
10. **Reducir mastermind/SKILL.md** a <1KB
11. **Limpiar SOUL.md** de duplicados con Memory
12. **Añadir tags** a los 81 skills sin tags
13. **Eliminar skills >30KB** con patrón de refs
14. **Resultado esperado:** Contexto del agente reducido en ~50%

### Fase 4: Mantenimiento continuo
15. **Crear skill `skill-audit-pattern`** para auditorías periódicas
16. **Añadir regla en SOUL.md:** "Solo crear skills que sean patrones reutilizables"
17. **Métricas mensuales:** contar skills, tamaño total, duplicados

---

## 7. Criterios para Crear un Nuevo Skill

Antes de crear un skill, aplicar el filtro:

1. **¿Es un patrón reutilizable?** → Si es específico de un proyecto → NO es skill
2. **¿Aporta algo nuevo?** → Si solo documenta un CLI tool → NO es skill
3. **¿Es compacto?** → Si es >5KB → usar refs pattern
4. **¿Tiene tags?** → Mínimo 3 tags descriptivos
5. **¿Es necesario?** → Si ya existe un skill similar → fusionar

---

## 8. Estado Esperado Final

| Métrica | Actual | Objetivo |
|---------|--------|----------|
| Total skills | 205 | ~150 |
| Tamaño total | ~3.5MB | ~1.5MB |
| Skills sin tags | 81 (39%) | 0 (0%) |
| Skills project-readmes | 12 | 0 |
| Skills >30KB | 4 | 0 |
| Skills con rutas hardcodeadas | 13 | 0 |
| Duplicación SOUL.md/Memory | 6 items | 0 |

---

*Auditoría generada automáticamente por Mastermind el 2026-06-01.*

# CHANGELOG

Todos los cambios notables de este proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y el proyecto usa [Semantic Versioning](https://semver.org/lang/es/).

## [4.1.0] — 2026-07-01

### 🏗️ Arquitectura
- **ChromaDB operativo** con 240 skills indexados semánticamente vía qwen3-embedding
- **Búsqueda semántica** — consultar-skills.py genera embedding de la consulta y busca por similitud coseno
- **Indexación automática** — indexar-skills.py corre cada domingo 04:00 UTC vía cron Hermes
- **Threshold 0.25** — filtro de relevancia para evitar ruido en contexto

### 🔄 Scripts del sistema
- **`consultar-skills.py`** — Búsqueda semántica en ChromaDB con query embedding y ranking por coseno
- **`indexar-skills.py`** — Indexación batch de todos los SKILL.md, embeddings vía NaN API, lotes de 10
- **`skill-lifecycle.py`** — Analiza uso real vía git log + notas (30 días), re-clasifica en HIGH/MEDIUM/LOW
- **`skill-learning.sh`** — Cola priorizada de ~120 skills del hub Hermes, instala 1 por ejecución
- **`backup-hermes-memory.sh`** — Backup con push automático a GitHub (descomentado)

### 📚 Documentación
- **README.md** reescrito — refleja la realidad: 240 skills, ChromaDB, Mastermind, sin marketing "framework open-source"
- **AGENTS.md** actualizado — flujo real con búsqueda semántica, 240 skills, cron jobs activos
- **Nuevo HTML explicativo** — ntizar-brain-mastermind-explained.html con diseño Aurora

### 🐛 Fixes
- **backup-hermes-memory.sh** — `git push` descomentado (antes solo commit, nunca subía a GitHub)
- **Directorios faltantes** — `learning/` y `config/` creados (skill-lifecycle.py escribía a rutas que no existían)
- **README decía "143 skills"** — corregido a 240
- **README decía "Koldo"** — corregido a Mastermind
- **README decía "framework open-source"** — corregido a sistema personal

### 🤖 Cron Jobs Hermes (10 activos)
- Verificados y documentados en AGENTS.md

## [4.0.3] — 2026-06-04

### ✨ Añadido
- **`test-suite.sh`** — 68 tests funcionales: estructura, contenido, consistencia, seguridad, links
- **`skills/README.md`** — Documentación de los 8 dominios y 80+ skills del sistema
- **`system-health.sh`** — Dashboard de salud: git, archivos, docs, tokens, tests, disco
- **Mobile-first CSS** — touch-friendly, stacked layout, tap targets 44px, responsive hero

### 🔄 Cambiado
- **`verify-system.sh`** — De 11 a 27 checks (contenido + consistencia + JSON válido)
- **Mobile experience** — Hero, feature grid, evolution cards, CTA buttons, footer optimizados para táctil
- **audit-v4.0.md** — Puntuación final: 9.0/10 (+3.4 desde v4.0.0)

## [4.0.2] — 2026-06-04

### ✨ Añadido
- **OG meta tags** — Open Graph y Twitter Card para social sharing profesional
- **Favicon SVG** — emoji 🧠 como favicon inline
- **Sección Evolución v3→v4** — comparativa visual con cards de arquitectura, memoria, routing y deploy
- **Card hover effects** — lift + shadow en todas las cards con transiciones suaves
- **Staggered scroll animations** — stats y cards aparecen con efecto escalonado
- **Footer con navegación** — links a GitHub, Contribuir, Issues, Dashboard Tokens
- **`verify-system.sh` v2** — de 11 a 27 checks: contenido, consistencia, JSON válido
- **`legacy-v3.1.tar.gz`** — backup comprimido de legacy/ (336KB → 65KB)
- **2 notas de aprendizaje** — consolidación documental y verify funcional

### 🔄 Cambiado
- **SOUL.md** — consolidado: 98→84 líneas, sin duplicación con AGENTS.md/README.md
- **AGENTS.md** — compacto: 81→67 líneas, solo referencia rápida
- **README.md** — limpio: 273→153 líneas, vista de usuario sin overlap
- **README_EN.md** — expandido con resumen técnico completo para contribuidores internacionales
- **Nav de landing** — "Agentes"→"Características", añadido enlace "Tokens"
- **tokens/index.html** — fallback data sincronizado con las 3 sesiones del JSON
- **audit-v4.0.md** — re-evaluación post-correcciones: 5.6→7.4/10

### 🗑️ Eliminado
- Duplicación entre SOUL.md, AGENTS.md y README.md (niveles, human loop, arquitectura)

## [4.0.1] — 2026-06-04

### ✨ Añadido
- **`tokens/tokens-log.json`** — Datos de tokens separados del HTML para carga dinámica
- **Sección HERO completa** en landing page — badge v4.0, KPIs, CTAs
- **Sección CARACTERÍSTICAS completa** — 4 cards + pipeline visual del flujo
- **12 Reglas actualizadas** a conceptos v4.0 (orquestador, skills, memory, human loop)

### 🔄 Cambiado
- **Landing page** — secciones HERO y CARACTERÍSTICAS reescritas (estaban vacías)
- **12 Reglas** — reemplazadas reglas v3.1 (agentes, Ebbinghaus, clusters) por v4.0
- **Dashboard de tokens** — carga dinámica desde `tokens-log.json` con fallback, innerHTML sanitizado
- **README.md** — roadmap actualizado, 12 reglas sincronizadas con index.html
- **SOUL.md** — eliminada referencia a `docs/` inexistente
- **verify-system.sh** — eliminado check de `docs/`, añadido check de `CHANGELOG.md`
- **pages.yml** — eliminados excludes obsoletos (`docs/`, `verify-system.bat`), añadido `audit-v4.0.md`
- **meta description** — eliminada referencia a "memoria Ebbinghaus"
- **CSS** — eliminada clase `.ebbinghaus-eq` obsoleta
- **(L)** → ❤️ en todos los archivos del repo

### 🗑️ Eliminado
- **`learning-platform/`** movido a `legacy/learning-platform/` — todo el código era v3.1 (Obsidian+OpenCode)

## [4.0.0] — 2026-06-03

### 🎯 Breaking Changes
- **Migrado de OpenCode+Obsidian a Hermes Agent+GitHub** — todo el sistema funciona ahora con herramientas nativas de Hermes
- **11 agentes genéricos → 1 orquestador + 143 skills especializados** — especialización por dominio reemplaza agentes de rol
- **Todo OpenCode movido a `legacy/`** — `.opencode/`, `agents/`, `skills/` ahora bajo `legacy/` (solo referencia, no se ejecuta)

### ✨ Añadido
- **`SOUL.md`** — Definición del orquestador único con principios, arquitectura y reglas
- **`AGENTS.md`** — Visión general con niveles de ejecución y modelo de especialización
- **`skills/SKILLS-INDEX.md`** — Índice completo de 143 skills Hermes organizados por dominio con prioridades
- **`human-loop-control` skill** — Sistema de puertas de aprobación para cambios críticos (>5 archivos, decisiones de arquitectura, deploy a producción)
- **Modelo de especialización por dominio** — 8 dominios de skills (software, github, frontend, backend, infra, devops, data-science, creative) con carga HIGH/MEDIUM/LOW
- **`legacy/README.md`** — Documentación del sistema legacy v3.1

### 🔄 Cambiado
- **221 archivos → 136 archivos** — 108 legacy + 28 nuevos
- **2 capas (docs+exec) → 1 capa (GitHub Markdown)** — sin wikilinks de Obsidian ni YAML de OpenCode
- **Ebbinghaus decay manual → Hermes `memory` + `session_search`** — persistencia nativa
- **15 skills propios → 143 skills Hermes** — carga bajo demanda por dominio
- **4 comandos slash → lenguaje natural** — Koldo entiende lenguaje natural
- **Multi-modelo por agente → modelo único (qwen3.6)** — gestión de modelos simplificada
- **README.md** — actualizado para v4.0 con tablas comparativas
- **docs/ARCHITECTURE.md** — reescrito completo con modelo de especialización, human loop, sistema de memoria
- **index.html** — landing page actualizada a v4.0 (1 orquestador + 143 skills, sin referencias a v3.x)

### 🗑️ Eliminado
- **Dependencia de OpenCode** — sin `.opencode/agents/` ni `.opencode/commands/` en código activo
- **Dependencia de Obsidian** — sin `agents/` con wikilinks en código activo
- **Sistema de Ebbinghaus decay** — reemplazado por memoria nativa de Hermes
- **Clasificador subagente** — clasificación integrada en Koldo
- **Spec-Writer subagente** — specs integradas en `delegate_task` goal
- **Planificador subagente** — planificación integrada en decisión de Koldo

### 📊 Resumen de Migración

| Aspecto | v3.1 | v4.0 |
|---------|------|------|
| Plataforma | OpenCode + Obsidian | Hermes Agent + GitHub |
| Agentes | 11 genéricos | 1 orquestador + 143 especializados |
| Skills | 15 propios | 143 Hermes (carga bajo demanda) |
| Memoria | Ebbinghaus manual | `memory` + `session_search` |
| Archivos | 221 (2 capas) | 136 (1 capa) |
| Comandos | 4 slash | 0 (lenguaje natural) |

## [3.1.0] — 2026-03-26

### ✨ Añadido
- Sistema multi-agente completo con 11 agentes y 4 comandos slash
- Memoria con decaimiento de Ebbinghaus
- Routing de modelos por tarea
- GitHub Pages con landing page

### 🔄 Cambiado
- Migración de carpeta local a repositorio GitHub
- README en español como idioma principal
- SVG banner desde design system

### 🗑️ Eliminado
- Dependencia de GitHub CLI (gh)
- Autenticación SSH → token HTTPS
- Scripts Windows (verify-system.bat, start.bat)

---

**Autor:** David Antizar
**Versión:** 4.1.0
**Fecha:** 2026-07-01
**Stack:** Hermes Agent + NaN.builders + GitHub + ChromaDB
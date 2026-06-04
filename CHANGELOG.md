# CHANGELOG

Todos los cambios notables de este proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) y el proyecto usa [Semantic Versioning](https://semver.org/lang/es/).

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
**Versión:** 4.0.0
**Fecha:** 2026-06-04
**Stack:** Hermes Agent + NaN.builders + GitHub
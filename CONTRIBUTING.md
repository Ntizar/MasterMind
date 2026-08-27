# Cómo contribuir a Ntizar Mastermind

Gracias por querer contribuir. Este proyecto es un sistema de orquestación multi-agente que se ejecuta en **Hermes Agent** sobre **NaN.builders** con **GitHub** como repositorio.

## 🧠 ¿Cómo funciona?

El sistema tiene 1 orquestador (Mastermind) que clasifica tareas y delega a 143 skills especializados por dominio. Todo está documentado en Markdown plano en este repo.

## 📦 Añadir un skill

Los skills son playbooks especializados que Mastermind carga bajo demanda. Para crear uno:

1. Escribe el skill en formato `SKILL.md` con YAML frontmatter
2. Míralo a `agent/skills/<categoria>/<nombre>/`
3. Si el dominio es nuevo, regístralo en la prioridad de carga

**Buenos candidatos:** DevOps, data science, testing, diseño, análisis de datos, etc.

## 🔧 Mejorar documentación

- **SOUL.md** — orquestador principal, reglas, principios
- **AGENTS.md** — arquitectura, niveles de ejecución
- **README.md** — visión general del proyecto

## 🐛 Reportar bugs

Abre un issue en GitHub describiendo:
- Qué esperabas que pasara
- Qué pasó realmente
- Contexto (modelo, sesión, tarea)

## 🌐 Entorno

- **Modelo:** qwen3.6 vía NaN (api.nan.builders/v1)
- **Infra:** MicroVM 1vCPU/2GB/20GB, NaN.builders
- **Repositorio:** GitHub (https://github.com/Ntizar/NtizarBrainMasterMind)
- **Framework:** Hermes Agent
- **Lenguaje:** Español (castellano)

## 📝 Guías

- TODO en castellano — NUNCA inglés en repos, scripts, cron, informes
- Cambios >5 archivos → human loop (presentar plan, esperar ✅)
- Nunca borrar del repo — solo crear o modificar
- Cada aprendizaje importante → commit al repo

## ❓ Preguntas

Abre un issue o empieza una discusión. Estamos aquí para ayudarte.

---

**Hecho con ❤️ por David Antizar**
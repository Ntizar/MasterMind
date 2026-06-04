<h1 align="center">Ntizar Mastermind</h1>

<p align="center">
  <strong>Un framework open-source de orquestación multi-agente con memoria persistente,<br>skills especializados y ejecución en la nube.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/NtizarBrainMasterMind/">🌐 Web</a> ·
  <a href="#inicio-rápido">Inicio Rápido</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0-blue?style=flat-square" alt="Version 4.0"/>
  <img src="https://img.shields.io/badge/orquestador-1-purple?style=flat-square" alt="1 Orquestador"/>
  <img src="https://img.shields.io/badge/skills-143-orange?style=flat-square" alt="143 Skills"/>
  <img src="https://img.shields.io/badge/plataformas-Hermes+GitHub-green?style=flat-square" alt="Hermes + GitHub"/>
  <img src="https://img.shields.io/badge/licencia-MIT-lightgrey?style=flat-square" alt="MIT License"/>
</p>

---

## Tu IA que realmente recuerda

Usas IA todos los días. Copias y pegas contexto. Re-explicas tu proyecto. Pierdes aprendizajes entre sesiones.

**¿Y si tu IA tuviera cerebro?**

No un chatbot. No un solo prompt. Un sistema estructurado, con un orquestador inteligente, 143 skills especializados y memoria persistente.

**Diseñado para la comunidad nan.builders** — ejecutándose en Hermes Agent sobre NaN.builders con GitHub como repositorio.

---

## ¿Qué es Ntizar Mastermind?

Ntizar Mastermind es un **framework de orquestación multi-agente** que usa **Hermes Agent** como motor de ejecución y **GitHub** como fuente de verdad.

```
Tu das una tarea
    │
    ▼
Koldo (orquestador) la clasifica (dominio + complejidad)
    │
    ▼
Carga los skills especializados del dominio relevante
    │
    ▼
Cada skill ejecuta con conocimiento profundo de su dominio
    │
    ▼
Koldo integra, verifica y presenta el resultado
    │
    ▼
La siguiente sesión empieza más inteligente, no desde cero
```

### Comparativa rápida

| Característica | v3.1 (Legacy) | **v4.0 (Actual)** |
|---|---|---|
| Plataforma | OpenCode + Obsidian | **Hermes Agent + GitHub** |
| Agentes | 11 agentes genéricos | **1 orquestador + 143 skills especializados** |
| Modelos | Multi-modelo manual | **Modelo único (qwen3.6)** |
| Memoria | Ebbinghaus decay manual | **`memory` + `session_search` nativo** |
| Skills | 15 skills propios | **143 skills Hermes (carga bajo demanda)** |
| Deploy | GitHub Pages | **NaN.builders + GitHub Pages** |

→ Detalles de arquitectura, niveles de ejecución y dominios → **[SOUL.md](SOUL.md)** | **[AGENTS.md](AGENTS.md)**

---

## Inicio Rápido

### Prerrequisitos

- [GitHub](https://github.com) (repositorio)
- [Hermes Agent](https://hermes-agent.nousresearch.com) (framework de agentes)
- Una cuenta en [NaN.builders](https://nan.builders) (VM en la nube)
- API key de un modelo de IA (qwen3.6 o deepseek-v4-flash)

### Instalación

```bash
# 1. Clonar
git clone https://github.com/Ntizar/NtizarBrainMasterMind.git
cd NtizarBrainMasterMind

# 2. Configurar API keys en .env

# 3. Iniciar con Hermes
hermes

# 4. Koldo (orquestador) se encarga del resto
```

### Primera tarea

```bash
# Una vez arrancado, simplemente dale una tarea:
"Crea una landing page para mi portfolio con modo oscuro"
```

El orquestador clasificará, cargará los skills necesarios y ejecutará el pipeline completo.

---

## Plataformas

### NaN.builders — Ejecución en la nube

- **VM permanente** con 1vCPU/2GB/20GB
- **Modelos:** qwen3.6, deepseek-v4-flash, Gemma4
- **Coste:** ~$0.50/1M tokens
- **Acceso móvil:** Telegram + WebUI

### GitHub — Repositorio y web

- **Código fuente** y documentación
- **GitHub Pages** para la landing
- **GitHub Actions** para deploy automático

---

## Token Tracking

El sistema rastrea el consumo de tokens en cada sesión:

| Métrica | Valor |
|---------|-------|
| **Log** | `tokens/tokens-log.json` |
| **Dashboard** | `tokens/index.html` |
| **Skill** | `/hermes-home/skills/koldo/token-tracking/` |
| **Precio qwen3.6** | $0.50/1M tokens (input+output) |

---

## Roadmap

### v4.0 actual (Junio 2026)
- [x] Migración a Hermes Agent + GitHub
- [x] 1 orquestador + 143 skills especializados
- [x] Token tracking con dashboard dinámico
- [x] SOUL.md unificado como fuente de verdad
- [x] Legacy v3.1 archivado en `legacy/`
- [x] Landing page completa con Aurora Design System
- [x] Auditoría y corrección de todos los hallazgos

### v4.1 (Próximo)
- [ ] Más skills de dominio específico
- [ ] Informes semanales de token usage automatizados
- [ ] Optimización de contexto para reducir costes

### v5.0 (Futuro)
- [ ] Multi-usuario con compartición de skills
- [ ] Marketplace de skills
- [ ] Editor visual de flujos
- [ ] Suite de benchmarks

---

## Contribuir

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

Áreas abiertas:
- 🧩 **Nuevos skills** — playbooks para tu dominio
- ⚡ **Optimización** — mejores prompts, flujos más inteligentes
- 🌐 **Documentación** — tutoriales, guías, videos
- 🧪 **Testing** — benchmarks y métricas de calidad

---

## Licencia

MIT License — ver [LICENSE](LICENSE).

Usa este sistema, fórzalo, mejóralo. Si te ahorra tiempo, pásalo.

---

<p align="center">
  Hecho con <span style="color: #f97316;">❤️</span> por <strong><a href="https://github.com/Ntizar">David Antizar</a></strong>
  <br/>
  <sub>Ntizar Mastermind — porque un mastermind no es un solo genio, sino un grupo de mentes especializadas trabajando juntas.</sub>
</p>

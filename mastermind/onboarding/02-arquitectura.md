# 02 — Arquitectura

## Dos sitios, un sistema

| Dónde | Qué | Rol |
|-------|-----|-----|
| `C:\Users\d_ant\Projects\MasterMind` (→ github.com/Ntizar/MasterMind) | Repo completo | **Fuente de verdad** |
| `C:\Users\d_ant\AppData\Local\hermes\` | Instalación Hermes: config.yaml, skills/, memories/ | **Ejecución** |

Los skills viven en AMBOS: la instalación local es la que Hermes carga; el repo es
la copia canónica que se sincroniza.

## Estructura del repo

```
MasterMind/
├── agent/          ← skills, memorias, identidad (SOUL.md, MEMORY.md, USER.md)
├── scripts/        ← motor: ChromaDB, stars-explorer, doctor, backup
├── notes/          ← notas de aprendizaje continuo (YYYY-MM-DD-titulo.md)
├── mastermind/     ← docs del sistema (este onboarding, patrones)
├── data/           ← stars-registry.json y datos de pipelines
├── index.html      ← web pública (GitHub Pages, consume Aurora v6 vía CDN)
└── AGENTS.md / README.md / CHANGELOG.md
```

## Stack técnico

- **Hermes Agent (desktop, Windows)** — motor, memoria persistente, delegate_task, gateway, cron
- **GitHub** — fuente de verdad y backup
- **NaN.builders** — modelos vía API OpenAI-compatible (qwen3.8-flash, glm5.3-flash, qwen3-embedding)
- **ChromaDB** — base vectorial local (`~/.mastermind/chromadb`), búsqueda semántica de skills

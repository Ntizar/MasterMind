<h1 align="center">MasterMind</h1>

<p align="center">
  <strong>El sistema de agente IA personal de David Antizar:<br>memoria persistente, skills con búsqueda semántica y backup en GitHub.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/MasterMind/">🌐 Web</a> ·
  <a href="#cómo-funciona">Cómo funciona</a> ·
  <a href="#stack">Stack</a> ·
  <a href="README_EN.md">English</a>
</p>

---

## Qué es (y qué no es)

**Esto no es un framework open-source.** No es un producto que puedas clonar y ejecutar. Es mi **sistema personal de agente IA** — una configuración muy específica de Hermes Agent + NaN.builders + ChromaDB + GitHub, construida para mí y que ejecuta tanto en mi PC (Windows) como en la nube.

Lo que sí es: una **arquitectura de referencia** de cómo un agente IA puede aprender de cada tarea, indexar su conocimiento en una base vectorial, aprender de las stars de GitHub mientras duermes, y persistir todo en un repo.

## Cómo funciona

```
Tarea de David
│
▼
Mastermind (agente Hermes — qwen3.8 / glm5.3 vía NaN API)
│
├── 1. Consulta ChromaDB (búsqueda semántica)
│      └── python scripts/consultar-skills.py "palabras clave" --json
│
├── 2. Filtra skills con score > 0.25
│      └── Carga solo los relevantes con skill_view()
│
├── 3. Ejecuta la tarea
│      └── Terminal, browser, files, delegate_task
│
└── 4. Aprendizaje continuo
       ├── ¿Merece skill?   → skill_manage(create) + re-indexar
       ├── ¿Merece nota?    → notes/YYYY-MM-DD-titulo.md
       ├── ¿Merece memoria? → memory(add)
       └── Commit al repo
```

### Las 3 capas de conocimiento

| Capa | Dónde vive | Qué guarda | Persistencia |
| --- | --- | --- | --- |
| 🧠 **Memoria Hermes** | `agent/MEMORY.md` + `agent/USER.md` | Preferencias, proyectos, lecciones | Inyectada en cada turno |
| 📚 **Skills** | `agent/skills/` | Procedimientos reutilizables por dominio | Carga bajo demanda vía ChromaDB |
| 🔒 **Repo GitHub** | `Ntizar/MasterMind` | Backup completo de todo | Push en cada ciclo de aprendizaje |

> El número de skills **no es fijo**: crece con cada ciclo del stars-explorer y cada sesión de trabajo. La cifra actual se consulta con `python scripts/indexar-skills.py` o consultando ChromaDB.

### Búsqueda semántica (ChromaDB)

El sistema no carga skills por nombre — busca por **significado**:

```bash
python scripts/consultar-skills.py "visor de mapas con isócronas" --json
# → skills ordenados por score de similitud coseno
# → sin límite arbitrario: si 50 skills son relevantes, se cargan los 50
```

- **Embeddings:** `qwen3-embedding` vía NaN API (distancia coseno, dim 4096)
- **Colección:** `mastermind-skills` (ChromaDB persistente en `~/.mastermind/chromadb`)
- **Re-indexación:** tras cada ciclo de aprendizaje, o manual con `--reset`

### Aprendizaje automático desde las stars de GitHub

El corazón del sistema: mientras duermo, Mastermind estudia los repos que marco con estrella y convierte lo que aprende en skills.

| Job | Schedule | Qué hace |
| --- | --- | --- |
| `mastermind-scout` | cada 6h | Explora un batch de stars → analiza tech stack y patrones → crea skills nuevos (con dedup semántico) → commit + push |
| `mastermind-weekly-digest` | lunes 9:00 | Resumen semanal: números, skills nuevos, skips y recomendaciones |

Criterios completos y detalles del pipeline: [`mastermind/stars-explorer.md`](mastermind/stars-explorer.md).

## Stack

| Componente | Qué es |
| --- | --- |
| **Modelo principal** | `qwen3.8-flash` vía NaN API (api.nan.builders/v1) |
| **Modelo secundario** | `glm5.3-flash` — fallback / según disponibilidad de tokens |
| **Agente** | Hermes Agent — desktop (Windows local), max_turns 90, delegación nativa |
| **Gateway** | Hermes gateway — arranca al login (Scheduled Task/Startup), da vida a los cron |
| **Vector DB** | ChromaDB — colección `mastermind-skills`, persistente local |
| **Embeddings** | `qwen3-embedding` — distancia coseno, dim 4096 |
| **GitHub** | `Ntizar/MasterMind` — auth vía `gh` CLI (keyring de Windows) |
| **Idioma** | Español — todo el sistema |

## Estructura del repo

```
MasterMind/
├── agent/               ← el agente
│   ├── skills/          ← skills por dominio (indexados en ChromaDB)
│   ├── MEMORY.md        ← memoria de proyectos y lecciones
│   ├── USER.md          ← identidad y preferencias de David
│   └── SOUL.md          ← identidad del agente (fuente de verdad)
├── scripts/             ← motor: ChromaDB, stars-explorer, backup, lifecycle
├── notes/               ← notas de aprendizaje continuo
├── mastermind/          ← documentación del sistema
├── data/                ← stars-registry.json (estado de los pipelines)
├── index.html           ← web pública (GitHub Pages)
└── AGENTS.md            ← referencia rápida para agentes que aterrizan aquí
```

## Scripts del sistema

| Script | Función |
| --- | --- |
| `scripts/consultar-skills.py` | Búsqueda semántica en ChromaDB |
| `scripts/indexar-skills.py` | Indexa todos los SKILL.md en ChromaDB (`--reset` para reindexar todo) |
| `scripts/explorar-stars.py` | Explora las stars de GitHub y prepara análisis para crear skills |
| `scripts/run-stars-explorer.sh` | Wrapper del explorador (token vía `gh auth`, Windows-compatible) |
| `scripts/backup-hermes-memory.sh` | Backup de memoria al repo |
| `scripts/skill-lifecycle.py` | Analiza uso real y reclasifica skills |
| `scripts/ebbinghaus-decay.py` | Repaso espaciado (curva del olvido) |

## Roadmap

- **v4.2 (actual)** — migración a Windows local: gateway propio, ChromaDB embebido, scouts de stars, estructura `agent/` unificada
- **v4.3 (próximo)** — más crons de dominio (ESIOS, inventario de APIs), TTS/STT local, dashboard de tracking

## Licencia

MIT License — ver [LICENSE](LICENSE).

Hecho con ❤️ por **[David Antizar](https://github.com/Ntizar)**

Mastermind es mi ejecutor, yo soy el autor.

<h1 align="center">NtizarBrainMasterMind</h1>

<p align="center">
  <strong>Mi sistema de agente IA personal con búsqueda semántica,<br>memoria persistente y backup en GitHub.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/NtizarBrainMasterMind/">🌐 Web</a> ·
  <a href="#cómo-funciona">Cómo funciona</a> ·
  <a href="#stack">Stack</a> ·
  <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versión-4.1-blue?style=flat-square" alt="v4.1"/>
  <img src="https://img.shields.io/badge/skills-303-orange?style=flat-square" alt="303 Skills"/>
  <img src="https://img.shields.io/badge/búsqueda-ChromaDB-purple?style=flat-square" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/agente-Mastermind-green?style=flat-square" alt="Mastermind"/>
</p>

---

## Qué es (y qué no es)

**No es un framework open-source.** No es un producto que puedas clonar y ejecutar. Es mi **sistema personal de agente IA** — una configuración muy específica de Hermes Agent + NaN.builders + ChromaDB + GitHub construida para mí.

Lo que sí es: una **arquitectura de referencia viva** de cómo un agente IA escala su conocimiento — 303 skills indexados semánticamente, aprendizaje continuo post-tarea, y todo persistido en GitHub.

---

## Cómo funciona

```
Tarea de David
       │
       ▼
Mastermind (agente IA en NaN.builders)
       │
       ├── 1. ChromaDB — búsqueda semántica (qwen3-embedding)
       │     └── consultar-skills.py "palabras clave" --json
       │
       ├── 2. Filtra skills relevantes (score > 0.25)
       │     └── Carga con skill_view() — sin límite arbitrario
       │
       ├── 3. Decide ejecución
       │     ├── 🟢 Directo   (1-3 tool calls)
       │     ├── 🟡 Simple    (4-8 tool calls)
       │     ├── 🟠 Paralelo  (delegate_task)
       │     └── 🔴 Complejo  (orquestación multi-subagente)
       │
       └── 4. Aprendizaje continuo
             ├── ¿Nuevo skill?        → skill_manage(create)
             ├── ¿Nota de sesión?     → notes/YYYY-MM-DD-titulo.md
             └── ¿Hecho durable?      → memory(add)
```

### Las 3 capas de conocimiento

| Capa | Dónde vive | Qué guarda | Persistencia |
|------|-----------|------------|-------------|
| 🧠 **Memoria Hermes** | `/hermes-home/memories/` | Preferencias, entorno, lecciones aprendidas | Inyectada en cada turno |
| 📚 **Skills** | `/hermes-home/skills/` (303) | Procedimientos reutilizables, workflows, pitfalls | Carga bajo demanda vía ChromaDB |
| 🔒 **Repo GitHub** | `NtizarBrainMasterMind` | Backup completo: skills, notas, scripts, config | Push diario 05:00 UTC |

### Búsqueda semántica (ChromaDB)

Cada `SKILL.md` se convierte en un vector con `qwen3-embedding` (4096 dimensiones), indexado en ChromaDB. Cuando llega una petición, el sistema busca por **significado**, no por nombre:

```bash
cd /hermes-home/scripts
NAN_API="$NAN_API" /hermes-home/chromadb-venv/bin/python consultar-skills.py "transporte público GTFS" --json
```

- **Colección:** `mastermind-skills` (localhost:8000)
- **Modelo:** qwen3-embedding vía NaN API
- **Distancia:** coseno | **Threshold:** > 0.25
- **Re-indexación:** domingo 04:00 UTC (cron automático)
- **Sin límite de skills:** si 50 son relevantes → se cargan los 50

### Filosofía de skills — sin límites

No hay límite de skills. ChromaDB filtra semánticamente, no por número. Con 303 skills hoy, o 500 mañana — el sistema escala sin fricción. **Nunca poner límites conservadores.** La única regla: cargar solo los relevantes.

---

## Stack

| Componente | Especificación |
|-----------|----------------|
| **Modelo** | deepseek-v4-flash / qwen3.6 vía NaN API (`api.nan.builders/v1`) |
| **Infra** | MicroVM NaN.builders (1vCPU / 2GB / 20GB) |
| **Agente** | Hermes Agent — max_turns: 90, delegación: 3 subagentes |
| **Vector DB** | ChromaDB v2 — colección `mastermind-skills`, 4096d embeddings |
| **Embeddings** | qwen3-embedding (NaN API) — distancia coseno |
| **GitHub** | `Ntizar/NtizarBrainMasterMind` — auth token HTTPS, sin `gh` CLI |
| **TTS** | Edge TTS — voz `es-ES-AlvaroNeural` |
| **STT** | Whisper local (modelo base) |
| **Cron** | 8 jobs Hermes activos |
| **Idioma** | **Castellano** — TODO el sistema: repos, scripts, cron, informes |

---

## Skills activos (303)

Indexados por ChromaDB y cargados bajo demanda. Distribución por dominios:

| Dominio | Skills aprox | Ejemplos |
|---------|-------------|----------|
| 🔥 **Core (Software)** | ~25 | TDD, code review, debugging, refactor, system-audit |
| 📦 **GitHub** | ~7 | PR workflow, issues, repo management, auth |
| 🌐 **Frontend / CSS** | ~15 | Aurora DS, dashboards, liquid glass, design systems |
| ⚙️ **Backend / APIs** | ~15 | Node.js patterns, ESM, APIs REST, fetch paralelo |
| 🏗️ **Infra / DevOps** | ~20 | Docker, seguridad, cron jobs, deploy NaN, pipelines |
| 📊 **Data / Ciencia** | ~15 | Monte Carlo, simuladores, quant, timesfm |
| 🎨 **Creative** | ~25 | p5.js, manim, ASCII, diagramas, sketch, diseño |
| 🧠 **Mastermind** | ~12 | Orquestación, ChromaDB, backup, spec workflow |
| 📚 **STEM** | ~55 | Matemáticas, física, dibujo técnico, química, biología |
| 🔬 **ML / Visión** | ~25 | YOLO, SAM, segmentación, satélite, deep learning |
| 🚆 **Movilidad / GIS** | ~35 | GTFS, NeTEx, isocronas, OSM, mapas 3D, Valhalla |
| 📄 **Documentos / PDF** | ~10 | Procesamiento PDF, OCR, conversion, reportes |
| 🔌 **MCP / Integraciones** | ~15 | PostgreSQL MCP, Nango, APIs externas |
| Otros | ~40 | Salud, finanzas, crypto, productividad, STEM, educación |

**Carga bajo demanda vía ChromaDB** — nunca se cargan todos a la vez.

---

## Cron jobs activos (8)

| Nombre | Schedule | Último estado |
|--------|----------|---------------|
| `BiciMad Tetuán` | L-Mi 06:30, 13:00 | ✅ ok |
| `inventario-apis-procesar` | cada 30m | ✅ ok |
| `inventario-apis-resumen-diario` | 22:00 UTC | ✅ ok |
| `skill-maintenance` | día 1 cada mes | ✅ ok |
| `chromadb-reindex-semanal` | domingo 04:00 UTC | ✅ ok |
| `skills-sync-to-github` | 05:00 UTC diario | ✅ ok |
| `stars-explorer-nocturno` | 03:00 UTC diario | ✅ ok |
| `deep-learning-diario` | 03:30 UTC diario | ✅ ok |

---

## Scripts del sistema (24 scripts)

| Script | Función |
|--------|---------|
| `consultar-skills.py` | Búsqueda semántica en ChromaDB con query embedding y ranking por coseno |
| `indexar-skills.py` | Indexación batch de todos los SKILL.md en ChromaDB |
| `start-chromadb.sh` | Auto-start del servidor ChromaDB local |
| `skill-learning.sh` | Cola priorizada de aprendizaje desde el hub Hermes |
| `skill-lifecycle.py` | Analiza uso real (git + notas) y re-clasifica en HIGH/MEDIUM/LOW |
| `explorar-stars.py` | Explora GitHub stars de David y genera skills nuevos |
| `ebbinghaus-decay.py` | Repaso espaciado (curva de olvido) |
| `backup-hermes-memory.sh` | Backup de memoria + push automático a GitHub |
| `bicimad-multi-alert.py` | Alertas multi-parada BiciMad |
| `bicimad-alert.py` | Alerta simple BiciMad |
| `bicimad-calendar-sync.py` | Sincronización calendario BiciMad |
| `generate-dashboard.py` | Generador de dashboard web |
| `pipeline_europa.py` | Pipeline de datos europeos |
| `delegation-flows.py` | Flujos de delegación multi-agente |
| `knowledge-graph.py` | Generación de grafo de conocimiento |
| `fetch-repos-info.py` | Fetch de información de repos |
| `terran-auditor.py` | Auditoría de skills Terran |

---

## Notas de aprendizaje (25+)

Cada sesión compleja genera una nota en `notes/` con frontmatter YAML. Cubren desde auditorías de skills hasta exploración de stars de GitHub, configuración de ChromaDB, y análisis de proyectos.

---

## Aprendizaje continuo

Después de cada tarea compleja (5+ tool calls), Mastermind evalúa:

1. **¿Merece skill nuevo?** → `skill_manage(create)` con frontmatter completo
2. **¿Merece nota?** → `notes/YYYY-MM-DD-titulo.md`
3. **¿Merece registro en memoria?** → `memory(add)` para hechos durables
4. **¿Skill existente desactualizado?** → `skill_manage(patch)` inmediato

Los skills del hub externo se instalan vía `skill-learning.sh`, con cola priorizada de ~120 skills en cartera.

---

## Roadmap

### Actual (v4.1 — Julio 2026)
- [x] ChromaDB operativo con 303 skills indexados semánticamente
- [x] Búsqueda semántica por significado (qwen3-embedding, 4096d)
- [x] 8 cron jobs reales vía Hermes (monitorización, backup, aprendizaje)
- [x] Backup automático a GitHub 05:00 UTC diario
- [x] Re-indexación semanal de ChromaDB (domingo 04:00 UTC)
- [x] Stars Explorer — pipeline de exploración nocturna de GitHub stars
- [x] Deep Learning — pipeline de aprendizaje profundo diario
- [x] Aprendizaje continuo post-tarea (skill / nota / memoria)

### Próximo
- [ ] Migrar SOUL.md de raíz a v2.x (actualmente desactualizado — el real está en `mastermind/SOUL.md`)
- [ ] Informes semanales de token usage y costes
- [ ] Evaluación de threshold dinámico para ChromaDB
- [ ] Más skills de dominio específico (movilidad, energía, datos gobierno)

---

## Human Loop — Sistema de Control

**Se activa cuando:**
- Se modifican más de 5 archivos
- Decisiones de arquitectura
- Deploy a producción
- Migraciones de datos o plataforma
- El usuario lo solicita

**Patrón:** Planificar → ✅ → Implementar → ✅ → Sintetizar → ✅

---

## Atribución

<p align="center">
  Hecho con <span style="color: #f97316;">❤️</span> por <strong><a href="https://github.com/Ntizar">David Antizar</a></strong>
  <br/>
  <sub>Mastermind es mi ejecutor, yo soy el autor.</sub>
</p>

---

## Licencia

MIT License — ver [LICENSE](LICENSE).

<p align="center">
  <strong>v4.1 — 2026-07-20</strong>
</p>
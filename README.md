<h1 align="center">MasterMind</h1>

<p align="center">
  <strong>Mi agente IA personal con memoria persistente,<br>búsqueda semántica de skills y backup en GitHub.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/MasterMind/">🌐 Web</a> ·
  <a href="#cómo-funciona">Cómo funciona</a> ·
  <a href="#stack">Stack</a> ·
  <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.1-blue?style=flat-square" alt="Version 4.1"/>
  <img src="https://img.shields.io/badge/skills-240-orange?style=flat-square" alt="240 Skills"/>
  <img src="https://img.shields.io/badge/búsqueda-ChromaDB-purple?style=flat-square" alt="ChromaDB"/>
  <img src="https://img.shields.io/badge/agente-Mastermind-green?style=flat-square" alt="Mastermind Agent"/>
</p>

---

## Qué es (y qué no es)

**Esto no es un framework open-source.** No es un producto que puedas clonar y ejecutar. Es mi **sistema personal de agente IA** — una configuración muy específica de Hermes Agent + NaN.builders + ChromaDB + GitHub que he construido para mí.

Lo que sí es: una arquitectura de referencia de cómo un agente IA puede aprender de cada tarea, indexar su conocimiento en una base de datos vectorial, y persistir todo en GitHub.

---

## Cómo funciona

```
Tarea de David
       │
       ▼
Mastermind (agente qwen3.6 en NaN.builders)
       │
       ├── 1. Consulta ChromaDB (búsqueda semántica)
       │     └── consultar-skills.py "palabras clave" --json
       │
       ├── 2. Filtra skills con score > 0.25
       │     └── Carga solo los relevantes con skill_view()
       │
       ├── 3. Ejecuta la tarea
       │     └── Terminal, browser, file, delegate_task
       │
       └── 4. Aprendizaje continuo
             ├── ¿Merece skill? → skill_manage(create)
             ├── ¿Merece nota? → notes/YYYY-MM-DD-titulo.md
             └── ¿Merece memoria? → memory(add)
```

### Las 3 capas de conocimiento

| Capa | Dónde vive | Qué guarda | Persistencia |
|------|-----------|------------|-------------|
| 🧠 **Memoria Hermes** | `/hermes-home/memories/` | Preferencias, entorno, lecciones | Inyectada en cada turno |
| 📚 **Skills** | `/hermes-home/skills/` | 240 procedimientos reutilizables | Carga bajo demanda vía ChromaDB |
| 🔒 **Repo GitHub** | `MasterMind` | Backup completo de todo | Push cada 6h (automático) |

### Búsqueda semántica (ChromaDB)

El sistema no carga skills por nombre — busca por **significado**:

1. Cada `SKILL.md` se convierte en un vector con `qwen3-embedding`
2. Los 240 vectores se indexan en ChromaDB (localhost:8000, colección `mastermind-skills`)
3. Cuando llega una petición, se genera su embedding y se buscan los skills más cercanos por similitud coseno
4. Solo los que superan threshold 0.25 se cargan en contexto

**Sin límite arbitrario:** si 50 skills son relevantes, se cargan los 50.

---

## Stack

| Componente | Qué es |
|-----------|--------|
| **Modelo** | qwen3.6 vía NaN API (api.nan.builders/v1) |
| **Infra** | MicroVM 1vCPU / 2GB / 20GB — NaN.builders |
| **Agente** | Hermes Agent — max_turns: 90, delegación: 3 subagentes |
| **Vector DB** | ChromaDB v2 — colección mastermind-skills |
| **Embeddings** | qwen3-embedding — distancia coseno |
| **GitHub** | Ntizar/MasterMind — auth token HTTPS |
| **TTS** | Edge TTS — voz es-ES-AlvaroNeural |
| **STT** | Whisper local (modelo base) |
| **Cron** | 10 jobs Hermes (backup, ESIOS, deep learning, stars, re-index) |
| **Idioma** | Español — todo el sistema |

---

## Scripts del sistema

| Script | Función |
|--------|---------|
| `consultar-skills.py` | Búsqueda semántica en ChromaDB |
| `indexar-skills.py` | Indexa todos los SKILL.md en ChromaDB |
| `skill-lifecycle.py` | Analiza uso real (git + notas) y re-clasifica skills |
| `skill-learning.sh` | Instala 1 skill del hub Hermes cada ejecución |
| `backup-hermes-memory.sh` | Backup de memoria al repo GitHub |
| `start-chromadb.sh` | Auto-start de ChromaDB |
| `explorar-stars.py` | Explora stars de GitHub y genera skills |
| `ebbinghaus-decay.py` | Repaso espaciado (curva de olvido) |

---

## Roadmap

### v4.1 (actual — Julio 2026)
- [x] ChromaDB operativo con 240 skills indexados
- [x] Búsqueda semántica por similitud coseno
- [x] Cron jobs reales vía Hermes (10 jobs activos)
- [x] Backup automático a GitHub cada 6h
- [x] Re-indexación semanal de ChromaDB
- [x] Aprendizaje continuo post-tarea
- [ ] Push automático a GitHub en backup
- [ ] Ejecución regular del lifecycle analysis
- [ ] Smart threshold dinámico para ChromaDB

### v4.2 (próximo)
- [ ] Más skills de dominio específico
- [ ] Informes semanales de token usage
- [ ] Optimización de contexto

---

## Licencia

MIT License — ver [LICENSE](LICENSE).

---

<p align="center">
  Hecho con <span style="color: #f97316;">❤️</span> por <strong><a href="https://github.com/Ntizar">David Antizar</a></strong>
  <br/>
  <sub>Mastermind es mi ejecutor, yo soy el autor.</sub>
</p>
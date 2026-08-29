<div align="center">


# 🧠 MasterMind

**Un agente IA que aprende solo, recuerda todo y mientras tú duermes
estudia los repos que marcaste con estrella.**

[![Plataforma](https://img.shields.io/badge/plataforma-Windows_11-0078D4?style=flat-square&logo=windows11&logoColor=white)](https://github.com/Ntizar/MasterMind)
[![Motor](https://img.shields.io/badge/motor-Hermes_Agent-blue?style=flat-square)](https://github.com/NousResearch/hermes-agent)
[![Modelos](https://img.shields.io/badge/modelos-NaN.builders-FF6B35?style=flat-square)](https://nan.builders)
[![Búsqueda](https://img.shields.io/badge/skills-ChromaDB_semántico-8A2BE2?style=flat-square)](https://www.trychroma.com)
[![Idioma](https://img.shields.io/badge/idioma-Español-FFD700?style=flat-square)](#)
[![Licencia](https://img.shields.io/badge/licencia-MIT-green?style=flat-square)](LICENSE)

[🌐 Ver la web](https://ntizar.github.io/MasterMind/) · [Cómo funciona](#-cómo-funciona) · [El ciclo autónomo](#-el-ciclo-autónomo) · [English](README_EN.md)

</div>

---

> [!IMPORTANT]
> **Esto no es un framework open-source.** No puedes clonarlo y ejecutarlo tal cual — es el sistema personal de agente IA de David Antizar. Lo que sí es: una **arquitectura de referencia real y funcionando a diario**, de cómo un agente puede aprender de cada tarea, indexar su conocimiento por significado y aprender de GitHub mientras duerme.

---

## 💡 La idea en 30 segundos

La mayoría de asistentes IA sufren amnesia: cada sesión empiezan de cero, no saben quién eres ni lo que hicieron ayer, y su conocimiento útil se evapora.

**MasterMind es lo contrario.** Vive en mi PC (Windows 11), ejecuta sobre [Hermes Agent](https://github.com/NousResearch/hermes-agent) con modelos de [NaN.builders](https://nan.builders), y tiene tres superpoderes:

| Superpoder | Cómo |
|---|---|
| 🧠 **Recuerda** | Memoria persistente que se inyecta en cada sesión: quién soy, mis proyectos, mis preferencias y las lecciones aprendidas |
| 📚 **Sabe buscar** | Sus skills no se cargan por nombre sino **por significado**, con búsqueda semántica en ChromaDB y embeddings |
| 🌙 **Aprende solo** | Cada 6 horas explora las repos que marco con ⭐ en GitHub, extrae sus patrones y convierte lo que aprende en skills nuevos |

Y todo esto queda respaldado en este repositorio, que es su fuente de verdad.

---

## 🔄 Cómo funciona

```
                        Tarea de David
                              │
                              ▼
     ┌─────────────────────────────────────────────┐
     │   MASTERMIND (Hermes Agent + NaN.builders)  │
     └─────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  1️⃣ CONSULTA           2️⃣ EJECUTA            3️⃣ APRENDE
  Búsqueda semántica    Herramientas del      ¿Merece un skill?
  en ChromaDB:          agente: terminal,     ¿Merece una nota?
  "¿qué sé de X?"       navegador, ficheros,  ¿Merece memoria?
  → skills ordenados    delegación a          → lo guarda y
    por relevancia      sub-agentes           hace commit
                              │
                              ▼
                    La próxima sesión sabe más
```

### 1️⃣ La búsqueda semántica (el corazón del sistema)

MasterMind **no** tiene una lista de skills que carga todas juntas. Tiene una base de datos vectorial:

```bash
python scripts/consultar-skills.py "mapa de isócronas de transporte" --json
```

```json
[
  { "name": "routing-isochrones",     "score": 0.72 },
  { "name": "accessibility-map",      "score": 0.68 },
  { "name": "valhalla-routing",       "score": 0.61 }
]
```

Cada skill está indexado con `qwen3-embedding` (4096 dimensiones, distancia coseno). Si una tarea necesita 3 skills, carga 3. Si necesita 50, carga 50. **Sin límites artificiales — solo relevancia.**

### 2️⃣ Los niveles de ejecución

Antes de actuar, MasterMind decide cuánta artillería necesita la tarea:

| Nivel | Cuándo | Patrón |
|:---:|---|---|
| 🟢 **1 — Directo** | Buscar, leer, un commit | MasterMind solo, 1-3 tool calls |
| 🟡 **2 — Simple** | Un refactor, un módulo | 4-8 tool calls |
| 🟠 **3 — Paralelo** | Frontend + backend + tests | Delegación a 2-3 sub-agentes |
| 🔴 **4 — Orquestación** | Una feature completa | Planner → implementadores → revisor |

Y en cambios críticos (más de 5 archivos, decisiones de arquitectura, deploys) se activa el **human loop**: planifica → espera tu ✅ → implementa → espera tu ✅. Nunca asume.

---

## 🌙 El ciclo autónomo

Esto es lo que hace MasterMind cuando nadie le está hablando:

<div align="center">

```
     ☀️  DÍA                    🌙  NOCHE                  📅  SEMANA
┌─────────────────┐      ┌─────────────────────┐     ┌──────────────────┐
│  SCOUT  · cada 6h│      │ DOCTOR · diario 10h │     │ DIGEST · lunes 9h│
│                 │      │                     │     │                  │
│ Explora un batch│      │ ¿Gateway vivo?      │     │ ¿Qué hemos       │
│ de tus stars de │      │ ¿Crons corrieron?   │     │ aprendido esta   │
│ GitHub →        │      │ ¿ChromaDB synced?   │     │ semana?          │
│                 │      │ ¿Repo sincronizado? │     │                  │
│ ¿Merece skill?  │      │                     │     │ Skills nuevos,   │
│ ├─ SÍ → lo crea │      │ Se autocura lo      │     │ números, recomend│
│ └─ NO → lo salta│      │ seguro y si todo    │     │ aciones para la  │
│      (con razón)│      │ va bien, en silencio│     │ próxima semana   │
│                 │      │                     │     │                  │
│ commit + push   │      │ commit si toca      │     │ informe          │
└─────────────────┘      └─────────────────────┘     └──────────────────┘
```

</div>

**El dedup semántico es lo que hace sostenible el ciclo:** antes de crear un skill, el scout busca en ChromaDB si ya existe algo equivalente. Si existe, lo salta y anota la razón. Cada skill que entra al sistema es conocimiento **nuevo**, no duplicado.

---

## 🗂️ Las 3 capas de conocimiento

| Capa | Dónde vive | Qué guarda |
|---|---|---|
| 🧠 **Memoria** | `agent/MEMORY.md` + `agent/USER.md` | Proyectos, preferencias, lecciones del día a día. Se inyecta en cada sesión |
| 📚 **Skills** | `agent/skills/` + ChromaDB | Procedimientos reutilizables por dominio: GIS, transporte, dashboards, ML, STEM... |
| 🗃️ **Memoria de especialistas** | `agent/skills/<skill>/references/estado-*.md` | Cada skill con estado acumulativo recuerda su dominio entre sesiones — comiteada y versionada (ver `mastermind/memoria-especialistas.md`) |
| 🔒 **Backup** | Este repositorio | Todo lo anterior, con push en cada ciclo de aprendizaje |

> [!NOTE]
> El número de skills **no es fijo**: crece con cada ciclo del scout y cada sesión de trabajo. Es una pregunta que el sistema se hace, no un dato que se escribe en un badge.

---

## 🏗️ Estructura del repositorio

```
MasterMind/
│
├── 🤖 agent/                  ← el agente
│   ├── skills/                ← skills por dominio (indexados en ChromaDB)
│   ├── MEMORY.md              ← memoria de proyectos y lecciones
│   ├── USER.md                ← identidad y preferencias de David
│   └── SOUL.md                ← la identidad del agente (fuente de verdad)
│
├── ⚙️ scripts/                ← el motor
│   ├── consultar-skills.py    ← búsqueda semántica
│   ├── indexar-skills.py      ← indexación en ChromaDB
│   ├── explorar-stars.py      ← explorador de stars de GitHub
│   ├── doctor.py              ← health check del sistema
│   ├── test-doctor.py         ← tests del doctor: inyecta cada bug real y verifica que lo detecta
│   └── ...                    ← backup, lifecycle, ebbinghaus...
│
├── 📝 notes/                  ← notas de aprendizaje continuo
├── 📊 data/                   ← stars-registry.json (estado de los pipelines)
├── 📖 mastermind/             ← documentación interna: onboarding numerado
│   └── onboarding/            ← (01-06) de identidad a recuperación desde cero
└── 🌐 index.html              ← la web pública (GitHub Pages)
```

---

## 🧰 Stack

| Capa | Tecnología | Papel |
|---|---|---|
| **Agente** | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Motor de ejecución: tools, delegación, gateway, cron |
| **Superficie** | Hermes Desktop (Windows 11) | Donde converso con MasterMind a diario |
| **Modelos** | [NaN.builders](https://nan.builders) API | `glm5.3-flash` / `qwen3.8-flash` según fase y presupuesto |
| **Embeddings** | `qwen3-embedding` | Vectores de 4096 dim para la búsqueda semántica |
| **Base vectorial** | [ChromaDB](https://www.trychroma.com) | Persistente y embebida, sin servidor |
| **VCS** | GitHub (`Ntizar/MasterMind`) | Fuente de verdad y backup con historia |
| **Gateway** | Hermes Gateway | Mantiene vivos los cron jobs, autoarranque al login |

---

## 🚀 Guía rápida (si fueras yo)

> [!WARNING]
> Esto es lo que haría yo en **mi** máquina para reconstruir el sistema. No es un instalador genérico.

```bash
# 1. Instalar Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash   # o el instalador Windows

# 2. Clonar el sistema (el repo ES la configuración)
git clone https://github.com/Ntizar/MasterMind ~/Projects/MasterMind

# 3. Instalar ChromaDB en el Python del sistema
pip install chromadb

# 4. Indexar los skills (necesita las credenciales de la API de embeddings en el .env de Hermes)
python scripts/indexar-skills.py --reset

# 5. Comprobar que el sistema respira
python scripts/doctor.py

# 6. Verificar que el doctor detecta los bugs (tests de inyección)
python scripts/test-doctor.py

# 7. Probar la búsqueda semántica
python scripts/consultar-skills.py "cualquier tema" --json
```

Y el health check en acción:

```
🩺 Doctor Mastermind — 2026-08-28 14:39

✅ gateway          ✓ proceso vivo, autoarranque activo
✅ chromadb         indexados: 311 | SKILL.md en disco: 311
✅ stars-registry   último run hace 2.6h | 133 repos procesados
✅ git              rama: master | LIMPIO

✅ Todo en orden
```

---

## 📜 Las 12 reglas del sistema

Destiladas del uso diario real:

1. **Un orquestador, muchos especialistas** — MasterMind clasifica y delega, los skills ejecutan
2. **Skills bajo demanda por significado** — ChromaDB primero, `skill_view()` después
3. **Memoria persistente** — nada se aprende dos veces, nada se olvida
4. **GitHub como fuente de verdad** — Markdown plano, sin dependencias externas
5. **NUNCA borrar del repo** — solo crear o modificar
6. **Notas significativas** → `notes/YYYY-MM-DD-titulo.md`
7. **Skills nuevos** → `agent/skills/` + reindexar ChromaDB
8. **Cada aprendizaje importante** → commit al repo
9. **Los secretos viven solo en `.env`** — nunca en notas, commits ni prompts de cron
10. **SOUL.md es la fuente de verdad** de la identidad
11. **Todo en castellano** — repos, scripts, crons e informes
12. **Human loop en cambios críticos** — diffs visibles, aprobación explícita

---

<div align="center">

**Hecho con ❤️ por [David Antizar](https://github.com/Ntizar)**

*MasterMind es mi ejecutor. Yo soy el autor.*

[🌐 Web](https://ntizar.github.io/MasterMind/) · [English](README_EN.md) · [Licencia MIT](LICENSE)

</div>

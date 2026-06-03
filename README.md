<p align="center">
  <img src="assets/banner.svg" alt="Ntizar Mastermind" width="800"/>
</p>

<h1 align="center">Ntizar Mastermind</h1>

<p align="center">
  <strong>Framework open-source de orquestación multi-agente con memoria persistente,<br>decaimiento de Ebbinghaus y routing de modelos.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/NtizarBrainMasterMind/">🌐 Web</a> ·
  <a href="#inicio-rápido">Inicio Rápido</a> ·
  <a href="docs/ARCHITECTURE.md">Arquitectura</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-3.1-blue?style=flat-square" alt="Version 3.1"/>
  <img src="https://img.shields.io/badge/agentes-11-orange?style=flat-square" alt="11 Agentes"/>
  <img src="https://img.shields.io/badge/modelos-multi--modelo-green?style=flat-square" alt="Multi-modelo"/>
  <img src="https://img.shields.io/badge/memoria-Ebbinghaus%20decay-purple?style=flat-square" alt="Sistema de Memoria"/>
  <img src="https://img.shields.io/badge/licencia-MIT-lightgrey?style=flat-square" alt="MIT License"/>
  <img src="https://img.shields.io/badge/web-live-blueviolet?style=flat-square" alt="Web en vivo"/>
  <img src="https://img.shields.io/badge/skills-15-blue?style=flat-square" alt="15 Skills"/>
</p>

---

## Tu IA que realmente recuerda

Usas IA todos los días. Copias y pegas contexto. Re-explicas tu proyecto. Pierdes aprendizajes entre sesiones. Tus prompts son largos, caros y frágiles.

**¿Y si tu IA tuviera cerebro?**

No un chatbot. No un solo prompt. Un sistema estructurado, multi-agente, con memoria persistente, roles especializados y una curva de olvido que mantiene tu contexto ligero y relevante.

**Diseñado para la comunidad nan.builders** — pero extrapolable a cualquier sistema de agentes IA.

---

## ¿Qué es Ntizar Mastermind?

Ntizar Mastermind es un **framework open-source de orquestación multi-agente** sobre [OpenCode](https://opencode.ai) + [Obsidian](https://obsidian.md). Transforma tu flujo de trabajo de "una conversación a la vez" a un **sistema de inteligencia persistente y auto-mejorable**.

```
Tu das una tarea
    │
    ▼
El ORQUESTADOR la clasifica (tipo, complejidad, dominio)
    │
    ▼
Selecciona el FLUJO óptimo (2 a 10 agentes)
    │
    ▼
Cada AGENTE se ejecuta en el mejor modelo para su rol
    │
    ▼
Los resultados son REVISADOS, CRITICADOS y SINTETIZADOS
    │
    ▼
Los aprendizajes se ARCHIVAN con curva de expiración
    │
    ▼
La siguiente sesión empieza más inteligente, no desde cero
```

### Comparativa rápida

| Característica | Prompting tradicional | **Ntizar Mastermind v3.1** |
|---|---|---|
| Contexto | Se pierde cada sesión | **Memoria persistente con decaimiento inteligente** |
| Agentes | Una sola personalidad | **11 agentes especializados con roles definidos** |
| Modelos | Un modelo hace todo | **Cada agente usa su modelo óptimo** |
| Coste | Contexto completo siempre | **40-60% ahorro vía carga inteligente** |
| Calidad | Sin proceso de revisión | **Revisión obligatoria + crítico adversarial** |
| Aprendizaje | Empieza desde cero | **Acumula patrones, skills y conocimiento** |
| Control | La IA decide todo | **Humano en el bucle en cada checkpoint** |
| Portabilidad | No portátil | **Cross-platform: Linux, macOS, Windows/WSL** |

---

## Los 11 Agentes

| # | Agente | Rol | Piénsalo como... |
|---|--------|-----|------------------|
| 00 | **Orquestador** | Clasifica tareas, diseña flujos, delega | El CEO |
| 01 | **Clasificador** | Evalúa complejidad, dominio, ambigüedad | El Triaje |
| 02 | **Explorador** | Lee contexto sin modificar nada | El Scout |
| 03 | **Planificador** | Define estrategia, pasos, criterios de éxito | El Arquitecto |
| 04 | **Spec Writer** | Convierte plan en spec ejecutable | El Abogado de Contratos |
| 05 | **Implementador** | Ejecuta la spec, produce entregables | El Constructor |
| 06 | **Revisor** | Validación PASS/FAIL contra criterios | El Inspector de Calidad |
| 07 | **Crítico** | Revisión adversarial — encuentra lo que otros no ven | El Abogado del Diablo |
| 08 | **Sintetizador** | Transforma reportes en resultados legibles | El Traductor |
| 09 | **Archivador** | Destila aprendizajes con metadatos de decaimiento | El Bibliotecario |
| 10 | **Bibliotecario** | Mantiene el grafo de conocimiento y salud del sistema | El Jardinero |

> **El Crítico nunca se degrada.** Si el mejor modelo no está disponible, el Crítico se omite completamente en vez de ejecutarse en un modelo inferior. Calidad sobre cantidad.

> **Nuevo en v3.1:** El Crítico se activa automáticamente cuando se cumple ≥1 criterio objetivo (complejidad ≥4, ≥3 reintentos, ≥3 archivos, impacto alto, reviewer WARNINGs, o solicitud humana explícita).

---

## Arquitectura Multi-Modelo

Cada agente usa el modelo correcto para su trabajo:

```
Orquestador + Crítico  ──►  Claude Opus / GPT-4o       (alto razonamiento)
Explorador              ──►  Gemini 2.5 Pro              (contexto de 1M tokens)
Implementador           ──►  Claude Opus / Sonnet         (generación de código)
Revisor                 ──►  Claude Sonnet / Flash        (criterios concretos)
Sintetizador + Archiv.  ──►  Claude Haiku / Flash         (tareas mecánicas)
```

**Resultado:** Misma calidad de output, 40-60% menos coste. Tú eliges los modelos — el sistema propone, tú confirmas.

---

## Memoria que olvida (a propósito)

Cada aprendizaje tiene un **tipo de decaimiento** basado en la curva del olvido de Ebbinghaus:

```
R(t) = a / (log(t+1))^b + c
```

| Tipo | 30 días | 90 días | 180 días | Uso |
|------|---------|---------|----------|-----|
| **Permanente** | 100% | 100% | 100% | Reglas del sistema, patrones fundamentales |
| **Lento** | 71% | 58% | 48% | Patrones técnicos reutilizables |
| **Normal** | 52% | 37% | 29% | Soluciones a problemas específicos |
| **Rápido** | 30% | 18% | 12% | Fixes puntuales, contexto temporal |

Solo se cargan aprendizajes que son **relevantes para la tarea actual** Y que **no han decaído por debajo del umbral**. El conocimiento viejo e irrelevante se desvanece naturalmente. Los patrones críticos persisten para siempre.

---

## Arquitectura de Dos Capas

Innovación v3: **cero duplicación** entre documentación y ejecución.

```
agents/                         .opencode/agents/
(Capa Documental — Obsidian)       (Capa Ejecutable — OpenCode)
 │                                  │
 │  Contexto rico, wikilinks,      │  Config YAML mínima,
 │  misiones, interconexiones      │  instrucciones operativas,
 │                                  │  asignación de modelos
 │                                  │
 └── Fuente de verdad              └── Motor de ejecución
      (legible por humanos)              (ejecutable por máquina)
```

Los archivos `.opencode/` referencian los docs de Obsidian para contexto completo. **42% de reducción** en tokens de la capa ejecutable vs v2.

---

## Skills del Ecosistema

15 skills documentados para patrones reutilizables:

### Core (HIGH)
| Skill | Dominio |
|-------|---------|
| `multi-agent-orchestration` | Orquestación con 11 agentes, 3 flujos adaptativos, delegación, checkpoints |
| `two-layer-architecture` | Patrón documental/ejecutable con cero duplicación |
| `ebbinghaus-memory-system` | Memoria con curva de olvido, índice inteligente, carga bajo demanda |
| `adversarial-critic` | Agente crítico con 6 criterios objetivos de activación |
| `system-verification-portability` | Verificación cross-platform, .gitignore, portabilidad |

### Flujo y Comunicación (MEDIUM)
| Skill | Dominio |
|-------|---------|
| `adaptive-flow-selection` | Selección de flujo corto/medio/largo por complejidad |
| `structured-report-protocol` | Reportes estructurados entre agentes |
| `collaborative-decision-protocol` | Protocolo de decisión colaborativa |
| `intelligent-index-loading` | Índice con señales de relevancia y decay |
| `skill-maintenance-protocol` | Reaprendizaje activo del Librarian |

### Templates y Deploy (MEDIUM)
| Skill | Dominio |
|-------|---------|
| `spec-template-pattern` | Specs verificables con verbos prohibidos |
| `learning-template-pattern` | Destilación de aprendizaje con clusters y decay |
| `review-template-pattern` | Validación PASS/FAIL con hallazgos categorizados |
| `nan-builders-deploy` | Deploy estático para nan.builders + GitHub Pages |

### Clusters (MEDIUM)
| Skill | Dominio |
|-------|---------|
| `dynamic-clusters-pattern` | Clusters dinámicos y red de conocimiento |

---

## Inicio Rápido

### Prerrequisitos

- [Obsidian](https://obsidian.md) (gratis)
- [OpenCode](https://opencode.ai) (CLI para desarrollo con IA)
- Al menos una API key de un modelo de IA

### Instalación

```bash
# 1. Clonar
git clone https://github.com/Ntizar/NtizarBrainMasterMind.git
cd NtizarBrainMasterMind

# 2. Abrir como vault en Obsidian
#    (Archivo → Abrir bóveda → Abrir carpeta como bóveda)

# 3. Configurar API keys en OpenCode
#    (ver docs de OpenCode para setup)

# 4. Verificar instalación
./verify-system.sh    # Linux/macOS/WSL
# o
./verify-system.bat   # Windows

# 5. Iniciar
opencode
# Luego: /ntizar-start
```

### Primera tarea

```bash
# Una vez arrancado, simplemente dale una tarea:
"Crea una landing page para mi portfolio con modo oscuro"
```

El orquestador clasificará, propondrá un flujo, esperará tu confirmación y ejecutará el pipeline completo.

---

## Estructura del Proyecto

```
NtizarBrainMasterMind/
├── AGENTS.md                  # Punto de entrada del sistema
├── index.html                 # 🌐 Web oficial (GitHub Pages)
├── verify-system.sh           # Verificador cross-platform (Linux/macOS/WSL)
├── verify-system.bat          # Verificador Windows
├── .gitignore                 # Ignorar Obsidian cache, IDE, OS files
├── CHANGELOG.md               # Historial de cambios
├── .nojekyll                  # Desactivar Jekyll en GitHub Pages
├── skills/                    # 🆕 15 skills documentados
│   ├── multi-agent-orchestration.md
│   ├── two-layer-architecture.md
│   ├── ebbinghaus-memory-system.md
│   ├── adversarial-critic.md
│   ├── dynamic-clusters-pattern.md
│   ├── system-verification-portability.md
│   ├── intelligent-index-loading.md
│   ├── structured-report-protocol.md
│   ├── adaptive-flow-selection.md
│   ├── collaborative-decision-protocol.md
│   ├── skill-maintenance-protocol.md
│   ├── spec-template-pattern.md
│   ├── learning-template-pattern.md
│   ├── review-template-pattern.md
│   └── nan-builders-deploy.md
│
├── agents/                    # CAPA DOCUMENTAL (Obsidian)
│   ├── 00-orchestrator.md     # ... hasta 10-librarian.md
│   ├── session-prompt.md      # Prompt de activación
│   ├── state/                 # Config del sistema + estado
│   ├── templates/             # Plantillas de intake, spec, review
│   ├── skills/                # Skills de dominio (4 activos)
│   ├── learnings/             # Patrones con metadatos de decaimiento
│   └── projects/              # Hubs de proyectos + clusters
│
├── .opencode/                 # CAPA DE EJECUCIÓN (OpenCode)
│   ├── agents/                # Configs YAML de agentes
│   └── commands/              # /ntizar-start, /ntizar-status, etc.
│
├── learning-platform/         # Brain Academy — plataforma interactiva
├── design-system/             # Liquid Glass CSS (1,379 líneas)
├── docs/                      # Documentación extendida
└── assets/                    # Banner SVG
```

---

## Plataforma de Aprendizaje

> **Brain Academy v3.0** — En vivo: [ntizar-brain-learning.vercel.app](https://ntizar-brain-learning.vercel.app)

Plataforma web interactiva que enseña a construir y usar Ntizar Mastermind. Diseñada para 2 perfiles (con/sin experiencia), con gamificación real.

- 6 módulos interactivos (M0-M5)
- 2 perfiles adaptativos
- Quizzes con feedback inmediato
- XP, badges, confetti
- Guía PDF con diseño Ntizar

---

## Roadmap

### v3.1 actual (Junio 2026)
- [x] Arquitectura de dos capas
- [x] 11 agentes especializados
- [x] Multi-modelo por agente
- [x] Memoria con decaimiento Ebbinghaus
- [x] 15 skills documentados
- [x] Verificación cross-platform
- [x] .gitignore completo
- [x] CHANGELOG.md
- [x] Activación objetiva del Critic (6 criterios)
- [x] Estado de sesión limpio
- [x] Portabilidad total (sin rutas absolutas)
- [x] Plataforma Brain Academy v3.0
- [x] Design System Liquid Glass

### v3.2 — Métricas y Observabilidad
- [ ] Dashboard de métricas del sistema (tokens, PASS/FAIL, reintentos)
- [ ] Registro automático de métricas por ciclo
- [ ] Análisis de rendimiento por agente
- [ ] Alertas de degradación de calidad

### v4.0 — Inteligencia Colaborativa
- [ ] Compartición de conocimiento multi-usuario
- [ ] Marketplace de skills
- [ ] Detección de patrones cross-proyecto
- [ ] Editor visual de flujos
- [ ] Suite de benchmarks

---

## Contribuir

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

Áreas abiertas:
- 🧩 **Nuevos skills** — playbooks para tu dominio
- ⚡ **Optimización de agentes** — mejores prompts, flujos más inteligentes
- 🌐 **Plataforma de aprendizaje** — contenido, traducciones, accesibilidad
- 🔌 **Integración MCP** — trabajo del protocolo multi-agente de v3.2
- 📊 **Métricas y observabilidad** — dashboard de rendimiento
- 📖 **Documentación** — tutoriales, guías, videos
- 🧪 **Testing** — benchmarks y métricas de calidad

---

## Licencia

MIT License — ver [LICENSE](LICENSE).

Usa este sistema, fórkealo, mejóralo. Si te ahorra tiempo, pásalo.

---

<p align="center">
  Hecho con <span style="color: #f97316;">♡</span> por <strong><a href="https://github.com/Ntizar">David Antizar</a></strong>
  <br/>
  <sub>Ntizar Mastermind — porque un mastermind no es un solo genio, sino un grupo de mentes especializadas trabajando juntas.</sub>
</p>

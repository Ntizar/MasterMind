<p align="center">
  <img src="assets/banner.svg" alt="Ntizar Mastermind" width="800"/>
</p>

<h1 align="center">Ntizar Mastermind</h1>

<p align="center">
  <strong>Un framework open-source de orquestación multi-agente con memoria persistente,<br>decaimiento de Ebbinghaus y routing de modelos.</strong>
</p>

<p align="center">
  <a href="https://ntizar.github.io/NtizarBrainMasterMind/">🌐 Web</a> ·
  <a href="#inicio-rápido">Inicio Rápido</a> ·
  <a href="docs/ARCHITECTURE.md">Arquitectura</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-3.0-blue?style=flat-square" alt="Version 3.0"/>
  <img src="https://img.shields.io/badge/agentes-11-orange?style=flat-square" alt="11 Agentes"/>
  <img src="https://img.shields.io/badge/modelos-multi--modelo-green?style=flat-square" alt="Multi-modelo"/>
  <img src="https://img.shields.io/badge/memoria-Ebbinghaus%20decay-purple?style=flat-square" alt="Sistema de Memoria"/>
  <img src="https://img.shields.io/badge/licencia-MIT-lightgrey?style=flat-square" alt="MIT License"/>
  <img src="https://img.shields.io/badge/web-live-blueviolet?style=flat-square" alt="Web en vivo"/>
</p>

---

## Tu IA que realmente recuerda

Usas IA todos los días. Copias y pegas contexto. Re-explicas tu proyecto. Pierdes aprendizajes entre sesiones. Tus prompts son largos, caros y frágiles.

**¿Y si tu IA tuviera cerebro?**

No un chatbot. No un solo prompt. Un sistema estructurado, multi-agente, con memoria persistente, roles especializados y una curva de olvido que mantiene tu contexto ligero y relevante.

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

| Característica | Prompting tradicional | **Ntizar Mastermind v3** |
|---|---|---|
| Contexto | Se pierde cada sesión | **Memoria persistente con decaimiento inteligente** |
| Agentes | Una sola personalidad | **11 agentes especializados con roles definidos** |
| Modelos | Un modelo hace todo | **Cada agente usa su modelo óptimo** |
| Coste | Contexto completo siempre | **40-60% ahorro vía carga inteligente** |
| Calidad | Sin proceso de revisión | **Revisión obligatoria + crítico adversarial** |
| Aprendizaje | Empieza desde cero | **Acumula patrones, skills y conocimiento** |
| Control | La IA decide todo | **Humano en el bucle en cada checkpoint** |

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
R(t) = a / (log(t+1))ᵇ + c
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
./verify-system.bat    # Windows

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
├── verify-system.bat          # Verificador de instalación
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

## Skills de Dominio

Playbooks que los agentes cargan bajo demanda:

| Skill | Dominio | Contenido |
|-------|---------|-----------|
| `software-dev` | Desarrollo | 6 fases obligatorias, matriz de decisiones |
| `dashboard-dev` | Visualización de datos | Pipeline de 6 fases, re-aprendizaje dinámico |
| `web-deploy` | Hosting compartido | Patrón de propagación single-source |
| `pwa-android` | PWA → APK | Stack completo con verificación binaria |

Los skills se cargan **bajo demanda** — solo cuando el clasificador detecta un dominio que coincide. Puedes crear los tuyos usando la plantilla incluida.

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

### v3.0 actual (Marzo 2026)
- [x] Arquitectura de dos capas
- [x] 11 agentes especializados
- [x] Multi-modelo por agente
- [x] Memoria con decaimiento Ebbinghaus
- [x] 4 skills de dominio · 32+ aprendizajes
- [x] Plataforma Brain Academy v3.0
- [x] Design System Liquid Glass

### v3.1 — Optimización MCP
- [ ] Integración nativa de servidor MCP
- [ ] Sistema de presupuesto de tokens
- [ ] Handoffs de agentes en streaming
- [ ] Cache de resultados de agentes
- [ ] Reescritura dinámica de flujos

### v4.0 — Inteligencia Colaborativa
- [ ] Compartición de conocimiento multi-usuario
- [ ] Marketplace de skills
- [ ] Detección de patrones cross-proyecto
- [ ] Editor visual de flujos
- [ ] Suite de benchmarks

---

## Las 12 Reglas

Destiladas de 13 ciclos de uso real:

1. **Flujo completo obligatorio** — ningún agente se salta
2. **Sincronización multi-archivo** — propagar cambios a todos los archivos
3. **Verificar integridad binaria** — magic bytes, no solo extensiones
4. **Deploy consciente de la plataforma** — conocer las limitaciones
5. **README actualizado con cada versión** — siempre al día
6. **El humano decide la arquitectura** — la IA propone, el humano dispone
7. **Clusters dinámicos** — las categorías crecen orgánicamente
8. **Carga bajo demanda** — por relevancia + decaimiento, nunca todos
9. **Capacidad mínima documentada** — cada agente tiene un suelo
10. **Crítico: omitir, nunca degradar** — la calidad no es negociable
11. **Verificar en vivo antes de entregar** — siempre confirmar el deploy
12. **Asignación de modelos es colaborativa** — el sistema propone, el humano confirma

---

## Contribuir

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](CONTRIBUTING.md).

Áreas abiertas:
- 🧩 **Nuevos skills** — playbooks para tu dominio
- ⚡ **Optimización de agentes** — mejores prompts, flujos más inteligentes
- 🌐 **Plataforma de aprendizaje** — contenido, traducciones, accesibilidad
- 🔌 **Integración MCP** — trabajo del protocolo multi-agente de v3.1
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

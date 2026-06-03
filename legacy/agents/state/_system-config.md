# System Config

## Configuración portable del sistema

> **v3.1 — Portabilidad total.** Ninguna ruta absoluta. Todo relativo al workspace.
> Cambiar solo `workspace_root` y `github_local_root` al migrar.

system_name: Ntizar Agent System
version: 3.1
workspace_root: .
default_language: es
naming_convention: kebab-case
github_local_root: ./GitHub/  # relative to workspace_root — change if needed

## Arquitectura v3 — Multi-agente real

> Desde v3, el sistema usa subagentes reales de OpenCode (no role-playing).
> Cada agente es un archivo `.md` en `.opencode/agents/` con su propio modelo configurable.
> Obsidian (`agents/`) es la fuente de verdad documental.
> `.opencode/agents/` es la capa ejecutable. Verificar con `verify-system.sh` o `verify-system.bat`.

### Capas del sistema

| Capa | Ubicación | Función |
|------|-----------|---------|
| Documental (fuente de verdad) | `agents/` | Definiciones completas, Obsidian wikilinks, learnings, skills |
| Ejecutable | `.opencode/agents/` | Archivos OpenCode con frontmatter YAML, modelo configurable |
| Comandos | `.opencode/commands/` | Slash commands: `/ntizar-start`, `/ntizar-status`, `/ntizar-models`, `/ntizar-archive` |

### Agentes ejecutables (`.opencode/agents/`)

| Archivo OpenCode | Modo | Agente Obsidian | Rol |
|-----------------|------|-----------------|-----|
| ntizar-build.md | primary | [[00-orchestrator]] + [[01-classifier]] | Orchestrator + classifier integrado |
| ntizar-plan.md | primary | [[00-orchestrator]] (read-only) | Análisis sin modificar archivos |
| ntizar-explorer.md | subagent | [[02-explorer]] | Contexto y análisis |
| ntizar-planner.md | subagent | [[03-planner]] | Estrategia y pasos |
| ntizar-spec-writer.md | subagent | [[04-spec-writer]] | Spec ejecutable |
| ntizar-implementer.md | subagent | [[05-implementer]] | Ejecución |
| ntizar-reviewer.md | subagent | [[06-reviewer]] | Validación de calidad |
| ntizar-critic.md | subagent | [[07-critic]] | Revisión adversarial |
| ntizar-synthesizer.md | subagent | [[08-synthesizer]] | Comunicación de resultados |
| ntizar-archiver.md | subagent | [[09-archiver]] | Destilación de aprendizaje |
| ntizar-librarian.md | subagent | [[10-librarian]] | Mantenimiento del sistema |

### Cambio clave en v3: Classifier integrado en Orchestrator
El [[01-classifier]] ya no es un subagente separado. Su función está integrada en `ntizar-build.md`
porque necesita contexto completo de la conversación (que los subagentes de OpenCode no reciben).
El archivo `01-classifier.md` se conserva como documentación del proceso de clasificación.

## Modelos — tabla de capacidad por agente

> En v3, el orchestrator PROPONE modelos al humano tras clasificar cada tarea.
> El humano siempre tiene la última palabra. Ver [[_session-state]] regla R9 y R12.
> Si no se especifica modelo en un subagente, hereda el del primary que lo invoca.

| Agente | Nivel mínimo | Degradable | Notas | Modelos recomendados |
|--------|-------------|-----------|-------|---------------------|
| orchestrator+classifier | Alto | No | Pierde el hilo con modelo débil | Claude Opus, GPT-4o |
| explorer | Medio | Sí | Contexto estructurado permite modelo menor | Gemini 2.5 Pro (contexto largo), Claude Sonnet |
| planner | Alto/Medio | Parcial | Medio solo si tarea simple | Claude Sonnet, GPT-4o |
| spec-writer | Medio-Alto | Parcial | Medio si el plan ya es detallado | Claude Sonnet |
| implementer | Alto/Medio | Parcial | Alto para código no trivial | Claude Opus, Claude Sonnet |
| reviewer | Medio | Sí | Criterios concretos permiten modelo menor | Claude Sonnet, Gemini Flash |
| critic | Alto | No | **Omitir antes que degradar** — notificar al humano | Claude Opus |
| synthesizer | Bajo-Medio | Sí | Más degradable — solo reformatea | Claude Haiku, Gemini Flash |
| archiver | Bajo | Sí | Más mecánico del sistema | Claude Haiku, Gemini Flash |
| librarian | Bajo | Sí | Excepto evaluación de obsolescencia | Claude Haiku, Gemini Flash |

## Degradabilidad por fase (orchestrator)

| Fase | Degradable | Condición |
|------|-----------|-----------|
| CLASSIFY | No | Integrada en orchestrator — siempre modelo alto |
| EXPLORE | Sí | Si contexto es estructurado |
| PLAN | Parcial | Solo en baja complejidad |
| SPEC | Parcial | Si plan ya es detallado |
| IMPLEMENT | Depende | Ver nivel mínimo del implementer |
| REVIEW | Sí | Si criterios son concretos |
| CRITIC | No | Omitir antes que degradar |
| SYNTHESIZE | Sí | Siempre — más degradable |
| ARCHIVE | Sí | Siempre — más mecánica |
| LIBRARIAN | Sí | Salvo evaluación de skills |

## Sistema de decay (Ebbinghaus)

> Desde v3, los learnings tienen relevancia temporal calculada con la curva de Ebbinghaus.
> Ver documentación completa en [[_index|learnings/_index]].

Fórmula: `R(t) = a / (log(t+1))^b + c` donde t = días desde la fecha del learning.

| Tipo decay | R(30d) | R(90d) | R(180d) | Uso |
|-----------|--------|--------|---------|-----|
| permanente | 1.0 | 1.0 | 1.0 | Reglas del sistema |
| lento | ~0.71 | ~0.58 | ~0.48 | Patrones técnicos |
| normal | ~0.52 | ~0.37 | ~0.29 | Soluciones específicas |
| rápido | ~0.30 | ~0.18 | ~0.12 | Fixes puntuales |

- Learnings con R(t) < 0.2 durante 60+ días → archivables (mover a `learnings/archive/`)
- El orchestrator calcula R(t) mentalmente al leer `_index.md` — sin scripts externos

## Reglas de portabilidad
- Usar siempre rutas relativas desde workspace_root
- Nunca referenciar rutas absolutas en archivos del sistema
- `agents/` = documentación completa (Obsidian). `.opencode/agents/` = config ejecutable
- En nuevo ordenador: copia carpeta completa y edita solo este archivo
- Verificar con `verify-system.sh` (Linux/macOS/WSL) o `verify-system.bat` (Windows)

## Instalación en nuevo ordenador
1. Copia la carpeta completa al nuevo vault (incluye `agents/` y `.opencode/`)
2. Abre este archivo y ajusta `workspace_root` y `github_local_root`
3. Verifica que `agents/skills/_index` no tenga rutas absolutas
4. Ejecuta `verify-system.sh` (Linux/macOS/WSL) o `verify-system.bat` (Windows)
5. Abre OpenCode apuntando al vault
6. Usa `/ntizar-start` o [[session-prompt]] para activar

## Multi-modelo: implementado en v3

> **Estado: IMPLEMENTADO.** Desde v3, cada subagente puede correr con un modelo diferente.
> Se configura en el frontmatter `model:` de cada `.opencode/agents/*.md`.
> El orchestrator propone modelos tras clasificar — el humano siempre decide.

**Beneficio real:**
- Explorer con modelo de contexto largo (Gemini 2.5 Pro, 1M tokens)
- Implementer con modelo de alta capacidad (Claude Opus, GPT-4o)
- Archiver/Synthesizer con modelo económico (Haiku, Flash)
- Ahorro de coste estimado ~40-60% manteniendo calidad

## Activación objetiva del Critic (v3.1)

> **Nuevo en v3.1.** El orchestrator activa el Critic automáticamente cuando se cumple ≥1 criterio:
> 1. Complejidad ≥ 4 (según classifier)
> 2. ≥ 3 reintentos en cualquier fase
> 3. Entregables ≥ 3 archivos en tareas software
> 4. Tarea software con impacto alto
> 5. Reviewer emite WARNINGs (aunque PASS)
> 6. Humano solicita explícitamente

Si ninguno se cumple → Critic omitido con notificación al humano.

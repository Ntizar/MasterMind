---
nombre: Ntizar Brain
tipo: sistema
descripcion: Sistema de inteligencia operativa general sobre Obsidian + OpenCode
version: 3.1
actualizado: 2026-06-03
---

# Sistema de Agentes — Ntizar Brain v3

## Qué es esto
Sistema de inteligencia operativa general sobre Obsidian + OpenCode.
Ejecuta cualquier tarea: técnica, estratégica, creativa, analítica, documental u operativa.

## Arquitectura

Dos capas, sin duplicación:

| Capa | Ubicación | Qué contiene |
|------|-----------|-------------|
| Documental | `agents/` | Definiciones completas con wikilinks, misión, contexto, conexiones (Obsidian) |
| Ejecutable | `.opencode/agents/` | Config YAML + instrucciones operativas mínimas (OpenCode) |
| Comandos | `.opencode/commands/` | `/ntizar-start`, `/ntizar-status`, `/ntizar-models`, `/ntizar-archive` |

Cada archivo `.opencode/` referencia su archivo Obsidian para detalle completo.
Cada archivo Obsidian indica su ejecutable en la sección "Ejecutable OpenCode".

## Cómo activarlo

**Opción A — Comando OpenCode (recomendado):**
Usa `/ntizar-start` para arrancar.

**Opción B — Manual:**
El orchestrator lee al arrancar:
1. Este archivo (AGENTS.md)
2. [[00-orchestrator]]
3. [[_system-config]]
4. [[_session-state]]
5. [[_index|skills/_index]]
6. [[_index|learnings/_index]]
7. [[_clusters]]

Los learnings individuales se cargan bajo demanda — filtrados por señal de relevancia Y decay R(t) > 0.3.

## Agentes

### Primarios (el humano elige uno al abrir OpenCode)

| Agente | Modo | Cuándo usar |
|--------|------|-------------|
| `ntizar-build` | Trabajo completo (lee + escribe) | Sesiones de ejecución |
| `ntizar-plan` | Solo lectura | Exploración y análisis sin modificar nada |

### Subagentes (delegados por el orchestrator via Task tool)

| Agente | Documentación | Rol |
|--------|--------------|-----|
| ntizar-explorer | [[02-explorer]] | Analiza contexto sin modificar |
| ntizar-planner | [[03-planner]] | Diseña estrategia y pasos |
| ntizar-spec-writer | [[04-spec-writer]] | Genera spec ejecutable |
| ntizar-implementer | [[05-implementer]] | Ejecuta la spec |
| ntizar-reviewer | [[06-reviewer]] | Valida calidad — PASS/FAIL |
| ntizar-critic | [[07-critic]] | Revisión adversarial (omitir antes que degradar) |
| ntizar-synthesizer | [[08-synthesizer]] | Comunica resultados al humano |
| ntizar-archiver | [[09-archiver]] | Destila aprendizaje con decay |
| ntizar-librarian | [[10-librarian]] | Mantiene skills, índices, clusters |

El [[01-classifier]] está integrado en el orchestrator (necesita contexto completo de conversación).

## Multi-modelo

Tras clasificar cada tarea, el orchestrator **propone** qué modelo usar para cada subagente.
El humano siempre confirma o modifica. Si no se especifica modelo, hereda el del primary.
Ver tabla de capacidad mínima en [[_system-config]].

## Tipos de tarea soportados
- **Software:** programación, refactorización, debugging, arquitectura
- **Research:** análisis, síntesis, comparativas, validación de fuentes
- **Estrategia:** planes, decisiones, evaluaciones, roadmaps
- **Escritura:** documentos, briefs, emails, contenido, SOPs
- **Operaciones:** procesos, flujos, automatizaciones, checklists
- **Conocimiento:** organización en Obsidian, taxonomías, mapas mentales
- **Creatividad:** brainstorming, conceptos, propuestas
- **Análisis de datos:** interpretación, resúmenes ejecutivos, visualización

## Cómo dar tareas

**Lenguaje natural** o con [[task-intake]] para tareas complejas.

**Checkpoints humanos:**
- Después de CLASSIFY → confirma modelos propuestos (o di "ok")
- Después de SPEC → aprueba con ✅ o da feedback
- Después de SYNTHESIZE → aprueba con ✅ para archivar

## Reglas globales

Las reglas permanentes del sistema (R1-R12) están en [[_session-state]].
Las más críticas:

1. Flujo completo obligatorio — ningún agente se salta, aunque emita "PASS SIN HALLAZGOS"
2. Spec aprobada antes de implementar
3. No se archiva sin reviewer PASS y ✅ humano
4. El orchestrator pregunta al humano antes de decidir diseño/arquitectura
5. El orchestrator **propone** modelos — nunca decide en silencio
6. Learnings con decay Ebbinghaus — ver [[_index|learnings/_index]]
7. Sistema portátil — ver [[_system-config]] + `verify-system.bat`

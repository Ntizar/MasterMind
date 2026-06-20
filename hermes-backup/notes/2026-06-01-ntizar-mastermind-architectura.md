# Ntizar Mastermind — Sistema de Orquestación Multi-Agente

**Fecha:** 2026-06-01  
**Tipo:** conocimiento  
**Clusters:** multi-agent, orquestacion, memoria-ebbinghaus  
**Decay:** lento  

## Resumen

Ntizar Mastermind es un framework open-source de orquestación multi-agente que funciona sobre OpenCode + Obsidian. Es el sistema operativo cerebral de David Antizar.

## Arquitectura

### 11 Agentes Especializados

| # | Agente | Rol | Modelo recomendado | Degradable |
|---|--------|-----|-------------------|------------|
| 00 | Orchestrator | Clasifica, diseña flujos, delega | Claude Opus / GPT-4o | NO |
| 01 | Classifier | Evalúa complejidad, dominio, ambigüedad | Claude Opus / GPT-4o | NO (integrado en 00) |
| 02 | Explorer | Lee contexto sin modificar nada | Gemini 2.5 Pro | Sí |
| 03 | Planner | Define estrategia y pasos | Claude Opus / Sonnet | Sí |
| 04 | Spec Writer | Convierte plan en spec ejecutable | Claude Sonnet | Sí |
| 05 | Implementer | Ejecuta la spec | Claude Sonnet / Flash | Sí |
| 06 | Reviewer | Validación PASS/FAIL | Claude Sonnet / Flash | Sí |
| 07 | Critic | Revisión adversarial | Claude Opus / GPT-4o | NO (se omite si no hay alto) |
| 08 | Synthesizer | Transforma reportes en resultados legibles | Claude Haiku / Flash | Sí |
| 09 | Archiver | Destila aprendizajes con metadata de decaimiento | Claude Haiku / Flash | Sí |
| 10 | Librarian | Mantiene grafo de conocimiento | Claude Haiku / Flash | Sí |

### Reglas Críticas

1. **Todos los agentes del flujo deben pasar siempre** — ninguno se salta. Si no hay trabajo sustancial, emite "PASS SIN HALLAZGOS".
2. **El Critic nunca se degrada** — si no hay modelo alto disponible, se omite completamente.
3. **Protocolo de decisión colaborativa** — antes de decisiones de diseño/architectura con más de una opción válida, DEBE preguntar al humano.
4. **Máximo 2 reintentos por fase**.
5. **Checkpoints al humano** con contexto claro en cada fase crítica.

### Flujos Adaptativos

- **Flujo largo** (técnica compleja): EXPLORE → PLAN → SPEC → IMPLEMENT → REVIEW → CRITIC → SYNTHESIZE → ARCHIVE
- **Flujo medio** (estratégica): EXPLORE → PLAN → IMPLEMENT → REVIEW → SYNTHESIZE → ARCHIVE
- **Flujo corto** (simple): IMPLEMENT → REVIEW → SYNTHESIZE

### Arquitectura de Dos Capas (v3)

```
agents/                    .opencode/agents/
(Obsidian - Documentación)     (OpenCode - Ejecución)
```

- Obsidian: contexto rico, wikilinks, misiones, interconexiones
- OpenCode: config YAML mínima, instrucciones operativas
- **42% de reducción** en contenido ejecutable vs v2

## Memoria con Decaimiento Ebbinghaus

Fórmula: `R(t) = a / (log(t+1))^b + c`

| Tipo | 30 días | 90 días | 180 días | Uso |
|------|---------|---------|----------|-----|
| Permanente | 100% | 100% | 100% | Reglas del sistema, patrones fundamentales |
| Lento | 71% | 58% | 48% | Patrones técnicos reutilizables |
| Normal | 52% | 37% | 29% | Soluciones a problemas específicos |
| Rápido | 30% | 18% | 12% | Fixes puntuales, contexto temporal |

### Librarian Protocol

- Si R(t) < 0.2 Y 60+ días → archivar a `learnings/archive/`
- **NUNCA borrar** — solo archivar
- Detecta skills con "reaprendizaje activo" y actualiza patrones automáticamente

## Aprendizajes del Archiver

Formato de aprendizaje v2:
- clusters, proyecto, patrón, decay
- Decisión clave (1 oración)
- Patrón reutilizable
- Qué funcionó / qué evitar
- Skills usados
- Criterios de éxito

## Coste Optimization

Multi-modelo inteligente:
- Alto razonamiento (Orchestrator, Critic) → Claude Opus / GPT-4o
- Contexto largo (Explorer) → Gemini 2.5 Pro
- Generación (Implementer) → Claude Sonnet
- Mecánico (Synthesizer, Archiver) → Claude Haiku / Flash

**Resultado:** 40-60% ahorro en tokens vs usar un solo modelo caro.

---
name: multi-agent-orchestration
description: Patrón de orquestación multi-agente con 11 agentes especializados, flujo adaptativo de 3 niveles, protocolo de delegación y gestión de errores.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [orquestación, multi-agente, flujo-adaptativo, delegación, checkpoints]
---

# Patrón de Orquestación Multi-Agente

## Qué es

Patrón de orquestación que coordina **11 agentes especializados** en un flujo adaptativo de 3 niveles (corto/medio/largo). Cada agente tiene un rol definido, una capacidad de procesamiento (alto/medio/bajo) y un modelo asignado. El orchestrator central gestiona la delegación, los checkpoints humanos, la gestión de errores con reintentos y la asignación de modelos por subagente.

### Los 11 agentes

| Agente | Abrev. | Capacidad | Rol principal |
|--------|--------|-----------|---------------|
| Orchestrator | ORCH | Alto | Coordina todo el flujo, clasifica tareas, asigna modelos |
| Explorer | EXP | Alto | Analiza contexto, explora repositorio sin modificar |
| Planner | PLANN | Alto | Diseña estrategia, pasos y decisiones clave |
| Spec Writer | SPEC | Medio | Genera especificación ejecutable |
| Implementer | IMP | Alto | Ejecuta la spec, escribe código |
| Reviewer | REV | Medio | Valida calidad — emite PASS/FAIL |
| Critic | CRIT | Medio | Revisión adversarial (activación condicional) |
| Synthesizer | SYNTH | Medio | Comunica resultados al humano |
| Archiver | ARCH | Bajo | Destila aprendizaje con decay Ebbinghaus |
| Librarian | LIB | Bajo | Mantiene skills, índices, clusters |
| Classifier | CLASS | Alto | Integrado en orchestrator, clasifica tipo de tarea |

### Flujo adaptativo de 3 niveles

```
NIVEL CORTO (≤2 pasos, ≤2 archivos):
  ORCH → CLASSIFY → SPEC → IMP → REV → SYNTH → ARCH

NIVEL MEDIO (3-5 pasos, 3-7 archivos):
  ORCH → CLASSIFY → EXP → PLANN → SPEC → IMP → REV → SYNTH → ARCH

NIVEL LARGO (≥6 pasos, ≥8 archivos):
  ORCH → CLASSIFY → EXP → PLANN → SPEC → IMP → REV → CRIT → SYNTH → ARCH → LIB
```

El nivel se decide en la fase CLASSIFY según: complejidad de la tarea, número de archivos entregables estimados y si requiere análisis previo del contexto.

### Modelo de capacidad por agente

Cada agente tiene una capacidad de procesamiento clasificada en **alto**, **medio** o **bajo**. Los agentes de capacidad **degradable** pueden reducir su nivel en caso de sobrecarga:

- **Alto**: Pueden procesar tareas complejas sin degradación. Ej: orchestrator, explorer, implementer.
- **Medio**: Requieren contexto bien estructurado. Pueden degradarse a bajo si el contexto es ambiguo. Ej: spec-writer, reviewer, critic, synthesizer.
- **Bajo**: Solo procesan tareas simples y bien definidas. Se degradan automáticamente si el contexto excede su alcance. Ej: archiver, librarian.

### Asignación de modelos por subagente

Tras clasificar cada tarea, el orchestrator **propone** qué modelo usar para cada subagente. El humano siempre confirma o modifica. Si no se especifica modelo, cada subagente hereda el del primary.

```yaml
# Ejemplo de asignación propuesta por orchestrator
modelos_propuestos:
  orchestrator: "claude-sonnet-4-20250514"
  explorer: "claude-sonnet-4-20250514"
  planner: "claude-sonnet-4-20250514"
  spec-writer: "claude-sonnet-4-20250514"
  implementer: "deepseek-v3"
  reviewer: "claude-sonnet-4-20250514"
  critic: "claude-sonnet-4-20250514"
  synthesizer: "claude-sonnet-4-20250514"
  archiver: "gpt-4o-mini"
  librarian: "gpt-4o-mini"
```

## Cuándo usar

- Cualquier tarea que requiera más de un tipo de habilidad (explorar + planificar + implementar + validar)
- Tareas con complejidad ≥ 3 en la escala del sistema
- Cuando se necesitan múltiples archivos entregables (≥ 3)
- Tareas de estrategia, arquitectura o diseño donde la validación adversarial es valiosa
- Cuando el humano quiere mantener control en checkpoints clave

## Pasos

### Paso 1 — Clasificación (CLASSIFY)

El orchestrator clasifica la tarea y determina el nivel del flujo:

```
[CLASSIFY]
tarea: "Migrar frontend a nuevo framework"
complejidad: 5
archivos_estimados: 12
nivel: LARGO
modelos_propuestos: { ... }
```

**Checkpoint humano:** El humano confirma o modifica los modelos propuestos. Si dice "ok", el flujo avanza.

### Paso 2 — Exploración (solo nivel medio/largo)

```
[EXPLORE]
rango: "src/components/, src/pages/"
sin_modificar: true
resultado: "Análisis de estructura actual, dependencias, patrones existentes"
```

### Paso 3 — Planificación (solo nivel medio/largo)

```
[PLAN]
pasos:
  - "Refactorizar componentes base"
  - "Migrar páginas"
  - "Actualizar rutas"
  - "Verificar build"
decisiones_clave:
  - "Framework destino: React 19 con Server Components"
  - "CSS: mantener Tailwind, migrar a config v4"
```

### Paso 4 — Especificación (SPEC)

El spec-writer genera una especificación ejecutable con pasos detallados.

**Checkpoint humano:** El humano aprueba la spec con ✅ o da feedback. Sin spec aprobada, no se implementa.

### Paso 5 — Implementación (IMP)

El implementer ejecuta la spec. Cada paso se valida contra la spec antes de continuar.

### Paso 6 — Revisión (REV)

El reviewer valida la implementación contra la spec. Emite PASS o FAIL con hallazgos.

### Paso 7 — Crítica adversarial (solo nivel largo, condicional)

El critic valida contra el mundo real, no contra la spec. Ver [[adversarial-critic]] para detalles.

### Paso 8 — Síntesis (SYNTH)

El synthesizer comunica los resultados al humano de forma clara y concisa.

**Checkpoint humano:** El humano aprueba con ✅ para archivar.

### Paso 9 — Archivado (ARCH)

El archiver destila el aprendizaje con decay Ebbinghaus. Ver [[ebbinghaus-memory-system]].

### Paso 10 — Mantenimiento (solo nivel largo)

El librarian actualiza índices, clusters y skills si es necesario.

## Pitfalls

- **Saltar un agente:** El flujo completo es obligatorio. Ningún agente se salta, aunque emita "PASS SIN HALLAZGOS".
- **Delegar sin contexto:** Cada subagente necesita el contexto completo hasta su punto de entrada. No delegar con contexto insuficiente.
- **Modelo inadecuado:** Usar un modelo de capacidad baja para una tarea de complejidad alta genera errores en cascada.
- **Sin checkpoint humano:** No avanzar sin la aprobación humana en los checkpoints de CLASSIFY, SPEC y SYNTH.
- **Over-delegación:** No delegar tareas triviales (un archivo, un cambio menor) a todo el flujo. Usar nivel corto.

## Verificación

1. ✅ El orchestrator clasifica la tarea y propone modelos antes de delegar
2. ✅ El nivel del flujo (corto/medio/largo) coincide con la complejidad
3. ✅ Cada checkpoint humano se cumple antes de avanzar
4. ✅ El flujo completo se ejecuta sin saltos, incluso si hay "PASS SIN HALLAZGOS"
5. ✅ La spec está aprobada antes de que el implementer empiece
6. ✅ Los modelos asignados coinciden con la capacidad de cada agente
7. ✅ El archiver destila el aprendizaje al final de cada flujo completo

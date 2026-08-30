---
name: skillopt
description: Use al iterar skills de agentes LLM con validación y gates.
version: 1.0.0
tags: [agent-skills, self-evolving-agents, llm, meta-learning, mastermind]
author: David Antizar
license: MIT
metadata:
  hermes:
    tags: [agent-skills, llm, meta-learning]
    related_skills: [hermes-agent-skill-authoring]
---

# SkillOpt — Skills entrenables para agentes congelados

## When to Use

- Al iterar o mejorar un SKILL.md tras tareas con correcciones manuales repetidas.
- Al querer aplicar validación anti-regresión antes de hacer patch de un skill.


Repo: https://github.com/microsoft/SkillOpt (MIT, ~16.5k⭐, PyPI `skillopt`, Python 3.10+)
Paper: https://arxiv.org/abs/2605.23904 · Docs: https://microsoft.github.io/SkillOpt/

## Idea central

Entrena **skills en lenguaje natural** para un agente LLM con pesos congelados, como si fuera una red neuronal:

- **Epochs / batch-size / learning rate** sobre trajectorias del agente
- **Ediciones guiadas por trajectoria**: analiza fallos/éxitos de ejecución y edita el texto del skill
- **Validation gates**: una actualización del skill solo se acepta si mejora en un conjunto de validación (evita regresiones)
- **Artefacto desplegable**: `best_skill.md` — un markdown que se carga en el prompt del agente

## Aplicación práctica al sistema Mastermind

Patrones transferibles a `agent/skills/`:

1. **Skill = artefacto versionado entrenable**: tratar SKILL.md como parámetro optimizable, no como documento estático.
2. **Loop de mejora**: ejecutar tarea → recopilar trajectoria (qué steps fallaron, qué corregí a mano) → editar skill → re-ejecutar una tarea de validación conocida antes de aceptar el cambio.
3. **Validation gate manual**: antes de hacer patch de un skill, repetir mentalmente un caso de prueba real (tarea pasada vía session_search) y comprobar que el skill actual lo resuelve mejor que antes.
4. **Anti-regresión**: nunca reemplazar secciones que funcionan; ediciones incrementales con `skill_manage(action='patch')`, conservando pasos verificados.
5. **Regeneración desde trajectorias**: cuando una corrección manual se repite 2+ veces (visible en session_search), es señal de que el skill necesita ese conocimiento destilado.

## Instalación / uso directo

```bash
pip install skillopt
# Requiere API OpenAI-compatible (compatible con NaN.builders vía base_url)
# Entrenamientos con ALFWorld y otros benchmarks gymnasium en docs/
```

## Pitfalls

- Es alfa (Development Status 3); los benchmarks incluidos (ALFWorld) no representan tareas reales tipo GIS/dashboards — lo valioso son los patrones, no el pipeline literal.
- El validation gate requiere tareas repetibles y medibles; para tareas exploratorias usa criterios cualitativos.
- No toca pesos del modelo: solo mejora el prompt/skill; un skill perfecto no arregla un modelo inadecuado.

## Verificación

- Repo accesible y PyPI: `pip index versions skillopt`
- Tras aplicar un patrón a un skill de Mastermind: re-ejecutar la tarea tipo y confirmar mejora (menos correcciones manuales).

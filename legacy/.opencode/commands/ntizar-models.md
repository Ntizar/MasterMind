---
description: "Propone y configura modelos para cada subagente de la sesion"
agent: ntizar-build
---

Lee el archivo agents/state/_system-config.md para ver la tabla de capacidad por agente.

Luego emite la PROPUESTA DE MODELOS para la sesion actual.
Considera:
- El modelo principal con el que estoy corriendo ahora
- La tarea que se va a ejecutar (si hay alguna en curso, consulta agents/state/_session-state.md)
- Los modelos disponibles: anthropic/claude-opus-4, anthropic/claude-sonnet-4, anthropic/claude-haiku-3-5, google/gemini-2.5-pro, openai/gpt-4o, openai/o3

Si el humano pasa argumentos con este comando, interpretarlos como instrucciones de configuracion.
Ejemplo: /ntizar-models "usa haiku para todo excepto implementer"

$ARGUMENTS

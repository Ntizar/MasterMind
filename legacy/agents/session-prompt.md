# Session Prompt — Ntizar Agent System

## Cómo usar este archivo
Copia el bloque de texto de abajo y pégalo tal cual al inicio de cualquier sesión nueva en OpenCode.
No lo modifiques. El sistema se activa solo.

---

## Prompt de activación (copy-paste)

```
Lee los siguientes archivos en este orden exacto:
1. AGENTS.md
2. agents/00-orchestrator.md
3. agents/state/_system-config.md
4. agents/state/_session-state.md
5. agents/skills/_index.md
6. agents/learnings/_index.md
7. agents/projects/_clusters.md

IMPORTANTE: NO cargues learnings individuales todavía.
El _index.md de learnings tiene toda la información para decidir qué cargar.
Los learnings completos se cargan solo cuando la señal de relevancia del índice
coincide con la tarea activa — bajo demanda, no al arranque.

Cuando hayas leído los 7 archivos, responde con este formato exacto y nada más:

SISTEMA ACTIVO
──────────────
Skills cargados: [N] → [nombres separados por coma]
Learnings en índice: [N] (ninguno cargado completo aún)
Clusters activos: [N] → [nombres separados por coma]
Proyectos activos: [N] → [nombres separados por coma]
Última tarea completada: [nombre o "ninguna"]
Estado: [tarea_activa del session-state o "en reposo"]

Esperando tarea.
```

---

## Notas de uso

- Si el sistema responde con un formato distinto, repite el prompt
- Si `_session-state.md` tiene una `tarea_activa` distinta de "ninguna",
  el sistema puede reanudar desde la última fase — pregunta si quieres continuar o empezar nuevo
- Para dar una tarea, escríbela en lenguaje natural después de recibir "Esperando tarea"
- Para tareas complejas con mucho contexto, rellena `agents/templates/task-intake.md` primero
  y pega su contenido junto con tu instrucción
- Para activar modo ahorro de tokens desde el inicio: añade "Modo ahorro activo" al final del prompt

---

## Actualización de este archivo
Si añades nuevos skills, proyectos o cambias la estructura del sistema, no necesitas tocar este prompt.
Los pasos 5, 6 y 7 siempre cargan los índices actualizados automáticamente.

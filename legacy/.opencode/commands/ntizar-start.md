---
description: "Inicia el sistema Ntizar Brain - carga archivos de arranque y espera tarea"
agent: ntizar-build
---

Ejecuta la secuencia de arranque completa del sistema Ntizar Brain:

1. Lee agents/00-orchestrator.md
2. Lee agents/state/_system-config.md
3. Lee agents/state/_session-state.md
4. Lee agents/skills/_index.md
5. Lee agents/learnings/_index.md
6. Lee agents/projects/_clusters.md

Despues de cargar, presenta:
```
NTIZAR BRAIN v3 — SISTEMA ACTIVO
=================================
Modelo principal: [el modelo actual]
Skills activos: [numero]
Learnings disponibles: [numero]
Clusters: [numero]

Esperando tarea. Describe que necesitas.
```

Si se pasan argumentos, interpretarlos como la primera tarea:
$ARGUMENTS

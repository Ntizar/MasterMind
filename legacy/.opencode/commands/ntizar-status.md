---
description: "Muestra el estado actual de la sesion Ntizar Brain"
agent: ntizar-build
subtask: true
---

Lee los siguientes archivos y presenta un resumen del estado actual:
1. agents/state/_session-state.md
2. agents/state/_system-config.md
3. agents/learnings/_index.md (solo contar filas, no leer learnings)
4. agents/skills/_index.md
5. agents/projects/_clusters.md

Presenta el estado en este formato:

```
ESTADO DE SESION — NTIZAR BRAIN v3
===================================
Tarea activa: [tarea o "ninguna"]
Fase actual: [fase o "ninguna"]
Ultimo checkpoint: [descripcion]

RECURSOS:
  Skills activos: [numero] -> [lista]
  Learnings registrados: [numero]
  Clusters activos: [numero] -> [lista]
  Proyectos con hub: [numero] -> [lista]

REGLAS PERMANENTES: [numero] reglas (R1-RN)
```

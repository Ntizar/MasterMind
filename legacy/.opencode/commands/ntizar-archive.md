---
description: "Archiva el learning del ultimo ciclo completado"
agent: ntizar-archiver
---

Archiva el learning del ciclo que acaba de completarse.

Si se pasan argumentos, usarlos como nombre de la tarea:
$ARGUMENTS

Proceso:
1. Revisa el contexto de la conversacion actual para extraer:
   - Classifier Report
   - Plan / Spec
   - Implementer Report
   - Reviewer Report
2. Crea el archivo de learning en agents/learnings/
3. Actualiza agents/learnings/_index.md con la nueva fila (incluyendo campo decay)
4. Actualiza agents/projects/_clusters.md si hay clusters o proyectos nuevos
5. Presenta un resumen de lo archivado

---
fecha: 2026-03-25
tarea: gamificacion-badges-y-pdf
tipo: software
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: gamification-with-badges
---

# Learning Platform v2 — Gamificación con Badges y PDF Export

## Decisión clave
Añadir sistema de 7 badges desbloqueables + export a PDF de 1 página con guía de instalación. Los badges se checkean automáticamente al ganar XP. El PDF reemplaza el export JSON.

## Patrón reutilizable
**Nombre:** gamification-with-badges
**Descripción:** Para plataformas educativas: (1) Definir array de badges con id, nombre, icono, descripción y función check, (2) Checkear badges al completar acciones (XP, módulos, quizzes), (3) Mostrar badges en finish modal con tooltip, (4) Alert al desbloquear.

## Qué funcionó
- 7 badges: Primera Misión, Arquitecto, Domador de Agentes, Rápido y Furioso, Francotirador, Graduado, Maestro Brain
- Cada badge tiene función `check(state)` que evalúa si se cumple
- Auto-check al awardXP() — sin código extra en cada acción
- PDF con jsPDF: header azul, 4 pasos de instalación, stats del usuario, QR code
- Finish modal responsive con badges grid

## Qué evitar
- No hardcodear badge checks — usar funciones reutilizables
- No hacer PDF de múltiples páginas — mantener en 1 página
- No mostrar badges vacíos — si no tiene ninguno, mostrar mensaje motivacional

## Skills usados
- software-dev.md (jsPDF integration, gamification logic)

## Criterios que validaron el éxito
- 7 badges definidos en array BADGES
- Función checkBadges() que evalúa todos los badges
- Alert al desbloquear badge con icono y nombre
- PDF se descarga con nombre personalizado
- Finish modal muestra badges desbloqueados (o mensaje si no tiene)

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: medio (~20min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-platform-v2-simplificado-robusto]] · [[2026-03-25-pdf-export-guia-instalacion]]

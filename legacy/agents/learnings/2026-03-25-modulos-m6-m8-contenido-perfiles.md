---
fecha: 2026-03-25
tarea: modulos-m6-m8-contenido-perfiles
tipo: software
complejidad: alta
clusters: [sistema, web]
proyecto: learning-platform
patron: profile-specific-guided-projects
---

# Learning Platform v2 — Módulos M6-M8 con Proyectos por Perfil

## Decisión clave
Crear M6-M8 con contenido específico por perfil: (1) M6 guía primer proyecto real, (2) M7 tiene 12 ejemplos concretos (3 por perfil: writer, analyst, developer, manager), (3) M8 enseña a replicar el sistema completo con plantillas.

## Patrón reutilizable
**Nombre:** profile-specific-guided-projects
**Descripción:** Para plataformas multi-perfil: después de los módulos teóricos (M0-M5), añadir módulos prácticos (M6-M8) con: (1) selector de proyecto por perfil, (2) ejemplos copy-paste listos para usar, (3) guía paso a paso para replicar el sistema. Enfocado en acción inmediata, no teoría.

## Qué funcionó
- **M6**: Guía primer proyecto real con flujo completo (10 pasos) + prompt template
- **M7**: **12 ejemplos concretos** organizados por perfil:
  - Writer: artículo blog, SOP, resumen de documentos
  - Analyst: CSV ventas, dashboard, propuesta comercial
  - Developer: landing page, debuggear, refactorizar
  - Manager: onboarding, documentar proceso, retrospectiva
- **M8**: Guía para replicar sistema completo + 2 plantillas (skill, learning) + tabla componentes esenciales

## Qué evitar
- No dar teoría sin práctica — cada ejemplo es copy-paste directo a OpenCode
- No asumir conocimiento técnico — lenguaje natural, sin jerga
- No olvidar el "por qué" — cada ejemplo explica qué hace el sistema

## Skills usados
- software-dev.md (estructura de contenido educativo)
- dashboard-dev.md (organización de información por categorías)

## Criterios que validaron el éxito
- M6: 1 flujo completo paso a paso + prompt template
- M7: 12 ejemplos (3 por perfil × 4 perfiles)
- M8: Tabla de 6 componentes + 5 pasos replicar + 2 plantillas
- Todo en lenguaje natural, sin código técnico
- Enfoque en "replicar y usar" no en "entender teoría"

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: alto (~35min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-modules-v2-contenido-completo-enriquecido]] · [[2026-03-25-contenido-calidad-m1-m2-mejorado]]

---

## 📊 Contenido M6-M8

| Módulo | Elementos | Ejemplos | Plantillas |
|--------|-----------|----------|------------|
| M6 | 1 flujo completo | 1 proyecto guiado | 1 prompt template |
| M7 | 4 secciones perfil | 12 ejemplos | 0 |
| M8 | 3 secciones | 0 | 2 (skill, learning) |
| **Total** | **8** | **13** | **3** |

**Objetivo:** Que cualquier usuario (incluso sin conocimiento técnico) pueda:
1. Usar el sistema con su primera tarea real (M6)
2. Copiar ejemplos de su perfil (M7)
3. Replicar el sistema para otros proyectos (M8)

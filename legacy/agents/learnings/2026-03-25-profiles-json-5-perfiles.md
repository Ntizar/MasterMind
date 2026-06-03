---
fecha: 2026-03-25
tarea: profiles-json-5-perfiles
tipo: software
complejidad: baja
clusters: [sistema, web]
proyecto: learning-platform
patron: user-profile-personalization
---

# Learning Platform v2 — Sistema de 5 Perfiles de Usuario

## Decisión clave
Crear un archivo `profiles.json` que define vocabulario, ejemplos, casos de uso y duración para cada tipo de usuario, permitiendo personalización real del contenido.

## Patrón reutilizable
**Nombre:** user-profile-personalization
**Descripción:** Para plataformas educativas multi-usuario, definir perfiles con: (1) vocabulario a evitar/usar, (2) ejemplos de dominio relevante, (3) casos de uso específicos, (4) duración estimada por módulo. Esto permite adaptar contenido sin duplicar código.

## Qué funcionó
- Estructura JSON clara con 5 perfiles distintos
- Cada perfil tiene icono, descripción y vocabulario específico
- Campos `evitar` y `usar` para adaptar lenguaje técnico
- Duración diferente por perfil (junior-dev más rápido, no-programador más lento)
- Casos de uso específicos por perfil (3-5 ejemplos cada uno)

## Qué evitar
- No hardcodear perfiles en el JavaScript — mantener en JSON separado
- No solapar vocabulario entre perfiles técnicos y no técnicos
- No asumir que todos los perfiles necesitan las mismas explicaciones

## Skills usados
- software-dev.md (estructura JSON)
- web-deploy.md (consideraciones de assets)

## Criterios que validaron el éxito
- 5 perfiles definidos: no-programador, junior-dev, consultor, equipo-pequeno, estudiante
- Cada perfil tiene: id, nombre, icono, descripción, vocabulario, ejemplos, casos, duración
- Archivo `profiles.json` creado en learning-platform/
- JSON válido y parseable

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: corto (~10min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-learning-platform-v2-planificacion-ordenada]] · [[2026-03-25-learning-platform-vercel-deploy]]

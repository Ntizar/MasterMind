---
fecha: 2026-03-25
tarea: sandbox-integrado-semana-1
tipo: software
complejidad: media
clusters: [sistema, web]
proyecto: learning-platform
patron: interactive-simulation-pattern
---

# FASE 3 Semana 1 — Sandbox Integrado Completado

## Decisión clave
Crear sandbox.html + sandbox.js que simula OpenCode con respuestas predefinidas para 6 tipos de tareas comunes. Los usuarios pueden probar el sistema sin instalar nada.

## Patrón reutilizable
**Nombre:** interactive-simulation-pattern
**Descripción:** Para plataformas educativas: simular herramienta real con (1) interfaz idéntica (chat input/output), (2) respuestas predefinidas por keywords, (3) delays para simular "thinking", (4) animación de agentes trabajando. Permite práctica sin riesgos.

## Qué funcionó
- **sandbox.html**: Chat interface con glass effects, avatar emojis, typing indicator
- **sandbox.js**: 6 tipos de respuesta (sop, csv, landing, onboarding, debug, articulo) + default
- **Keyword detection**: Detecta tipo de tarea por palabras clave en el input
- **Agent flow animation**: Muestra flujo de agentes con delays realistas (2.5-4s)
- **Example tasks**: 4 ejemplos clickeables para usuarios que no saben qué escribir
- **Personalización**: Reemplaza {{NAME}} con nombre del usuario desde localStorage

## Qué evitar
- No intentar simular todo — solo 6-8 tipos de tareas comunes
- No hacer respuestas instantáneas — delays dan sensación de proceso real
- No olvidar responsive — sandbox funciona en móvil también

## Skills usados
- software-dev.md (JavaScript chat logic, keyword matching)
- dashboard-dev.md (UX de simulación)

## Criterios que validaron el éxito
- sandbox.html creado con chat interface glass-style
- sandbox.js con 6 respuestas predefinidas + default
- Botón "🧪 Sandbox" en navbar de platform principal
- typing indicator animado (3 dots bouncing)
- agent-flow animation con delays escalonados
- Example tasks clickeables (4 ejemplos)

## Contexto de la tarea
- Flujo ejecutado: orchestrator → implementer → archiver
- Reintentos necesarios: ninguno
- Tiempo estimado: medio (~20min)

## Conexiones
**Clusters:** #sistema · #web
**Proyecto:** [[learning-platform]]
**Aprendizajes relacionados:** [[2026-03-25-fase-3-roadmap-creado]]

---

## 📊 Sandbox Stats

| Elemento | Cantidad |
|----------|----------|
| Tipos de respuesta | 6 + 1 default |
| Ejemplos rápidos | 4 |
| Animaciones | 3 (messageSlide, agentFadeIn, typingBounce) |
| Delays realistas | 2.5-4s |
| Líneas código | ~350 (HTML + JS) |

**Próximo:** Semana 2 — Mermaid.js diagrams animados

---
fecha: 2026-03-26
tarea: migracion-v3-multi-agente-simplificacion
tipo: conocimiento
complejidad: alta
clusters: [sistema]
proyecto: ninguno
patron: layer-separation-no-duplication
decay: permanente
---

# Migración v3: multi-agente real + simplificación de capas

## Decisión clave
Un sistema multi-agente necesita dos capas (documental y ejecutable) pero cada capa debe tener solo lo que le toca — duplicar contenido entre capas crea complejidad que mata el sistema.

## Patrón reutilizable
**Nombre:** layer-separation-no-duplication
**Descripción:** Cuando un sistema tiene una capa visual/documental (Obsidian) y una capa ejecutable (OpenCode), separar responsabilidades: la capa documental tiene definiciones completas con contexto rico y conexiones; la capa ejecutable tiene solo config + instrucciones operativas mínimas + referencia a la documental. Nunca duplicar misión, filosofía ni formatos de output en ambas capas.

## Qué funcionó
- Reducir .opencode/agents/ de 718 líneas totales a 414 (-42%) sin perder funcionalidad
- Cada subagente .opencode/ dice "Lee agents/XX-nombre.md para detalle completo" en vez de repetir todo
- Cada agente Obsidian tiene sección "Ejecutable OpenCode" con la ruta al .opencode/
- El classifier se integró en el orchestrator porque los subagentes de OpenCode no reciben contexto de conversación
- verify-system.bat reemplaza sync-agents.bat: no hay nada que sincronizar si cada capa tiene contenido diferente

## Qué evitar
- Duplicar contenido operativo (formatos de output, reglas) en ambas capas — el subagente lo lee de su .opencode/, no necesita que el Obsidian también lo tenga
- Crear scripts de "sync" entre capas — si necesitas sync, es que tienes duplicación
- Hacer subagentes demasiado cortos (< 25 líneas) — necesitan suficiente instrucción para trabajar autónomamente sin que el orchestrator les explique todo cada vez

## Skills usados
- ninguno

## Criterios que validaron el éxito
- Cero duplicación de contenido entre agents/ y .opencode/agents/
- Cada archivo tiene solo lo que le toca (verificable leyéndolos en paralelo)
- El mapa de Obsidian sigue completo y navegable con wikilinks
- Los .opencode/ tienen instrucciones operativas suficientes para que cada subagente trabaje autónomamente

## Contexto de la tarea
- Flujo ejecutado: orchestrator directo (sin ciclo formal — tarea de mantenimiento del sistema)
- Modelos usados: claude-opus-4.6 para todo
- Reintentos necesarios: ninguno
- Tiempo estimado: medio

## Conexiones
**Clusters:** #sistema
**Aprendizajes relacionados:** [[2026-03-24-sistema-v2-index-inteligente]] · [[2026-03-25-leccion-trabajar-ordenado-por-partes]]

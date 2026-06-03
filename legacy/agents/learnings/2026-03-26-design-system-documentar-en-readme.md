---
fecha: 2026-03-26
tarea: design-system-documentar-en-readme
tipo: conocimiento
clusters:
  - "#web"
  - "#sistema"
proyecto: "[[learning-platform]]"
patron: design-system-visibility-in-repo
decay: lento
---

# Documentar el Design System en el README del repo

## Contexto
El design system Liquid Glass (1,379 lineas CSS) existia como archivo pero no estaba explicado en ningun README. El usuario pidio que se incluyera porque es parte fundamental del ecosistema.

## Problema
Un design system sin documentacion visible en el README es invisible para:
- Contributors potenciales que no saben que existe
- Usuarios que quieren reutilizarlo
- SEO y discoveribilidad del proyecto

## Patron: design-system-visibility-in-repo
Cuando un proyecto tiene un design system propio:
1. **Seccion dedicada en el README** con: paleta, efecto signature, componentes, ejemplo de uso
2. **Snippet de codigo** mostrando como aplicar el estilo principal
3. **Link a demo** (`design-system/demo.html`)
4. **Banner/assets** del repo generados desde el propio design system para coherencia visual
5. Incluirlo en el roadmap como feature completada

## Senal de relevancia
Crear o actualizar documentacion de cualquier proyecto con design system propio.

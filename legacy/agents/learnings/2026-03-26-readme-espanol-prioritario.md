---
fecha: 2026-03-26
tarea: readme-espanol-prioritario
tipo: operaciones
clusters:
  - "#sistema"
  - "#github"
proyecto: "[[learning-platform]]"
patron: readme-native-language-first
decay: permanente
---

# README en idioma nativo como principal

## Contexto
Al crear el repo de ntizar-mastermind se puso el README.md en ingles y el espanol como README_ES.md (secundario). El usuario corrigio: el espanol debe ser el README.md principal y el ingles el README_EN.md.

## Problema
Por defecto se asume ingles como idioma principal del README. Esto es un sesgo del ecosistema tech, pero si el proyecto esta escrito en espanol, los agentes definen sus misiones en espanol, y el creador habla espanol, el README principal debe ser en espanol.

## Patron: readme-native-language-first
- README.md → idioma nativo del proyecto/creador
- README_EN.md → traduccion al ingles
- Los links entre ambos se cruzan (`English` / `Espanol (principal)`)
- El repo description en GitHub puede ser bilingue

## Senal de relevancia
Crear cualquier repositorio o documentacion publica para el sistema Ntizar.

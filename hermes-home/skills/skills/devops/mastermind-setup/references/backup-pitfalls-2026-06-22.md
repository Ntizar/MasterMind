# Backup Pitfalls y Lecciones (2026-06-22)

## Backup Pitfall: Doble Nesting con cp

Problema: cp -r source/ dest/ cuando dest/ ya existe crea ruta duplicada.

Soluciones:
1. git reset --hard commit-limpio, borrar hermes-backup/, copiar desde cero
2. cp -rT source/ dest/ (la T evita nesting extra)
3. cp -r source/* dest/ (copia contenido, no directorio)

En git: los commits con doble nesting generan historial sucio.
Solucion: git reset --hard commit-limpio + force push.

## Backup Pitfall: Commits Duplicados

Los intentos fallidos generan commits duplicados en el historial.
Solucion: reset --hard al commit limpio, copiar desde cero, force push.

## Backup Pitfall: .hub/quarantine/

Contiene skills en cuarentena que NO deben copiarse al repo.
Excluir del conteo de SKILL.md.

## Backup Pitfall: skill-learning.log en .gitignore

Necesita git add -f para forzarlo.

## Comparacion de Skills

Si el repo tiene MAS skills que Hermes, no hay nada que copiar.
El repo puede estar mas actualizado.
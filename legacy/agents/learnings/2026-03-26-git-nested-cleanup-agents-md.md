---
fecha: 2026-03-26
tarea: git-nested-cleanup-agents-md
tipo: operaciones
clusters:
  - "#github"
  - "#sistema"
patron: clean-nested-git-before-repo-init
decay: normal
---

# Limpiar .git anidados y artefactos Windows antes de crear repo

## Contexto
Al copiar la carpeta AGENTS.MD del vault al repo, se incluyo un `.git/` anidado (era un subrepo anterior) y archivos `nul` (artefacto de Windows cuando se redirige output a `nul`). Esto causa problemas al inicializar el repo padre.

## Problema
- `.git/` anidados crean submodulos implicitos o conflictos
- Archivos `nul` son artefactos de Windows que no deberian entrar al repo
- Carpetas con nombres case-insensitive (AGENTS.MD vs AGENTS.md) causan problemas en Windows

## Patron: clean-nested-git-before-repo-init
Antes de hacer `git init` en una carpeta nueva:
1. `find . -name ".git" -type d` — eliminar todos los `.git/` anidados
2. `find . -name "nul" -type f -delete` — eliminar artefactos Windows
3. Verificar que no hay carpetas con nombres que solo difieren en case (Windows es case-insensitive)
4. Si hay carpeta y archivo con mismo nombre (ej: `AGENTS.MD/` carpeta + quieres `AGENTS.md` archivo), renombrar via temp: `mv folder/file temp && rm -rf folder && mv temp file`

## Senal de relevancia
Crear repositorio nuevo a partir de archivos existentes de un vault Obsidian o proyecto.

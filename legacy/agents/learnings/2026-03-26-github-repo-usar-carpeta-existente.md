---
fecha: 2026-03-26
tarea: github-repo-usar-carpeta-existente
tipo: operaciones
clusters:
  - "#github"
  - "#sistema"
proyecto: "[[learning-platform]]"
patron: use-existing-project-structure
decay: lento
---

# Usar carpeta Github existente para repos

## Contexto
Al crear el repositorio de ntizar-mastermind, se creo inicialmente en una ubicacion nueva (`C:\Ntizar_Obsidian\ntizar-brain`) en vez de usar la carpeta `Github/` que ya existia dentro del vault con los demas repos (MonteCarloInversion, nap-dashboard, Caedelcielo, medvisit, SistemaElectricoFuturo).

## Problema
Crear repos en ubicaciones ad-hoc rompe la organizacion establecida. Luego hay que borrar, mover, y se pierde tiempo.

## Patron: use-existing-project-structure
**Antes de crear cualquier directorio nuevo, verificar si ya existe una estructura organizativa para ese tipo de contenido.**

Regla concreta:
- Repos de GitHub → `Ntizar_Brain/Github/`
- Siempre hacer `ls` de la carpeta padre antes de crear

## Senal de relevancia
Crear un nuevo repositorio o proyecto que necesita carpeta local.

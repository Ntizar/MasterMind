---
fecha: 2026-03-26
tarea: svg-banner-desde-design-system
tipo: software
clusters:
  - "#web"
  - "#sistema"
proyecto: "[[learning-platform]]"
patron: svg-banner-from-css-variables
decay: normal
---

# Banner SVG generado desde variables del Design System

## Contexto
Para el README del repo se necesitaba un banner. En vez de usar una imagen externa o un PNG generico, se genero un SVG que usa los colores exactos del design system Liquid Glass (azul #3b82f6, naranja #f97316, fondo #0a0f1e).

## Problema
Un archivo PNG o JPG como banner tiene problemas:
- No escala limpiamente en dark/light mode
- No se puede editar sin herramienta de diseno
- GitHub no renderiza archivos binarios inline sin subir al repo

## Patron: svg-banner-from-css-variables
Generar banners como SVG puro que:
1. Usa los mismos colores que las CSS custom properties del design system
2. Incluye elementos visuales representativos (pipeline de agentes, nodos, conexiones)
3. Es editable como texto — cualquier contributor puede ajustarlo
4. GitHub renderiza SVGs nativamente en READMEs
5. Se escala a cualquier resolucion sin pixelarse

## Senal de relevancia
Crear assets visuales para repos, landing pages, o documentacion del ecosistema Ntizar.

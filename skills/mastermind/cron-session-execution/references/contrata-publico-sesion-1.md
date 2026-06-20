# ContrataPúblico — Sesión 1 (2026-06-16)

## Contexto
Proyecto: Herramienta web para entender y cumplir la Ley 9/2017 de Contratos del Sector Público.
Stack: HTML vanilla + Aurora Design System + Plotly.js + localStorage. Zero backend.
Deploy: GitHub Pages.

## Ejecución
- Script: `scripts/sesion-01-parse-ley.py`
- Descargó HTML del BOE (1.7 MB)
- Parseó 347 artículos con estructura completa
- Outputs:
  - `js/ley-data.js` (731 KB) — estructura navegable + funciones JS
  - `data/ley-texto.json` (1.1 MB) — texto completo por artículo
- Commit: `342e494` — "Sesión 1: Parser de la Ley 9/2017 — estructura + texto completo"
- Push: ✅ `main -> main`

## Estado
Sesiones 0-3 completadas. Sesión 4 pendiente.

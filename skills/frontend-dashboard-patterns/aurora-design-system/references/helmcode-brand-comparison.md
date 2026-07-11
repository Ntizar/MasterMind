# Helmcode Brand Kit vs Aurora — Gaps y Aprendizajes

**Fecha:** 2026-07-09
**Fuente:** https://helmcode.com/es/brand
**Estado:** ✅ Todos los gaps resueltos en commit `4bc05f9` (2026-07-09)

## Contexto

Comparativa entre el brand kit de Helmcode (empresa de IA empresarial) y Aurora Ntizar v5.2. Helmcode es un brand kit (identidad de marca documentada en 1 página). Aurora es un design system CSS modular (11 packs, 119 componentes, 243 KB).

## Veredicto general

Aurora gana como **proyecto de ingeniería** (reusabilidad, profundidad técnica, accesibilidad, CI, documentación, multi-axis theming). Helmcode ganaba como **identidad de marca** (voz, posicionamiento, kit de prensa, reglas de acento disciplinadas) — **ahora Aurora tiene ambas cosas**.

## Gaps de Aurora vs Helmcode — RESUELTOS

### 1. Voz de marca y posicionamiento ✅

**Helmcode tenía:** Posicionamiento claro, boilerplate copiable, sección "lo que NO es", 4 pilares de valor.

**Aurora ahora tiene:** `BRAND.md` con posicionamiento ("CSS-only, sin build, sin dependencias, namespaced"), boilerplate copiar-pegar, 5 keywords de marca, sección "Aurora NO es", tono do/don't.

### 2. Kit de prensa / descargas de marca ✅

**Helmcode tenía:** Logos SVG + PNG (6 variantes + 3 símbolos), brandbook.md descargable, zip completo.

**Aurora ahora tiene:** 11 SVGs (5 símbolos + 5 logos + favicon.svg) + 10 PNGs (favicons 32/180/512px + símbolos 200px + logos 340px) + favicon.ico. `brandbook.md` descargable. Página `brand.html` con sección de descargas.

### 3. Reglas de acento explícitas (presupuesto de color) ✅

**Helmcode tenía:** Máx 4-5 momentos de acento por página, reglas NUNCA, texto de acento como token separado.

**Aurora ahora tiene:** `accent_budget` en `DESIGN.md` — máx 5 momentos saturados por página (scope page), reglas SÍ/NUNCA, dual rule (azul+naranja no se mezclan en misma sección). También en `AGENTS.md` como contrato para IAs.

### 4. Convención de antetítulo ✅

**Helmcode usaba:** `//` como antetítulo antes de secciones.

**Aurora ahora tiene:** `.nz-eyebrow` en `ntizar.css` con `›` (U+203A) como convención de marca. Font mono, uppercase, letter-spacing 0.12em. Variantes `--accent` y `--muted`.

### 5. Esquinas rectas como personalidad ✅

**Helmcode declaraba:** Esquinas rectas como personalidad técnica de la marca.

**Aurora ya tenía:** `data-nz-shape` (default|sharp|rounded|brutalist). Ahora formalizado en `AGENTS.md` con reglas de forma y anti-patterns.

## Lo que Aurora ya hace mejor que Helmcode

- **Ingeniería:** 7.119 líneas CSS modular vs 1 página HTML
- **Reusabilidad:** 6+ proyectos reales (GTFSSpain, GBFSSpain, DataHubEspana, etc.)
- **Multi-axis theming:** 6 skins × 4 shapes × 3 densities × 2 color systems
- **OKLCH:** Escalas 50-900 completas, no solo 2 tokens
- **Liquid glass:** 4 capas reales (specular + chromatic edge + dual inset)
- **Three.js:** Partículas, wireframes, shader custom, parallax — ahora también en brand.html
- **Accesibilidad:** WCAG AA/AAA, forced-colors, reduced-motion, skin contrast
- **CI:** Design lint automático en PRs
- **Mobile-first:** Obligatorio, touch targets 44px
- **Documentación:** INDEX.md, LLM.md, AGENTS.md, DESIGN.md, BRAND.md, brandbook.md, components.json, gallery.html, 5 examples
- **Namespacing:** `.nz` no colisiona con otros frameworks
- **Brand page viva:** `brand.html` con Three.js (A extruded 3D + partículas + anillos orbitales) — Helmcode es estática

## Archivos creados en el kit de marca

| Archivo | Bytes | Contenido |
|---|---|---|
| `BRAND.md` | 4.038 | Voz de marca, posicionamiento, boilerplate, keywords |
| `brandbook.md` | 4.803 | Guía descargable: símbolo, variantes, reglas, paleta |
| `AGENTS.md` | 3.206 | Contrato para IAs: 5 reglas duras, acento, anti-patterns |
| `brand.html` | 39.347 | Página de marca viva con Three.js |
| `DESIGN.md` (patch) | +accent_budget | Reglas de acento explícitas |
| `ntizar.css` (patch) | +`.nz-eyebrow` | Convención de antetítulo `›` |
| `assets/simbolo/` | 8 archivos | 5 SVG + 3 PNG del símbolo "A" |
| `assets/logo/` | 9 archivos | 5 SVG + 4 PNG del logotipo completo |
| `assets/favicon/` | 6 archivos | favicon.svg/ico + PNG 32/180/512 |

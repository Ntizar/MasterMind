---
name: aurora-llm-optimization
description: "Procedimiento para optimizar cualquier design system CSS para que sea infalible con LLMs: LLM.md decision guide, components.json machine-readable, examples/, validation scripts, updated AGENTS.md/INDEX.md/README."
version: "1.0.0"
author: Mastermind
tags: [aurora, llm, design-system, css, documentation, machine-readable]
---

# Aurora LLM Optimization

Procedimiento para optimizar un design system CSS (específicamente Ntizar Aurora) para que sea **infalible con LLMs**.

## Cuándo usar

- Un design system CSS necesita ser consumido por agentes IA
- Quieres que un LLM use tu sistema sin inventar clases, hardcodear valores o gastar tokens
- Estás creando un nuevo design system y quieres que sea LLM-ready desde el inicio

## Estructura de archivos (4 piezas)

### 1. `LLM.md` — Guía de decisión (~2-3 KB, ~500 tokens)

El archivo más importante. Debe cubrir el 95% de casos con "necesito X → packs Y → clases Z".

**Estructura obligatoria:**
```
# [Nombre] — LLM Decision Guide

## Paso 1: Carga CDN mínimo
[snippet HTML mínimo con CDN + class="nz"]

## Paso 2: Elige packs según lo que necesitas
[tabla: "¿Qué construyes?" → Packs → Clases clave]

## Paso 3: Heurística rápida "Necesito X → clases Y"
[por categoría: layout, componentes, data, charts, maps, UI, forms, patterns, motion]

## Paso 4: Personalizar marca (solo estos tokens)
[snippet CSS con tokens sobrescritos]

## Paso 5: Dark mode
[snippet con data-nz-theme="dark"]

## Anti-patrones LLM (NUNCA hagas esto)
[5-10 errores típicos con ❌/✅]

## Tokens de color clave
[tabla: token → valor → uso]

## Quick reference: ¿qué pack necesito?
[lista rápida de decisión]
```

**Reglas de LLM.md:**
- Máximo 2-3 KB (~500 tokens de contexto)
- Tablas en formato `| ¿Qué construyes? | Packs | Clases |`
- Anti-patrones con ❌ y ✅ visuales
- Siempre termina con "docs hermanas" (referencia a AGENTS.md, INDEX.md, examples/)

### 2. `components.json` — Spec machine-readable

JSON con todos los componentes, modificadores, parts, categorías y packs.

**Estructura mínima:**
```json
{
  "name": "Nombre Design System",
  "version": "x.y.z",
  "type": "css-only design system",
  "scope": ".nz (opt-in)",
  "cdn": "https://cdn.jsdelivr.net/gh/...",
  "architecture": {
    "layers": ["tokens", "base", "objects", "components", "utilities"],
    "naming": {
      "component": ".nz-thing",
      "modifier": ".nz-thing--mod",
      "part": ".nz-thing__part",
      "state": ".is-state",
      "utility": ".u-nz-*",
      "token": "--nz-*"
    }
  },
  "packs": {
    "core": {"file": "ntizar.css", "description": "...", "mandatory": true},
    "themes": {"file": "ntizar.themes.css", "description": "...", "mandatory": false}
  },
  "components": {
    "btn": {
      "base": ".nz-btn",
      "modifiers": ["primary", "accent", "ghost", "danger", "glass"],
      "parts": [],
      "selector_count": 41,
      "packs": ["core"],
      "category": "button"
    }
  },
  "by_category": {
    "button": [{"name": "btn", "base": ".nz-btn", "modifiers": [...]}],
    "input": [...],
    "layout": [...]
  }
}
```

**Generación automática:**
```bash
# Script en scripts/parse-components.js
# Parsea todos los .css, extrae selectores .nz-*
# Agrupa por base name (antes de __ o --)
# Asigna categoría y pack
# Escribe components.json
```

### 3. `examples/` — Snippets HTML completos

Mínimo 5 ejemplos que cubran los casos de uso más comunes:

| Archivo | Qué muestra | Packs usados |
|---|---|---|
| `login.html` | Formulario login (field, input, button) | core + forms + patterns |
| `dashboard.html` | App-shell, KPIs, chart, tabla | core + data + charts + ui + patterns |
| `landing.html` | Hero, features, pricing, footer | core + patterns + viz + motion |
| `ui-components.html` | Tabs, dropdown, modal, toast | core + ui |
| `forms.html` | Switch, segmented, OTP, file drop, stepper | core + forms |

**Reglas de los ejemplos:**
- Cada uno es HTML completo y funcional (DOCTYPE, head, body)
- CDN público en `<head>`
- Solo los packs necesarios
- Sin JS innecesario (solo lo mínimo para interactividad)
- Nombre descriptivo: `login.html`, no `ejemplo1.html`

### 4. `scripts/` — Validación y estadísticas

**`scripts/validate-llm.js`** — Valida consistencia:
- LLM.md existe y tiene contenido (>1KB)
- components.json es JSON válido con todos los packs
- Los ejemplos existen
- INDEX.md referencia a LLM.md
- AGENTS.md referencia a LLM.md
- package.json incluye nuevos archivos en `files`

**`scripts/component-stats.js`** — Estadísticas:
- Total de componentes
- Por categoría con barra visual
- Top 10 por selector count
- Resumen de packs
- Tamaño de archivos LLM

## Pasos de implementación

1. **Crear `LLM.md`** con la estructura de 5 pasos + anti-patrones
2. **Generar `components.json`** parseando todos los CSS (script en `scripts/parse-components.js`)
3. **Crear `examples/`** con mínimo 5 HTML completos
4. **Crear `scripts/validate-llm.js`** y `scripts/component-stats.js`
5. **Actualizar `AGENTS.md`** con decision tree: LLM.md → INDEX.md → DESIGN.md → examples/
6. **Actualizar `INDEX.md`** con referencia a LLM.md y components.json
7. **Actualizar `README.md`** con documentación de nuevos archivos
8. **Actualizar `package.json`** con nuevos archivos en `files` y scripts
9. **Ejecutar `node scripts/validate-llm.js`** para verificar consistencia
10. **Ejecutar `npm run stats`** para ver estadísticas

## Cómo se usa en la práctica

**Para un LLM que genera HTML:**
1. Lee `LLM.md` (~500 tokens) → sabe qué packs y clases usar
2. Si necesita detalles → lee `components.json` o `INDEX.md`
3. Genera HTML con clases correctas
4. NUNCA lee los CSS (~170 KB = ~50k tokens)

**Para un humano que integra Aurora:**
1. Lee `LLM.md` → decision rápida
2. Abre `examples/login.html` → copia y modifica
3. Consulta `components.json` → API completa

## Pitfalls

- **LLM.md > 5 KB** → gasta demasiados tokens de contexto. Recortar anti-patrones y tokens si es necesario.
- **components.json desactualizado** → si añades un componente CSS, regenera el JSON. El script de parsing automatiza esto.
- **Ejemplos que no funcionan** → cada ejemplo debe ser HTML funcional, no pseudocódigo.
- **No actualizar AGENTS.md** → si existe LLM.md pero AGENTS.md no lo referencia, los agentes seguirán cargando INDEX.md primero (16 KB vs 2 KB).
- **Olvidar package.json** → si los nuevos archivos no están en `files`, no se publican en npm/jsDelivr.

## Relación con otras skills

- **`liquid-glass-css`** → cubre el estilo visual de Aurora, pero NO la optimización LLM
- **`frontend-dashboard-patterns`** → cubre patrones de dashboards, pero NO la infraestructura de documentación LLM
- **`chromadb-skills-vector-search`** → usa components.json para búsqueda semántica de skills

## Versionado

- Cambios en LLM.md, components.json, examples → **PATCH** (no rompen nada)
- Cambios en estructura de componentes.json → **MINOR** (parsers externos pueden necesitar actualización)
- Cambios en naming de componentes CSS → **MAJOR** (rompe compatibilidad)

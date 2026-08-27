# [Nombre del Design System] — LLM Decision Guide

> **Este archivo es tu única referencia.** [X] KB de heurística pura. Si sigues esto al pie de la letra, **nunca fallarás**.
>
> **Regla de oro:** `Necesito X → carga packs Y → usa clases Z`. Nada más.

---

## Paso 1: Carga CDN mínimo

```html
<link rel="stylesheet" href="[CDN_URL]">
<body class="[SCOPE_CLASS]">
```

**Sin `[SCOPE_CLASS]` en el body, todo falla.** Es la regla número 1.

---

## Paso 2: Elige packs según lo que necesitas

| ¿Qué construyes? | Packs a cargar | Clases clave |
|---|---|---|
| **Cualquier cosa** | core | `[clases base]` |
| **[Caso 2]** | [packs] | [clases] |
| **[Caso 3]** | [packs] | [clases] |

**Packs opcionales (cargar solo si los usas):**
- `[pack1.css]` → [descripción]
- `[pack2.css]` → [descripción]

---

## Paso 3: Heurística rápida "Necesito X → clases Y"

### Layout
- [Elemento] → `.nz-[clase]`
- [Elemento] → `.nz-[clase]`

### Componentes
- [Componente] → `.nz-[base]` + `.nz-[base]--[mod]`
- [Componente] → `.nz-[base]` + `.nz-[base]__part`

### [Categoría]
- [Elemento] → `.nz-[clase]`

---

## Paso 4: Personalizar marca (solo estos tokens)

```css
.mi-app.[SCOPE_CLASS] {
  --nz-color-brand: #HEX;        /* tu color principal */
  --nz-color-accent: #HEX;       /* tu color secundario */
  --nz-font-sans: "Font", system-ui, sans-serif;
}
```

**Nunca hardcodees colores.** Usa siempre `var(--nz-color-brand)`.

---

## Paso 5: Dark mode

```html
<body class="[SCOPE_CLASS]" data-nz-theme="dark">
```

Para cambiar runtime: `document.body.dataset.nzTheme = 'dark'`.

---

## Anti-patrones LLM (NUNCA hagas esto)

```html
<!-- ❌ Olvidar scope class -->
<body>
  <button class="nz-btn">Click</button>  <!-- NO FUNCIONA -->
</body>

<!-- ❌ Inventar clases -->
<button class="nz-btn--super">Click</button>  <!-- NO EXISTE -->

<!-- ❌ Hardcodear valores -->
<button style="background: #2563eb; padding: 16px;">Click</button>

<!-- ❌ Escribir CSS paralelo para lo que el sistema ya tiene -->
<style> .mi-boton { ... } </style>

<!-- ✅ Correcto -->
<body class="[SCOPE_CLASS]">
  <button class="nz-btn nz-btn--primary">Click</button>
</body>
```

---

## Tokens de color clave

| Token | Valor por defecto | Uso |
|---|---|---|
| `--nz-color-brand` | `#HEX` | Color principal |
| `--nz-color-accent` | `#HEX` | Color secundario |
| `--nz-color-success` | `#HEX` | Éxito |
| `--nz-color-danger` | `#HEX` | Error |

---

## Quick reference: ¿qué pack necesito?

```
¿Botón/card/badge/alert/field/table?          → core
¿Dashboard con KPIs?                           → core + data
¿Gráficos?                                     → core + charts
¿Mapas?                                        → core + maps
¿Modals/tabs/dropdowns/toasts?                 → core + ui
¿Formularios?                                  → core + forms
¿Hero/pricing/footer?                          → core + patterns
¿Animaciones?                                  → core + motion
```

---

*Docs hermanas: `AGENTS.md` (reglas detalladas), `INDEX.md` (mapa completo de clases), `components.json` (spec machine-readable), `examples/` (snippets completos).*

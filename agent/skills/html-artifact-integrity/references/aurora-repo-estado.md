# Ntizar-Aurora — Estado verificado del repo (2026-08-28)

Verificado en vivo vía API de GitHub contra `Ntizar/Ntizar-Aurora` (rama `master`).

## Contenido real del repo

| Fichero | Existe | Nota |
|---|---|---|
| `ntizar.css` | ✅ | core, 64.6 KB |
| `ntizar.themes.css` | ✅ | 5 skins (aurora/sunset/midnight/ocean/citrus) + fix del gradiente violeta |
| `ntizar.nucleo.css` | ✅ | colores sólidos, bento, CSS-only charts (existe desde v5.1, no aparece en docs antiguas) |
| `ntizar.data.css` / `charts` / `maps` / `viz` / `motion` / `forms` / `ui` / `patterns` / `next` | ✅ | los 10 packs completos |
| `INDEX.md` | ✅ | 15.4 KB — API de clases por pack (fuente de verdad) |
| `LLM.md` | ✅ | 11.3 KB — guía de decisión rápida |
| `AGENTS.md`, `BRAND.md`, `DESIGN.md` | ✅ | reglas, tokens |
| `components.json` | ✅ | spec machine-readable (119 componentes) |
| `gallery.html` | ✅ | 190 KB, referencia visual |
| `CHEATSHEET.md` | ❌ **NO existe** | 404 verificado — docs antiguas que lo citen están obsoletas |
| `scripts/` y `examples/` | ✅ | directorios presentes |

## Estructuras HTML verificadas en el CSS (patrón real de uso)

```html
<!-- KPI (pack data) -->
<div class="nz-kpi nz-kpi--accent">
  <span class="nz-kpi__label">Etiqueta</span>
  <span class="nz-kpi__value">Valor</span>
  <span class="nz-kpi__delta">Delta</span>
</div>

<!-- Grid de stats -->
<div class="nz-stat-grid--3"> ...nz-kpi... </div>

<!-- Barra de progreso (hijo directo __bar, width inline) -->
<div class="nz-progress"><div class="nz-progress__bar" style="width:72%"></div></div>

<!-- Meter circular (CSS var, sin hijos) -->
<div class="nz-meter" style="--nz-meter-value:72; --nz-meter-color:var(--nz-color-brand)"></div>
```

## Tokens clave para personalización

```css
.nz {
  --nz-color-brand: #2563eb;
  --nz-color-accent: #f97316;
  --nz-gradient-aurora: linear-gradient(135deg, #2563eb 0%, #f97316 100%);
}
```

## Regla operativa

Antes de generar HTML con Aurora: descargar `INDEX.md` y `LLM.md` desde raw.githubusercontent (con User-Agent header; sin él puede fallar) y usar SOLO clases de ahí. La CDN es `https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@master/<pack>.css`. El skill `aurora-design-system` (user-owned) contiene referencias a CHEATSHEET.md y rutas `/root/workspace/` obsoletas — prevalece este fichero y el repo en vivo.
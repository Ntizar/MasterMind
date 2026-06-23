# Generación automática de components.json

## Patrón

Para mantener `components.json` sincronizado con los CSS, se usa un script Node.js que:

1. Parsea todos los archivos `.css` del design system
2. Extrae TODOS los selectores `.nz-*` usando regex
3. Agrupa por nombre base (antes de `__` o `--`)
4. Asigna categoría y pack a cada componente
5. Escribe `components.json` con estructura machine-readable

## Script de parsing (esqueleto)

```javascript
const fs = require('fs');
const path = require('path');
const re = require('path').resolve;

const ROOT = process.cwd();
const cssFiles = {
  core: 'ntizar.css',
  ui: 'ntizar.ui.css',
  patterns: 'ntizar.patterns.css',
  forms: 'ntizar.forms.css',
  data: 'ntizar.data.css',
  charts: 'ntizar.charts.css',
  maps: 'ntizar.maps.css',
  viz: 'ntizar.viz.css',
  motion: 'ntizar.motion.css',
  next: 'ntizar.next.css',
  themes: 'ntizar.themes.css',
};

const allSelectors = {};

for (const [pack, file] of Object.entries(cssFiles)) {
  const content = fs.readFileSync(path.join(ROOT, file), 'utf8');
  const selectors = new Set();
  for (const m of content.matchAll(/\.nz-([a-z][a-z0-9-]*)/g)) {
    selectors.add(m[0]);
  }
  allSelectors[pack] = [...selectors];
}

// Agrupar por base name
const baseComps = {};
for (const [pack, selectors] of Object.entries(allSelectors)) {
  for (const sel of selectors) {
    const name = sel.slice(4); // remove '.nz-'
    let base;
    if (name.includes('__')) {
      base = name.split('__')[0];
    } else if (name.includes('--')) {
      base = name.split('--')[0];
    } else {
      base = name;
    }
    if (!baseComps[base]) baseComps[base] = { selectors: [], packs: [] };
    if (!baseComps[base].selectors.includes(sel)) baseComps[base].selectors.push(sel);
    if (!baseComps[base].packs.includes(pack)) baseComps[base].packs.push(pack);
  }
}

// Construir output
const components = {};
for (const [base, info] of Object.entries(baseComps)) {
  if (base.startsWith('u-nz')) continue;
  
  const mods = info.selectors
    .filter(s => s.includes('--'))
    .map(s => s.split('--').pop())
    .filter(Boolean);
  const parts = info.selectors
    .filter(s => s.includes('__'))
    .map(s => s.split('__').slice(1).join('__'))
    .filter(Boolean);
    
  components[base] = {
    base: `.nz-${base}`,
    modifiers: [...new Set(mods)].slice(0, 30),
    parts: [...new Set(parts)].slice(0, 20),
    selector_count: info.selectors.length,
    packs: info.packs,
  };
}

const spec = {
  name: 'Nombre Design System',
  version: 'x.y.z',
  type: 'css-only design system',
  scope: '.nz (opt-in)',
  cdn: 'https://cdn.jsdelivr.net/gh/...',
  architecture: { /* ... */ },
  packs: { /* ... */ },
  components,
};

fs.writeFileSync('components.json', JSON.stringify(spec, null, 2));
```

## Categorización

Las categorías se asignan basándose en el pack y el nombre del componente:

| Pack | Categoría por defecto |
|---|---|
| core | component |
| ui | interactive / overlay / navigation |
| patterns | pattern |
| forms | form / input |
| data | data-display |
| charts | chart / data-display |
| maps | map |
| viz | visual |
| motion | animation |
| next | experimental |

Se puede sobreescribir con un mapa de categoría explícito.

## Frecuencia de actualización

- **Cada vez que se añade un componente CSS** → regenerar JSON
- **Cada PR** → el CI puede correr el script como validación
- **Manual** → `node scripts/generate-components.js`

## Validación

El script `scripts/validate-llm.js` verifica que:
- components.json es JSON válido
- Tiene todos los packs esperados
- Tiene >50 componentes
- Está referenciado en package.json

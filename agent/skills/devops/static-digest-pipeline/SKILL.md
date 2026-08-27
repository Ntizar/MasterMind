---
name: static-digest-pipeline
description: "Pipeline de digest estático: fetch API externa → normalización → scoring heurístico → JSON → HTML → GitHub Pages. Patrón para repos tipo datos-gob-watch."
version: "1.0.0"
category: data
tags: [devops, pipeline, digest, static]

---

# Static Digest Pipeline

## Cuándo usar

- Generas un digest periódico (semanal, diario) de datos públicos de una API
- Quieres publicar datos procesados como sitio estático en GitHub Pages
- Necesitas scoring heurístico para priorizar datasets o recursos
- El pipeline debe ejecutarse automáticamente sin intervención humana

## Cuándo NO usar

- Los datos necesitan actualizarse en tiempo real → un sitio estático no se actualiza al instante
- La API externa no tiene datos estructurados → no hay nada que normalizar ni hacer scoring
- Necesitas interactividad (filtros, búsqueda) → el HTML estático es solo lectura

## Metadata

> **Repo:** https://github.com/Ntizar/datos-gob-watch
> **Stack:** Node.js, HTML plano, CSS, GitHub Actions
> **URL:** https://ntizar.github.io/datos-gob-watch/

## Qué es

Pipeline que consulta una API externa (datos.gob.es), normaliza datos, aplica scoring heurístico, y genera un sitio estático publicado en GitHub Pages. Se ejecuta semanalmente vía GitHub Actions.

## Flujo Principal

```
API externa (datos.gob.es)
  → scripts/fetch-weekly.mjs (fetch + normalize + score)
  → data/latest.json (payload generado)
  → index.html (render estático con datos embebidos)
  → GitHub Pages (deploy automático)
```

## Patrón: Normalización de Datos API

```javascript
// 1. Listas → valores únicos
function normalizeList(value) {
  if (Array.isArray(value)) return value;
  if (value == null) return [];
  return [value];
}

// 2. Labels multilingües → preferir español
function pickLabel(value) {
  if (Array.isArray(value)) {
    const spanish = value.find(e => e._lang === "es" && e._value);
    if (spanish) return spanish.__value;
    const first = value.find(e => e._value);
    if (first) return first._value;
  }
  return value?._value ?? value ?? "";
}

// 3. URI tail → label legible
function formatLabelFromTail(value) {
  const tail = uriTail(value);
  return tail.replace(/[-_]/g, " ");
}
```

## Patrón: Scoring Heurístico

```javascript
function computeScore({ formats, themes, distributions, publisher, spatial, keywords }) {
  let score = 0;
  for (const format of formats) {
    if (preferredFormats.has(format)) score += 10; // CSV, JSON, GEOJSON...
  }
  for (const theme of themes) {
    if (preferredThemes.some(t => theme.toLowerCase().includes(t))) score += 12;
  }
  if (distributions.length >= 3) score += 8;
  if (publisher !== "Sin dato") score += 4;
  if (spatial !== "Sin dato") score += 3;
  if (keywords.length >= 3) score += 4;
  return Math.min(score, 100);
}
```

## Patrón: Paginación API

```javascript
async function fetchWeeklyDatasets() {
  const datasets = [];
  for (let page = 0; page < 5; page += 1) {
    const payload = await fetchPage(page, startApi, endApi);
    const items = payload?.result?.items ?? [];
    if (items.length === 0) break;
    datasets.push(...items.map(normalizeDataset));
    if (!payload?.result?.next) break;
  }
  return datasets
    .sort((a, b) => b.score - a.score)
    .slice(0, MAX_ITEMS);
}
```

## Patrón: GitHub Actions para Deploy Estático

```yaml
# .github/workflows/weekly.yml
name: Weekly Digest
on:
  schedule:
    - cron: '0 8 * * 1'  # Lunes 08:00 UTC
  workflow_dispatch: {}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

## Archivos del patrón

| Archivo | Responsabilidad |
|---------|----------------|
| `scripts/fetch-weekly.mjs` | Fetch + normalización + scoring |
| `data/latest.json` | Payload generado (input del HTML) |
| `index.html` | Frontend estático con datos embebidos |
| `ntizar.css` | Estilos Ntizar (copiado del design system) |
| `.github/workflows/weekly.yml` | Automatización semanal |

## Variantes del patrón

- **Diario:** cambiar cron a `0 8 * * *`
- **Mensual:** cambiar cron a `0 8 1 * *`
- **Trigger on push:** añadir `push:` al workflow
- **Multi-fuente:** extender fetch-weekly para múltiples APIs

## Caso de Estudio: datos-gob-watch

El proyecto `datos-gob-watch` (https://ntizar.github.io/datos-gob-watch/) es la implementación de referencia de este patrón:

- **API:** datos.gob.es (Open Data español)
- **Frecuencia:** semanal (GitHub Actions cron)
- **Heurísticas de ranking:** formatos reutilizables (JSON, CSV, GEOJSON), temáticas con potencial, múltiples distribuciones
- **Stack:** Node.js + HTML plano + ntizar.css + GitHub Pages
- **API endpoints:** `https://datos.gob.es/apidata/catalog/dataset/modified/` con ventana semanal

Reutilizar el patrón para cualquier monitorización de APIs de datos abiertos.

## Pitfalls

- **Rate limiting:** algunas APIs externas tienen límites. Implementar retry con backoff.
- **API changes:** la estructura de respuesta puede cambiar. Validar con `payload?.result?.items ?? []`.
- **CSS sync:** ntizar.css se copia manualmente. Usar symlink o git subtree para mantener sincronizado.
- **JSON embebido:** el index.html lee data/latest.json. Si el JSON es muy grande, considerar lazy loading.

---
name: static-digest-pipeline
description: Pipeline de digest estatico: fetch API externa, normalizacion, ranking, publicacion GitHub Pages con GitHub Actions. Derivado de datos-gob-watch.
version: "1.0.0"
tags: [pipeline, datos-estaticos, github-pages, digest, scraping]
---

# Static Digest Pipeline - Patron de Digest Semanal

## Descripcion

Patron para construir digests estaticos a partir de APIs externas: fetch, normalizacion, ranking con heuristicas, generacion de HTML estatico y deploy en GitHub Pages.

## Origen

Derivado del repositorio [datos-gob-watch](https://github.com/Ntizar/datos-gob-watch).

## Flujo Principal

```
API Externa (datos.gob.es)
  -> scripts/fetch-weekly.mjs (fetch + normalizacion + ranking)
  -> data/latest.json (payload generado)
  -> index.html (frontend estatico con estilo Ntizar)
  -> GitHub Pages (deploy automatico)
```

## Estructura del Repo

```
repo/
  scripts/fetch-weekly.mjs  # Fetch + normalizacion + ranking
  data/latest.json          # Payload generado del digest
  index.html                # Frontend estatico
  ntizar.css                # Capa visual
  .github/workflows/weekly.yml  # Refresh semanal + deploy
```

## Heuristicas de Ranking

Suben mas en ranking los datasets que traen:
- Formatos reutilizables: JSON, CSV, XML, GEOJSON, XLSX
- Tematicas con potencial de producto
- Varias distribuciones
- Metadatos razonablemente completos

## GitHub Actions Workflow

```yaml
name: Weekly Digest
on:
  schedule:
    - cron: '0 9 * * 1'  # Lunes 09:00 UTC
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm run build
      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

## Implementacion en Hermes

Para replicar este patron:

1. Crear script Node.js para fetch + normalizacion
2. Generar JSON intermedio con datos normalizados
3. Template HTML con los datos inyectados
4. GitHub Actions para ejecucion periodica
5. Deploy a GitHub Pages con `peaceiris/actions-gh-pages`

## Pitfalls

- **CORS**: algunas APIs no tienen CORS habilitado, usar proxy o fetch desde servidor
- **Rate limiting**: respetar limites de la API externa, usar cache
- **Datos sensibles**: nunca hardcodear API keys en el codigo cliente
- **Deprecacion de API**: monitorizar cambios en endpoints externos

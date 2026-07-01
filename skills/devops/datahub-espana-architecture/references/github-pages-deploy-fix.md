# GitHub Pages Deployment — Fix para `actions/configure-pages@v5`

## Problema
El workflow de GitHub Pages falla en el paso "Setup Pages" con:
```
Get Pages site failed. Please verify that the repository has Pages enabled
and configured to build using GitHub Actions
Error: Not Found - https://docs.github.com/rest/pages/pages#get-a-apiname-pages-site
```

## Causa
`actions/configure-pages@v5` con `enablement: false` (default) no puede encontrar el sitio Pages aunque esté habilitado.

## Solución
Añadir `enablement: true` al paso de configure-pages:

```yaml
- name: Setup Pages
  uses: actions/configure-pages@v5
  with:
    enablement: true  # ← CLAVE
```

## Workflow completo correcto
```yaml
name: Desplegar a GitHub Pages
on:
  push:
    branches: [ main ]
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: true
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
        with:
          enablement: true
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
        id: deployment
```

## Verificación
1. El repo debe ser PÚBLICO (Pages no funciona en privados con plan free)
2. Pages → Settings → Build and deployment → Source = "GitHub Actions"
3. Token necesita scopes: `pages: write`, `id-token: write`

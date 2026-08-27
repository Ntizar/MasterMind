---
name: github-pages-modern-deploy
description: Procedimiento correcto para hacer deploy de proyectos estáticos a GitHub Pages — método moderno con actions/deploy-pages@v4, nunca usar el legacy peaceiris/actions-gh-pages
category: devops
---

# GitHub Pages — Deploy Moderno (Método Correcto)

## Problema

El método **legacy** (`peaceiris/actions-gh-pages@v4` + branch `gh-pages`) está **obsoleto**.
GitHub está migrando todo al **GitHub Pages Deploy v2**. Los workflows legacy dan errores.

## Método CORRECTO (usar SIEMPRE)

Plantilla completa para repositorios con archivos estáticos (HTML/CSS/JS):

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
        id: deployment
```

## Reglas

1. **NUNCA uses** `peaceiris/actions-gh-pages@v4` — está legacy, da errores
2. **NUNCA uses** branch `gh-pages` — deploy directo desde `main`
3. **NUNCA necesites** `setup-node`, `npm ci`, `npm run build` — eso es solo si tu proyecto ES una app Node.js que genera archivos estáticos
4. **Siempre** las 3 permissions: `contents`, `pages`, `id-token`
5. **Siempre** el `concurrency` block para cancelar builds duplicados
6. **Siempre** `environment: github-pages` con la URL

## Casos especiales

### Proyecto que necesita build (ej: Vite, Next.js, React)

Si el proyecto requiere un build step (genera `dist/`):

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: 'dist/'
      - uses: actions/deploy-pages@v4
        id: deployment
```

### Proyecto con contenido en subdirectorio

Si los archivos estáticos están en un subfolder (ej: `frontend/`):

```yaml
      - uses: actions/upload-pages-artifact@v3
        with:
          path: 'frontend/'
```

## Verificar que funciona

Tras el push:
1. GitHub Actions → runs → debe ser verde
2. GitHub Settings → Pages → debe mostrar "Deployed to github-pages"
3. URL: `https://<usuario>.github.io/<repo>/`

## Ejemplos de repos que usan el método correcto

- `/root/workspace/CallesDinamicas/.github/workflows/pages.yml`
- `/root/workspace/GBFSSpain/.github/workflows/pages.yml`
- `/root/workspace/ISOTime/.github/workflows/pages.yml`
- `/root/workspace/DataHubEspana/.github/workflows/pages.yml`

## Ejemplo de método legacy (NO USAR)

- `/root/workspace/NapMaps/.github/workflows/deploy-pages.yml` ❌

## Pitfalls

- Si el workflow usa `peaceiris/actions-gh-pages` → **rewrite completo** al método moderno
- Si el workflow crea una branch `gh-pages` → **eliminar** esa branch, deploy directo desde `main`
- El `id-token: write` es obligatorio para la verificación de GitHub Pages
- Si hay error de permisos, verificar que las 3 permissions están en el workflow y que GitHub Pages está habilitado en Settings → Pages

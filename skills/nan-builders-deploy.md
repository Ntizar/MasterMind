---
id: "skill-04"
nombre: nan-builders-deploy
tipo: skill
rol: patrón de deploy estático para nan.builders y GitHub Pages
version: "1.0.0"
autor: comunidad nan.builders
licencia: MIT
plataformas: [nan.builders, github-pages]
tags: [deploy, static, nan-builders, github-pages, actions, curl, browser-tool]
creado: 2026-06-03
actualizado: 2026-06-03
---

# Patrón: Deploy Estático — nan.builders y GitHub Pages

## Qué es

Un patrón de despliegue estático para plataformas con restricciones específicas:
nan.builders (subdominios *.apps.nan.builders) y GitHub Pages.
Ambas plataformas comparten el patrón de archivos estáticos, pero tienen
limitaciones distintas que requieren estrategias diferentes.

### Plataformas soportadas

| Plataforma | Tipo | URL | Herramienta de análisis |
|-----------|------|-----|------------------------|
| **nan.builders** | Subdominio *.apps.nan.builders | `https://[nombre].apps.nan.builders` | `curl` (browser tool roto en subdominios) |
| **GitHub Pages** | Repo-based | `https://[usuario].github.io/[repo]` | actions/deploy-pages@v4 |

## Cuándo usar

- **Cuando el output es un sitio estático** (HTML/CSS/JS sin backend).
- **Cuando se necesita deploy rápido** sin configuración de servidor.
- **Cuando se trabaja con nan.builders** y el browser tool no funciona en subdominios.
- **Cuando se necesita verificación automática** del deploy.

## Pasos

### Paso 1: Preparar los archivos estáticos

Organizar los archivos según la plataforma destino:

```
output/
├── index.html          # Página principal
├── .nojekyll           # Para GitHub Pages (desactivar Jekyll)
├── favicon.ico         # Favicon en raíz del dominio
└── sw.js               # Service worker (si aplica, con rutas relativas)
```

**Reglas generales:**
- No servir desde `/public` — los archivos van en la raíz del directorio de deploy.
- Service worker con rutas relativas (no absolutas).
- Favicon en la raíz del dominio (`/favicon.ico`), no en `/images/`.
- Sin archivos externos que fallen en subdominios (fuentes de Google Fonts, CDNs).

### Paso 2: Deploy a nan.builders

**Problema conocido:** El browser tool está roto en subdominios `*.apps.nan.builders`.
**Solución:** Usar `curl`-based analysis para verificar el deploy.

```bash
# Verificar que el sitio responde
curl -I https://[nombre].apps.nan.builders

# Verificar que el contenido HTML se sirve correctamente
curl -s https://[nombre].apps.nan.builders | head -20

# Verificar tamaño de respuesta
curl -s -o /dev/null -w "%{size_download}" https://[nombre].apps.nan.builders

# Verificar headers de caché
curl -I https://[nombre].apps.nan.builders | grep -i cache
```

**Restricciones de nan.builders:**
- No hacer bind al puerto 80 desde contenedor no-root (el puerto 80 es privilegiado, requiere root).
- Límite de espacio/recursos — mantener archivos pequeños (<50KB por archivo HTML).
- Sin backend — solo archivos estáticos.
- Sin soporte para server-side rendering.

**Verificación post-deploy:**
```bash
# 1. Verificar que el subdominio responde
curl -s -o /dev/null -w "%{http_code}" https://[nombre].apps.nan.builders

# 2. Verificar que el HTML contiene el contenido esperado
curl -s https://[nombre].apps.nan.builders | grep -c "nan.builders"

# 3. Verificar que no hay errores 404
curl -s -o /dev/null -w "%{http_code}" https://[nombre].apps.nan.builders/missing-page
```

### Paso 3: Deploy a GitHub Pages

**Requisitos mínimos:**
- Branch `main` (o `master` para repos antiguos).
- Workflow en `.github/workflows/deploy.yml`.
- Archivo `.nojekyll` en la raíz para desactivar Jekyll.

**Workflow de ejemplo:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

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
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Configuración del repo:**
1. Ir a Settings → Pages → Source: `GitHub Actions`.
2. Asegurar que el branch `main` es el default.
3. Añadir `.nojekyll` en la raíz del repo.

**Verificación post-deploy:**
```bash
# Verificar que el site está live
curl -I https://[usuario].github.io/[repo]

# Verificar que el HTML se sirve con content-type correcto
curl -sI https://[usuario].github.io/[repo] | grep -i content-type
```

### Paso 4: Verificar que el site está live

**Antes de entregar, SIEMPRE verificar que el site está accesible:**

```bash
# nan.builders
curl -s -o /dev/null -w "HTTP %{http_code} | Size: %{size_download} bytes\n" \
  https://[nombre].apps.nan.builders

# GitHub Pages
curl -s -o /dev/null -w "HTTP %{http_code} | Size: %{size_download} bytes\n" \
  https://[usuario].github.io/[repo]
```

**Criterios de verificación:**
- Código HTTP 200
- El HTML contiene el contenido esperado
- El tamaño es razonable (no vacío, no excesivo)
- No hay redirecciones inesperadas

## Pitfalls

| Pitfall | Plataforma | Consecuencia | Cómo evitar |
|---------|-----------|-------------|-------------|
| Browser tool roto en subdominios | nan.builders | No se puede verificar visualmente | Usar `curl` para análisis |
| Bind puerto 80 desde contenedor no-root | nan.builders | Error de permisos, deploy falla | No intentar bind a puerto < 1024 |
| Servir desde /public | Ambas | 404 en la ruta raíz | Poner archivos en la raíz del directorio de deploy |
| Site no verificado antes de entregar | Ambas | Se entrega deploy que no funciona | Siempre hacer curl -I antes de entregar |
| Service worker con rutas absolutas | Ambas | Rutas rotas en subdominios | Usar rutas relativas en service worker |
| Favicon en /images/favicon.ico | Ambas | 404 en favicon | Poner favicon en la raíz del dominio |
| .nojekyll omitido | GitHub Pages | Archivos con `__` no se procesan | Siempre incluir .nojekyll en la raíz |
| Google Fonts en subdominios | nan.builders | Fuentes no cargan | Usar fuentes del sistema o inline |

### Pitfall detallado: Browser tool en nan.builders

El browser tool tiene un bug conocido en subdominios `*.apps.nan.builders`:
- No puede renderizar la página correctamente.
- No puede interactuar con el DOM.
- No puede tomar screenshots.

**Solución:** Usar `curl` para análisis:

```bash
# Análisis básico
curl -s https://[nombre].apps.nan.builders > /tmp/deploy-check.html
file /tmp/deploy-check.html
wc -c /tmp/deploy-check.html
grep -c "<html" /tmp/deploy-check.html

# Análisis de contenido
grep -i "nan.builders" /tmp/deploy-check.html | head -5

# Análisis de errores
grep -i "error\|fail\|broken" /tmp/deploy-check.html | head -5
```

### Pitfall detallado: Service worker con rutas relativas

Los service workers en subdominios nan.builders pueden tener problemas con rutas absolutas:

**Mal:**
```javascript
// sw.js — RUTAS ABSOLUTAS (fallan en subdominios)
self.addEventListener('fetch', event => {
  event.respondWith(fetch('/assets/cache-key'));
});
```

**Bien:**
```javascript
// sw.js — RUTAS RELATIVAS (funcionan en subdominios)
self.addEventListener('fetch', event => {
  event.respondWith(fetch('./assets/cache-key'));
});
```

## Verificación

Antes de considerar el deploy como completado, verificar:

1. **Archivos preparados**: ¿Todos los archivos están en la raíz del directorio de deploy?
2. **nan.builders**:
   - ¿El curl -I devuelve HTTP 200?
   - ¿El contenido HTML es el esperado?
   - ¿El tamaño es razonable (<50KB)?
   - ¿No se intentó bind a puerto 80?
3. **GitHub Pages**:
   - ¿El workflow usa actions/deploy-pages@v4?
   - ¿El branch es main?
   - ¿El archivo .nojekyll está en la raíz?
   - ¿El site responde con HTTP 200?
4. **Verificación final**:
   - ¿El site está live (curl -I confirma 200)?
   - ¿El favicon está en la raíz del dominio?
   - ¿El service worker (si existe) usa rutas relativas?
   - ¿No hay archivos externos que puedan fallar?

Si algún punto falla → el deploy no está completado y debe corregirse.

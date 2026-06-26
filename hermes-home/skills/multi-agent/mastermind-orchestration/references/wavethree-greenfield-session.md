# WaveThree — Greenfield Cron Session (2026-06-17)

## Resumen

Construcción del visor marino 3D WaveThree desde cero usando el patrón greenfield con pipeline de crons one-shot. Proyecto: Three.js + Vite + WebGL + GH Pages.

## Timeline real

| Hora | Fase | Qué pasó |
|------|------|----------|
| 17:18 | 1.0 — Scaffold | Repo creado, estructura de directorios, README, ARCHITECTURE.md, ADR-001, package.json workspaces, vite.config.js, .gitignore, scenario JSONs. Commit inicial. |
| 17:18 | 1.1 — MVP visual (manual) | Mastermind mejoró el shader Gerstner (10 ondas, espuma con fractal noise, Fresnel, Blinn-Phong, color-by-depth, cielo degradado), setup de escena (sky dome, Exp2 fog, 3 luces), index.html glassmorphism + FPS + keyboard shortcuts. Commit + push + GH Pages OK. |
| ~17:18 | Arranque crons | 9 crons one-shot cada hora desde 17:18 hasta 01:18 UTC del día siguiente. |
| ~17:30 | Cancelación crons | Se cancela cron F1.1 porque el MVP se hizo manualmente. |
| --:-- | F1.2 — UI avanzada | Pendiente (cron a las 18:18) |
| --:-- | F1.3 — Pipeline GEBCO | Pendiente (cron a las 19:18) |

## Decisiones de arquitectura tomadas

- **Zona piloto:** Gijón/Cantábrico — GEBCO coverage (0.004° grid), boyas reales, EMODnet bathymetry, SWAN model
- **Shader:** Gerstner custom (10 waves) → después JONSWAP + iFFT
- **WebGPU → WebGL:** WebGPURenderer no exportado en Three.js r170. Fallback a WebGLRenderer.
- **Repo público:** GH Pages gratuito requiere repo público. Datos abiertos (GEBCO, SWAN) justifican apertura.
- **Estructura monorepo:** apps/web-viewer/ + apps/preprocessing/ + src/ (scene, ocean, bathymetry, structures, ui, loaders) + data/ (raw, processed, scenarios) + docs/

## Pitfalls encontrados (sesión real)

1. Import paths 3 niveles: desde apps/web-viewer/src/main.js → src/ocean/gerstner.js requiere ../../../src/ocean/gerstner.js
2. netcdf@0.4.1 no existe en npm: el paquete correcto es netcdfjs@^4.0.0
3. WebGPURenderer no disponible en Three.js v0.170.0: usar WebGLRenderer + antialias
4. GH Actions + Pages: peaceiris/actions-gh-pages@v4 funciona, necesita publish_dir: ./dist
5. Cron one-shot con schedule ISO: cronjob(action='create', schedule='2026-06-17T17:18:00Z') programa para ese momento exacto
6. Cancelar crons manualmente tras adelantar trabajo
7. Glassmorphism CSS: backdrop-filter: blur(10px) necesita soporte de navegador, no funciona en todos los entornos WebUI

## Archivos creados

- /root/workspace/WaveThree/README.md — visión, tesis, roadmap 7 fases
- /root/workspace/WaveThree/docs/architecture/ARCHITECTURE.md — Mermaid, 6 capas
- /root/workspace/WaveThree/docs/decisions/ADR-001-estrategia-arquitectura.md
- /root/workspace/WaveThree/docs/sources/FASE-0-investigacion.md — Gijón, GEBCO, SWAN
- /root/workspace/WaveThree/src/ocean/gerstner.js — shader Gerstner 10 ondas
- /root/workspace/WaveThree/src/scene/setup.js — sky dome, niebla, luces, cámara
- /root/workspace/WaveThree/apps/web-viewer/src/main.js — entry, 4 escenarios, OrbitControls
- /root/workspace/WaveThree/apps/web-viewer/index.html — UI glassmorphism
- /root/workspace/WaveThree/apps/web-viewer/vite.config.js — alias, publicDir, port 3000
- /root/workspace/WaveThree/data/scenarios/*.json — 4 escenarios (temporal, swell, calm, storm)
- /root/workspace/WaveThree/.github/workflows/deploy-gh-pages.yml
- /root/workspace/WaveThree/src/bathymetry/index.js — placeholder
- /root/workspace/WaveThree/src/structures/index.js — placeholder
- /root/workspace/WaveThree/src/loaders/index.js — placeholder
- /root/workspace/WaveThree/src/ui/index.js — placeholder
- /root/workspace/WaveThree/.gitignore

## Comandos clave

```bash
# Crear repo privado
curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d '{"name":"WaveThree","private":true,"description":"Visor marino 3D con Three.js, WebGPU y datos oceanográficos"}'

# Clonar y setup
git clone https://github.com/Ntizar/WaveThree.git
cd WaveThree && npm install -w apps/web-viewer -w apps/preprocessing

# Build
cd apps/web-viewer && npx vite build

# GH Pages deploy workflow
# .github/workflows/deploy-gh-pages.yml con peaceiris/actions-gh-pages@v4

# Hacer repo público
curl -X PATCH -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/Ntizar/WaveThree \
  -d '{"private":false}'

# Habilitar Pages
curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/Ntizar/WaveThree/pages \
  -d '{"source":{"branch":"gh-pages","path":"/"}}'
```

## Estado del proyecto (post-sesión)

- Repo: github.com/Ntizar/WaveThree (público)
- GH Pages: https://ntizar.github.io/WaveThree/ (HTTP 200)
- Último commit: ece4c39 — "Fix: import paths, WebGL renderer, build OK"
- 9 crons programados: F1.2 → F1.3 → F2.1 → F2.2 → F3 → F4 → F5 → Auditoría
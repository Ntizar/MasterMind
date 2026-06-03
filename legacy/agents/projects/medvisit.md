---
nombre: medvisit
alias: medvisit
tipo: proyecto
clusters: [web, mobile]
repo_local: C:\Ntizar_Obsidian\Ntizar_Brain\Github\medvisit
estado: activo
---

# medvisit

App de gestión de visitas médicas para visitador médico. PWA instalable como APK Android sin pasar por Google Play. Funciona 100% offline tras la primera carga.

## Stack
- HTML5 + CSS3 + JS vanilla (sin frameworks)
- localStorage (persistencia offline)
- Service Worker (cache para offline)
- Netlify (hosting HTTPS gratuito)
- PWABuilder → Android TWA (generación del APK)
- SheetJS (exportación Excel desde CDN)

## Decisiones arquitectónicas permanentes
- Iconos deben ser PNG binarios reales — verificar magic bytes `89504e47` antes de desplegar
- SVG renombrado a .png causa fallo silencioso en PWABuilder (`Could not find MIME for Buffer <null>`)
- Generador de iconos: `genera-iconos-png.js` con Jimp v1 (`const { Jimp } = require('jimp')`)
- Deploy: `netlify deploy --auth="[token]"` — el flag `--auth` es más fiable que variable de entorno en Windows
- APK es una TWA: la URL de Netlify debe seguir activa para que la app funcione
- CDN externas (SheetJS, etc.) no están en el cache del SW → fallan sin internet en funciones críticas

## Pendientes conocidos
- Bundling local de SheetJS para funcionamiento offline completo

## Learnings de este proyecto
- (skill completo en [[agents/skills/pwa-android]])

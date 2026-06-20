---
name: nan-deploy-sync
version: "1.0.0"
description: "Procedimiento para verificar y forzar sync de deploy NaN Builders con GitHub — downloadGitHubDB, initDB, token .env, verificación post-deploy."
tags: [nan-builders, deploy, sync, github, lladosapp, dieta]
---

# Nan Deploy Sync

Cuando un deploy de NaN Builders está vacío tras un redeploy, o los datos no aparecen.

## Problema

NaN reinicia el contenedor en cada deploy. Si `initDB()` no descarga la DB de GitHub, cada contenedor empieza vacío.

## Solución en server.js

`initDB()` debe llamar a `downloadGitHubDB()` antes de cargar la DB. La función lee `GITHUB_TOKEN` de:
1. `process.env.GITHUB_TOKEN`
2. `.env` del proyecto (`path.join(__dirname, '.env')`)

**NUNCA leer de `/hermes-home/.env`** — no existe dentro del contenedor.

## Verificación post-deploy

Usar X-Session-Id header, no cookies:

```bash
# Login
curl -s -X POST -H 'Content-Type: application/json' \
  https://dieta-ntizar-ntizar.apps.nan.builders/api/auth/login \
  -d '{"nombre":"David Antizar","pin":"5101"}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sessionId',''))"

# Datos
curl -s -H 'X-Session-Id: <session_id>' \
  https://dieta-ntizar-ntizar.apps.nan.builders/api/datos | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('comidas',[])), 'comidas')"
```

Si 0 comidas: esperar 2-5 min (NaN tarda en arrancar). Reintentar.

## Cloudflare CDN Cache en NaN — Pitfall Crítico

NaN.builders usa Cloudflare como CDN. Cloudflare cachea HTTP 404/HTML fallback con `max-age=14400` (4 horas).

### El problema

Cuando despliegas un **archivo JS nuevo** (nunca servido antes), si por cualquier razón la CDN ve primero la respuesta fallback SPA de NaN (HTML/404), **cachea esa respuesta HTML durante 4h**. Aunque el deploy real ya tenga el archivo, los navegadores reciben el HTML cacheado como si fuera el JS.

### Por qué `?v=N` no es suficiente

```html
<script src="js/gtfs-engine.js?v=7"></script>   <!-- OK, query param -->
```

Esto funciona para `<script>` tags. Pero si tu archivo JS **a su vez importa** otro módulo ES:

```javascript
// dentro de main.js — ES Module import
import { GTFSEngine } from './gtfs-engine.js';  // ¡sin query param!
```

`import` statements no llevan query params (especificación ES modules). El navegador pide `./gtfs-engine.js` sin `?v=7`, y si la CDN tiene cacheada una versión anterior (o un 404), recibes basura.

### La solución: versionar el nombre del archivo

```javascript
// NO: gtfs-engine.js (puede tener cache 404)
// SÍ: gtfs-engine.v7.js (nombre único por build)
import { GTFSEngine } from './gtfs-engine.v7.js';
```

Esto fuerza a la CDN a pedir una URL que **nunca ha existido antes**, garantizando que ve el contenido real.

### Reglas prácticas

- Para archivos JS que son ES modules importados por otros: usar versionado en nombre (`nombre.v{N}.js`)
- Para `<script src>` tags: query param `?v=N` es suficiente
- Para CSS: query param funciona bien (no hay imports ES)
- Si detectas que un archivo nuevo sirve HTML en vez de JS en NaN: es el CDN cache. Renombrar con versión.
- Tras renombrar, actualizar TODOS los imports en los archivos que lo referencian

### Cómo verificar

```bash
# Ver headers de CDN
curl -sI "https://timeineco-ntizar-ntizar.apps.nan.builders/js/gtfs-engine.js" | grep -i "content-type\|cf-cache-status"
# Si muestra 'cf-cache-status: HIT' y 'content-type: text/html', está cacheado el fallback
```

## LladosApp usa SQLite

LladosApp lee de `data/masterfit.db` (SQLite), NO de `data/database.json`.
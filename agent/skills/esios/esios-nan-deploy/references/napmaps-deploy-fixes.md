# NapMaps — Deploy fixes definitivos para NaN.builders (Junio 2026)

Repositorio: `github.com/Ntizar/NapMaps` (privado)
Stack: Vite 6.3.0 + MapLibre GL JS 4.7.1 + Node 20 Alpine
Puerto: 3030
URL NaN: `napmaps-ntizar-ntizar.apps.nan.builders`
Estado: ✅ Desplegado y funcionando (200 OK)

## Problemas encontrados y fixes

### 1. `\"type\": \"module\"` + `require()` = CRASH silencioso

- **Causa:** `package.json` tiene `\"type\": \"module\"` pero el Dockerfile inlineaba `require(\"http\")` en `server.js`
- **Efecto:** Node.js ejecuta `.js` como ESM → `require()` es undefined → crash al arrancar
- **Síntoma:** Kaniko build exitoso, pod nunca arranca, NaN muestra \"Pending\" o 503
- **Fix:** Crear `server.mjs` como archivo separado en ESM puro (`import http from \"node:http\"`)

### 2. `npm ci --include=dev` en producción

- **Causa:** El Dockerfile original instalaba devDependencies en producción
- **Fix:** Multi-stage build 3 etapas:
  1. `deps` → `npm ci --include=dev` (todas las deps)
  2. `builder` → copia `node_modules` + `npx vite build`
  3. `runner` → `npm ci --omit=dev` (solo producción) + copia de `dist/`

### 3. Vite `base` path incorrecto

- **Original:** `base: '/NapMaps/'` (heredado de GitHub Pages)
- **Fix:** `base: '/'` para que NaN sirva desde raíz

### 4. Servidor inline en Dockerfile vs archivo separado

- **Original:** `RUN echo '...' > server.js` inlineado en Dockerfile
- **Problema:** No se puede lintear, no se puede testear, difícil de mantener
- **Fix:** `server.mjs` como archivo real en el repo, `COPY --chown=appuser:appgroup server.mjs ./`

### 5. Strings truncados con `***` sin cerrar — loading eterno

- **Causa:** 3 URLs de API (2 de estilos MapLibre + 1 de tiles DEM) tenían `***` como placeholder de API key y les faltaba la comilla de cierre
- **Efecto:** Error de sintaxis JS → el script ni siquiera se parsea → `DOMContentLoaded` nunca se ejecuta → `init()` nunca se llama → loading spinner infinito
- **Síntoma:** Pantalla de loading con spinner "NM" + barra de progreso, nada se renderiza, consola vacía (error de sintaxis ocurre antes de cualquier console.log)
- **Líneas afectadas:** 27, 32, 325 en `src/js/app.js`
- **Fix:** Usar concatenación de variables: `'https://...?api_key=' + API_KEY` donde `API_KEY` está definido al inicio del archivo
- **Detección:** `node -c src/js/app.js` → si falla, hay error de sintaxis. O usar `execute_code` para contar comillas impares en líneas con `uri:` o `tiles:`
- **Verificación post-fix:** `node -c` pasa → `npm run build` compila → servidor responde 200

## Estructura final del Dockerfile (3 stages)

```dockerfile
FROM node:20-alpine AS deps       # npm ci --include=dev
FROM node:20-alpine AS builder     # npx vite build
FROM node:20-alpine AS runner      # npm ci --omit=dev + server.mjs
```

## Comandos de verificación

```bash
# Health check
curl -s https://napmaps-ntizar-ntizar.apps.nan.builders/healthz
# Expected: {"status":"ok","uptime":...}

# Main page
curl -sI https://napmaps-ntizar-ntizar.apps.nan.builders/
# Expected: 200 + content-type: text/html

# Verificar ESM/CJS conflict
grep '"type"' package.json && grep 'require(' server.mjs || echo "OK: no conflict"

# Verificar sintaxis JS
node -c src/js/app.js  # Debe dar "Syntax OK"
```

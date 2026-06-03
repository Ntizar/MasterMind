---
nombre: PWA to APK Android
tipo: skill
clusters: [mobile, web]
aplica_a: apps móviles, PWA
creado: 2026-03-20
---

# Skill: PWA → APK Android con PWABuilder + Netlify

## Aplica cuando
- La tarea es construir una app móvil Android sin React Native ni Flutter
- El cliente no tiene servidor, quiere todo offline con localStorage
- Se necesita un APK instalable sin pasar por Google Play
- El stack es HTML + CSS + JS vanilla (o cualquier SPA estática)

---

## Stack probado
- **Frontend**: HTML5 + CSS3 + JS vanilla, sin frameworks
- **Almacenamiento**: localStorage (100% offline tras primera carga)
- **Hosting**: Netlify (gratuito, sin tarjeta, sin GitHub requerido)
- **Generador APK**: PWABuilder (pwabuilder.com) → Android TWA
- **Iconos**: Jimp (npm, puro JS, sin dependencias nativas)
- **Excel export**: SheetJS desde CDN

---

## Fases universales

1. **Estructura PWA mínima** — Tres archivos obligatorios para que PWABuilder acepte la app:
   - `manifest.json` con `name`, `short_name`, `start_url`, `display: standalone`, `icons` (192 y 512)
   - `sw.js` (service worker registrado en index.html)
   - Iconos **PNG binarios reales** (ver sección crítica abajo)

2. **Generar iconos PNG reales** — Usar el script `genera-iconos-png.js` con Jimp v1.
   Instalar localmente: `npm install jimp --prefix [carpeta-app]`

3. **Deploy a Netlify** — Via Netlify CLI con `--auth` flag:
   ```
   netlify deploy --dir="[ruta]" --site="[site-id]" --prod --auth="[token]"
   ```
   No usar `set NETLIFY_AUTH_TOKEN=...` en Windows CMD — no funciona.
   Usar `--auth` flag directo o PowerShell con `$env:NETLIFY_AUTH_TOKEN=...`.

4. **Generar APK en PWABuilder** — Ir a pwabuilder.com, pegar URL, esperar análisis,
   clic en "Package for stores" → Android → Download.
   El APK generado es una **TWA (Trusted Web Activity)**: wrapper Android que carga la URL.

5. **Instalar APK en Android** — Pasar el .apk al móvil, activar "Fuentes desconocidas",
   instalar. Requiere conexión para el primer arranque (carga desde Netlify);
   después el service worker sirve la app offline.

---

## Decisiones clave

| Pregunta | Por qué es bloqueante |
|----------|-----------------------|
| ¿Los iconos son PNG binarios reales? | PWABuilder/Bubblewrap parsea bytes — si el archivo es SVG renombrado, falla con `Could not find MIME for Buffer <null>` |
| ¿El hosting es HTTPS? | TWA requiere HTTPS obligatorio. Netlify lo proporciona gratis |
| ¿El manifest tiene `start_url`? | Sin él PWABuilder no puede crear el TWA |
| ¿El service worker está registrado en index.html? | Sin SW, PWABuilder baja la puntuación y puede rechazar el packaging |
| ¿SheetJS (u otras CDN) se usan offline? | Las CDN externas no están en el cache del SW → fallan sin internet. Considerar bundling local para funciones críticas |

---

## Script generador de iconos (Jimp v1)

```js
// genera-iconos-png.js — genera PNG binarios reales con Jimp v1
const { Jimp } = require('jimp');  // Jimp v1: export nombrado, NO default
const path = require('path');

async function crearIcono(size, outputPath) {
  const img = new Jimp({ width: size, height: size, color: 0x1a73e8ff });

  const grosor = Math.round(size * 0.12);
  const largo  = Math.round(size * 0.55);
  const cx = Math.round(size / 2);
  const cy = Math.round(size / 2);

  // Barra horizontal (cruz blanca)
  for (let y = cy - Math.floor(grosor/2); y < cy + Math.ceil(grosor/2); y++)
    for (let x = cx - Math.floor(largo/2); x < cx + Math.ceil(largo/2); x++)
      img.setPixelColor(0xffffffff, x, y);

  // Barra vertical
  for (let x = cx - Math.floor(grosor/2); x < cx + Math.ceil(grosor/2); x++)
    for (let y = cy - Math.floor(largo/2); y < cy + Math.ceil(largo/2); y++)
      img.setPixelColor(0xffffffff, x, y);

  await img.write(outputPath);  // Jimp v1 usa .write(), NO .writeAsync()
}

(async () => {
  await crearIcono(192, path.join(__dirname, 'icon-192.png'));
  await crearIcono(512, path.join(__dirname, 'icon-512.png'));
})();
```

**Verificar que los iconos son PNG reales antes de desplegar:**
```js
const b = require('fs').readFileSync('icon-192.png');
console.log(b.slice(0,8).toString('hex'));
// Debe ser: 89504e470d0a1a0a
// Si empieza por 3c73766720786d6c → es SVG renombrado, fallará
```

---

## Reglas

- **Nunca** generar iconos como SVG y renombrarlos a `.png` — Bubblewrap falla con `Buffer <null>`
- Jimp v1 usa `const { Jimp } = require('jimp')` (export nombrado) y `.write()` (no `.writeAsync()`)
- El `--auth` flag de Netlify CLI es más fiable que la variable de entorno en Windows
- El APK de PWABuilder es una TWA: necesita que la URL siga activa en Netlify
- Revocar tokens de Netlify tras el deploy — no dejarlos en código ni en historial

---

## Anti-patrones (nunca hacer)

- Usar `canvas` o `sharp` sin verificar que están instalados — no están disponibles por defecto en Node limpio
- Asumir que `require('jimp')` devuelve la clase directamente en v1 — en v1 es `{ Jimp }`
- Usar `set VAR=valor && comando` en Windows para pasar env vars a CLI — no funciona en todos los contextos; usar `--auth` flag o PowerShell
- Desplegar sin verificar los magic bytes del PNG — el error aparece solo en PWABuilder, no antes
- Depender de CDN para funcionalidades offline críticas (Excel, gráficos, etc.)

---

## Patrones probados

- **vanilla-pwa-android**: HTML+CSS+JS vanilla + localStorage + Netlify + PWABuilder = APK funcional sin frameworks
- **jimp-real-png**: instalar Jimp localmente con `--prefix` para no contaminar el proyecto raíz
- **netlify-cli-auth-flag**: `netlify deploy --auth="[token]"` es más portable en Windows que variables de entorno

---

## Creado
Fecha: 2026-03-20
Revisado: —
Origen: medvisit-app — app de gestión de visitas médicas para visitador médico, APK Android vía PWABuilder + Netlify

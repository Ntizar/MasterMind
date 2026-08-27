# Vite HTML Script Processing - Referencia Completa

## Resumen

Vite solo transforma scripts ES modules (`type="module"`). Scripts de página (IIFEs sin `type="module"`) se ignoran completamente, incluso con rutas absolutas.

---

## Patrón A — Rutas relativas vs absolutas (ES modules)

Vite solo transforma scripts con rutas absolutas en `index.html`:

```html
<!-- ❌ MALO — Vite ignora rutas relativas -->
<script type="module" src="js/app.js"></script>

<!-- ✅ BUENO — Vite transforma a /assets/hash.js -->
<script type="module" src="/js/app.js"></script>
```

Resultado del build:
```html
<script type="module" crossorigin src="/assets/index-Bx2mQ8iP.js"></script>
```

---

## Patrón B — Scripts de página (IIFEs, sin type="module")

**Problema:** Vite **no transforma** scripts `<script src="/js/app.js">` aunque tengan ruta absoluta. Los scripts IIFE no son ES modules, así que Vite los ignora.

**Síntoma:**
- HTML desplegado muestra `{{ }}` sin procesar (Vue no carga)
- `dist/` no contiene los archivos JS
- `curl /js/app.js` → 404

**Solución — Post-build script (`postbuild.js`):**

1. Copia los scripts JS/CSS a `dist/js/` y `dist/css/`
2. Transforma las referencias en el HTML (`/js/` → `js/`)
3. Se ejecuta tras `vite build`

```javascript
// postbuild.js
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const distDir = path.join(__dirname, 'dist');
const srcJsDir = path.join(__dirname, 'js');
const srcCssDir = path.join(__dirname, 'css');

const htmlPath = path.join(distDir, 'index.html');
let html = fs.readFileSync(htmlPath, 'utf-8');

const jsFiles = ['app.js', 'simulator.js', 'charts.js', /* ... */];
fs.mkdirSync(path.join(distDir, 'js'), { recursive: true });
for (const js of jsFiles) {
    const src = path.join(srcJsDir, js);
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(distDir, 'js', js));
}

fs.mkdirSync(path.join(distDir, 'css'), { recursive: true });
const cssFiles = ['app.css', 'ntizar.css'];
for (const css of cssFiles) {
    const src = path.join(srcCssDir, css);
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(distDir, 'css', css));
}

// Transformar referencias: /js/ → js/ (sin barra leading)
html = html.replace(/src="\/js\//g, 'src="js/');
html = html.replace(/href="\/css\//g, 'href="css/');
fs.writeFileSync(htmlPath, html);
```

En `package.json`:
```json
{
  "scripts": {
    "build": "vite build && node postbuild.js"
  }
}
```

---

## Patrón C — Convertir a ES modules (solución elegante)

Si es posible, convertir los IIFEs a ES modules con `export` y usar `type="module"` en el HTML. Vite los transforma automáticamente.

---

## Diagnóstico

1. Abrir el HTML desplegado y buscar `<script src="...">`:
   - Si ves `src="js/..."` → Vite no lo procesó (Patrón B) → **los archivos existen en el deploy** (post-build los copió)
   - Si ves `src="/js/..."` → Vite no lo procesó (ruta absoluta sin type="module") → **los archivos NO existen** → 404
   - Si ves `src="/assets/..."` → Vite sí lo procesó (ES module)

2. Comprobar 404s:
   ```bash
   curl -sI https://sitio.com/js/app.js | grep HTTP
   # Si da 404 → el script no se transformó ni se copió
   ```

3. Ver el build local:
   ```bash
   cat dist/index.html | grep '<script'
   # Si ves src="js/..." → Vite no procesó tus scripts
   # Si ves src="/js/..." → Vite los reconoció pero no los transformó (IIFE)
   # Si ves src="/assets/..." → Vite sí los procesó (ES module)
   ```

### Flujo de diagnóstico rápido (2026-06)

Cuando la web muestra `{{ }}` literal (Vue no renderiza):

1. `curl -s https://sitio.com/ | grep 'vue.global.prod'` → ¿Vue CDN está presente?
2. `curl -s https://sitio.com/ | grep 'src="js/'` → ¿Scripts con ruta relativa?
3. `curl -sI https://sitio.com/js/app.js | grep HTTP` → ¿Archivos existen?
4. Si Vue CDN está presente pero los scripts JS dan 404 → **Vite no los transformó**
5. Si tanto Vue como scripts dan 404 → **el deploy sirvió el HTML original, no el build**

---

## Pitfalls

- **`rollupOptions.input` NO transforma** scripts IIFE — solo los incluye como assets en el `dist/`. Combinado con post-build script, es la solución más robusta.
- **`transformIndexHtml` en plugins personalizados NO funciona** como handler nativo de Vite
- **El post-build script es la solución más práctica** para proyectos con scripts legacy
- **GitHub Pages sirve `dist/`** → si los scripts no están en `dist/js/`, dan 404
- **NaN.builders sirve el `dist/` del build** → mismo problema
- **CRÍTICO:** El HTML del repo debe tener rutas absolutas (`/js/...`) para que Vite al menos las reconozca. El post-build las convierte a relativas (`js/...`) para que funcionen en el deploy.
- **Solo aplica a `index.html` en la raíz del proyecto.** Scripts cargados dinámicamente con `createElement('script')` no se ven afectados.
- **No confundir con CDN scripts.** Los scripts CDN (`https://cdn...`) no necesitan transformación.
- **CSS también aplica.** `<link href="css/app.css">` tampoco se transforma sin la barra.

---

## Dockerfile + Vite

Si usas Docker (nginx) para servir el build:
- El Dockerfile copia todo el repo (`COPY . .`) → incluye `js/` y `css/` originales
- Pero el `index.html` tiene rutas absolutas `/js/...` → nginx las resuelve correctamente
- Si usas el post-build script, el HTML tiene rutas relativas `js/...` → también funcionan

**Recomendación:** Si el Dockerfile copia todo el repo, el post-build script no es necesario (los archivos `js/` ya existen). Solo es necesario si sirves solo el `dist/`.
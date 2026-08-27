---
name: pdf-to-landing
description: "Patrón completo para crear una webapp que convierte PDFs de propuestas de diseño en landing pages generadas por IA — extracción de texto, análisis de diseño, generación HTML, descarga directa o deploy."
version: "4.0.0"
tags: [pdf, landing, ia, nan-builders, express, frontend]
---

# PDF-to-Landing — Generador de landing pages desde PDFs

## Descripción

Webapp completa que permite subir un PDF con una propuesta de diseño web y genera automáticamente una landing page HTML basada en el análisis del diseño, usando la API de NaN (qwen3.6).

## Arquitectura (v2 — 2 endpoints limpios)

**⚠️ NO usar un endpoint monolítico** que haga todo (extracción + análisis + generación + deploy). El frontend acabaría haciendo múltiples POST al mismo endpoint con resultados inesperados. Usar 2 endpoints separados:

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Subir PDF  │───▶│  POST        │───▶│  Análisis    │
│  (web UI)   │    │  /api/analyze│    │  (LLM NaN)   │
└─────────────┘    └──────────────┘    └──────┬───────┘
                                              │ design JSON
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Descargar  │◀───│  POST        │◀───│  Usuario     │
│  HTML       │    │  /api/generate│   │  confirma    │
└─────────────┘    └──────────────┘    └──────────────┘
```

**Flujo UX recomendado:**
1. Usuario sube PDF → `POST /api/analyze` → muestra diseño detectado (empresa, colores, sector, tono)
2. Usuario revisa y pulsa "Generar" → `POST /api/generate` → genera HTML
3. Usuario descarga HTML o abre en nueva pestaña

**Por qué 2 endpoints:**
- El usuario puede revisar el análisis ANTES de gastar tokens en generación
- Si el análisis está mal, puede cancelar sin perder nada
- El frontend no necesita estado complejo para sincronizar pasos
- Los errores son claros: "error analizando" vs "error generando"

## Arquitectura v3 — Extracción visual + IA con colores reales

**Problema v2:** La IA "adivinaba" colores del PDF porque solo recibía texto. Los colores generados no correspondían a la identidad visual real.

**Solución v3:** Extraer colores del PDF visualmente (renderizar a canvas → Median Cut) y enviarlos a la IA como datos reales.

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Subir PDF  │───▶│  pdf.js      │───▶│  Median Cut  │
│  (browser)  │    │  renderiza   │    │  extrae      │
└─────────────┘    │  primera     │    │  colores     │
                   │  página      │    └──────┬───────┘
                   └──────────────┘           │ colores hex
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Subir PDF  │───▶│  POST        │───▶│  IA usa      │
│  + colores  │    │  /api/analyze│    │  colores     │
│  detectados │    │  (colores +  │    │  REALES      │
└─────────────┘    │   texto)     │    └──────┬───────┘
                   └──────────────┘           │ design JSON
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Descargar  │◀───│  POST        │◀───│  Usuario     │
│  HTML       │    │  /api/generate│   │  confirma    │
└─────────────┘    └──────────────┘    └──────────────┘
```

## Pasos

### 1. Extracción visual de colores (CLIENT-SIDE, v3+)
- **pdf.js** renderiza **hasta 5 páginas** del PDF a canvas en el navegador (no solo la primera)
- **Median Cut algorithm** extrae los colores dominantes de los píxeles de TODAS las páginas combinadas
- **⚠️ NO FILTRAR colores** — no eliminar blancos/negros/desaturados. El usuario decide cuáles usar. El filtro de saturación eliminaba verdes y pastel de diseños reales.
- **20 buckets** en Median Cut para máxima cobertura (menos = pierde colores minoritarios pero importantes)
- **Deduplicación euclídea** (threshold 30): elimina colores visualmente idénticos sin perder variedad. Sin esto, el mismo verde aparece 3-4 veces con hex casi iguales
- **Muestreo cada 2px** (no 4px) para mayor precisión en la detección
- Muestra los colores detectados como **chips editables** al usuario ANTES de analizar:
  - Clic en el dot → selector de color nativo del navegador
  - Clic en el hex → editar manualmente
  - ✕ → eliminar un color
  - **+ Añadir** → agregar colores manualmente (para correcciones)
- **Por qué multi-página:** Un PDF puede tener colores de marca solo en páginas interiores. Renderizar solo la página 1 pierde esos colores. Con 5 páginas, se capturan todos.
- **Por qué 15 buckets sin filtro:** Un PDF con 70% blanco, 20% verde marca, 5% gris texto, 5% otros → con 6 buckets y filtro, el verde se pierde. Con 15 sin filtro, aparece.
- Ver `references/color-extraction-median-cut.md` para implementación completa

**Por qué client-side:** No necesita servidor pesado, feedback instantáneo, y el usuario ve los colores antes de gastar tokens de IA.

### 2. Extracción de texto (SERVER-SIDE)
- Usar `pdf-parse` v1.1.4 para extraer texto del PDF
- **⚠️ Fijar versión `"1.1.4"` en package.json** — v2.x cambia la API completamente. Ver `references/pdf-parse-compatibility.md` para detalles.
- **Pitfall ESM:** `pdf-parse` no tiene default export. Usar `createRequire`:
  ```javascript
  import { createRequire } from 'module';
  const require = createRequire(import.meta.url);
  const pdfParse = require('pdf-parse');
  ```

### 3. Análisis de diseño con IA (mejorado en v3+)
- Enviar texto extraído **+ colores detectados visualmente** a qwen3.6 vía NaN API
- System prompt incluye: "Estos son los colores REALES extraidos visualmente del PDF. DEBES usarlos como base para la paleta."
- **10 reglas críticas para colores** en el prompt:
  1. `"fondo"` = color de fondo REAL del PDF (blanco, crema, oscuro, etc.)
  2. `"texto"` = color del texto PRINCIPAL (negro, gris oscuro, etc.)
  3. `"colores_dominantes"` = mínimo 5 colores (marca, fondo, texto, acentos)
  4. Si el PDF tiene verde como marca, el primario DEBE ser verde
  5. Fondo y texto son TAN IMPORTANTES como el color de marca
- JSON con: empresa, sector, tono, paleta de colores (usando los hex reales), tipografía, secciones, estilo visual, inspiración, CTA, features, testimonios
- **⚠️ Diseño detectado COMPLETAMENTE EDITABLE (v5+):**
  - Todos los campos son editables: Empresa (text), Sector (text), Tono (select), Inspiración (text), Tipografía (select), Estilo (textarea)
  - Los colores de paleta son editables con color picker + input hex
  - Los cambios del usuario se reflejan en `currentDesign` ANTES de generar
  - **Por qué editable:** La IA a menudo no capta el color exacto (ej: detecta `#ffcfb5` en vez de naranja quemado). El usuario es la última autoridad sobre su identidad visual.
  - UI: título dice "Diseño detectado (edita antes de generar)"
- **Pitfall:** qwen3 envuelve razonamiento en tags `<think>...</think>`. Usar `indexOf`/`substring` en vez de regex para limpiar (evita problemas de escaping con `write_file`).
- **Pitfall prompt colores:** Sin instrucciones explícitas sobre fondo/texto, la IA siempre pone `fondo: #FFFFFF` y `texto: #333333` por defecto aunque el PDF sea oscuro.

### 4. Generación de HTML (mejorado en v3+)
- Enviar diseño analizado a qwen3.6 con **bloque de强制 de colores**:
  ```
  COLOLES OBLIGATORIOS (extraidos del PDF real, NO los cambies):
  - primario: #2E7D32 (extraido del pixel real del PDF)
  - secundario: #4CAF50
  - acento: #81C784
  - fondo: #FFFFFF
  - texto: #000000
  Todos los colores del PDF: #2E7D32, #4CAF50, #81C784, #C8E6C9, #1B5E20
  ```
- El prompt DEBE especificar: "Usa estos colores EXACTAMENTE en las variables CSS y en TODOS los elementos. NUNCA uses colores por defecto azul/naranja."
- **10 reglas de generación:**
  1. Responsive (móvil + desktop)
  2. Moderna (glassmorphism, gradientes sutiles, animaciones CSS)
  3. Un solo archivo HTML con todo inline (CSS + JS)
  4. Google Fonts: Inter para body, Space Grotesk para headings
  5. Footer: "Hecho con ❤️ por David Antizar"
  6. USAR LOS COLORES EXACTOS de la paleta
  7. Hero + servicios + sobre nosotros + testimonios + CTA + footer
  8. NO frameworks — HTML + CSS + JS vanilla
  9. Animaciones fade-in al scroll con IntersectionObserver
  10. CSS variables con los colores exactos
- Landing page responsive, moderna, con glassmorphism
- Footer: "Hecho con ❤️ por David Antizar"
- Un solo archivo HTML con CSS y JS inline

### 5. Frontend — Three.js + Glassmorphism
- **Three.js** para fondo animado: partículas + formas geométricas wireframe + parallax con ratón
- **Liquid glass** para cards: `backdrop-filter: blur(24px) saturate(180%)`, gradientes sutiles, specular highlight
- Colores del fondo adaptados a la paleta del proyecto (azul/naranja por defecto)
- Ver `references/threejs-particle-background.md` para template reutilizable

### 6. Deploy (OPCIONAL — según prefiera el usuario)
- **Opción A (recomendada):** Descarga directa del HTML — sin dependencia de GitHub
- **Opción B:** GitHub Pages (solo frontend estático)
- **Opción C:** NaN Builders (backend + frontend con Dockerfile)
- **Preguntar al usuario** qué prefiere ANTES de implementar deploy automático

## Estructura del proyecto

```
pdf-to-landing/
├── server.js          # Backend Express (upload, extracción, IA)
├── public/
│   └── index.html     # Frontend: Three.js bg + pdf.js + Median Cut + glass UI
├── package.json       # type: "module" OBLIGATORIO
├── Dockerfile         # Multi-stage, non-root user
├── .env               # NAN_API token (NO en Git)
├── .env.example       # Template (SÍ en Git)
├── .gitignore         # Incluye .env
└── .dockerignore      # NO incluye .env
```

### Variables CSS de la paleta detectada
El frontend detecta colores y los envía al backend. El backend los incluye en el prompt de IA. El HTML generado usa CSS variables con esos colores exactos:
```css
:root {
  --primary: #F7931A;    /* color dominante del PDF */
  --secondary: #2C3E50;  /* segundo color */
  --accent: #1ABC9C;     /* color llamativo */
  --bg: #FFFFFF;         /* fondo (siempre claro) */
  --text: #333333;       /* texto oscuro */
}
```

## Deploy en NaN Builders

### Dockerfile mínimo
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./
COPY server.js ./
COPY public/ ./public/
RUN mkdir -p uploads deploy
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:3000/healthz || exit 1
EXPOSE 3000
CMD ["node", "server.js"]
```

### Checklist de deploy
- [ ] `package.json` tiene `"type": "module"` si usa ESM
- [ ] `.gitignore` incluye `.env`
- [ ] `.dockerignore` NO incluye `.env` (se copia al contenedor)
- [ ] Dockerfile tiene `USER appuser` (requisito NaN)
- [ ] Dockerfile tiene `HEALTHCHECK` apuntando a `/healthz`
- [ ] EXPOSE coincide con container port en NaN
- [ ] Server.js usa `process.env.PORT || 3000`
- [ ] `.env` tiene `NAN_API=<token_real>` (no literal `${NAN_API}`)

### Diagnóstico de deploy fallido

| Síntoma | Causa | Solución |
|---------|-------|----------|
| Build Kaniko SUCCEEDED, URL 404 Cloudflare | Contenedor crash al arrancar | Ver logs en cloud.nan.builders |
| Build Kaniko SUCCEEDED, URL 502 | Contenedor crash | Verificar ESM/CJS, token, puerto |
| `import` falla en server.js | package.json sin `"type": "module"` | Añadir `"type": "module"` |
| `pdf-parse` no tiene default export | ESM sin createRequire | Usar `createRequire(import.meta.url)` |
| `.env` tiene literal `${NAN_API}` | Variable no expandida | `source .env && echo "NAN_API=$NAN_API" > .env` |

## Frontend — Visualización del proceso (v5)

El frontend muestra el flujo en 5 fases:
1. 📄 **Upload + Preview** — drag & drop, renderiza hasta 5 páginas con pdf.js
2. 🎨 **Colores detectados** — chips hex extraídos visualmente del PDF (Median Cut, 15 buckets, sin filtro)
3. 🔍 **Análisis IA** — envía PDF + colores al backend, muestra diseño detectado
4. ✏️ **Editar diseño** — TODOS los campos editables (empresa, sector, tono, tipografía, estilo, colores)
5. 🚀 **Generar + Descargar** — usuario decide cuándo generar, descarga HTML o vista previa

**UX clave:** Mostrar colores y análisis ANTES de generar. El usuario ve qué detectó la IA y puede:
- Editar colores antes de analizar (chips editables)
- Editar diseño detectado después del análisis (campos editables)
- Cancelar si está mal

**Three.js background:** Partículas + formas geométricas wireframe con parallax. Colores adaptados a la paleta del proyecto.

## Pitfalls

- **🔴 `const` usado antes de definirlo → ReferenceError (TDZ):** En ESM, `const upload = multer(...)` definido DESPUÉS de `app.post('/api/analyze', upload.single(...), handler)` causa crash inmediato al arrancar. El orden en server.js DEBE ser: (1) imports, (2) `const` de multer/storage/upload, (3) funciones auxiliares, (4) handlers, (5) `app.post()` con rutas, (6) `express.static`, (7) `app.listen()`. Ver `references/server-2-endpoint-pattern.md` para el orden completo.
- **🔴 `write_file` doble-escapa backslashes en regex:** Cuando se escribe código con `write_file` que contiene regex como `new RegExp('[\\s\\S]*?')`, el tool puede duplicar los backslashes (`[\\\\s\\\\S]`). El regex queda roto. **Solución:** Usar `indexOf` en vez de regex para patrones simples (ej: limpiar `<think>` tags con `indexOf`/`substring` en vez de RegExp). Si se necesita regex, verificar con `cat -n file.js | grep 'backslash'` tras escribir.
- **🔴 Endpoint monolítico:** NO poner extracción + análisis + generación + deploy en un solo `POST /api/process`. El frontend hace múltiples calls y recibe resultados parciales o duplicados. Usar 2 endpoints separados: `/api/analyze` y `/api/generate`.
- **🔴 `pdf-parse` v2.x rompe la API de v1:** Desde v2.0.0, `pdf-parse` cambió completamente su API. El paquete ya NO es una función directa. Esto causa `TypeError: pdfParse is not a function` al subir un PDF.
  - **v1 (compatible):** `const pdfParse = require('pdf-parse'); const data = await pdfParse(buffer);`
  - **v2 (NO compatible):** `const { PDFParse } = require('pdf-parse'); const parser = new PDFParse({ data: buffer }); const result = await parser.getText(); await parser.destroy();`
  - **Solución:** Fijar versión: `"pdf-parse": "1.1.4"` en package.json. Si `npm install` instala v2.x, hacer `npm install pdf-parse@1.1.4` explícitamente.
  - **Cuidado:** `npm ci` sin lockfile fija puede instalar v2.x. Verificar siempre con `npm list pdf-parse` tras instalar.
  - **Si se necesita v2:** Reescribir el handler: importar `{ PDFParse }`, crear instancia con `new PDFParse({ data })`, llamar `getText()`, y `destroy()` al final.
- **🔴 `pdf-parse` en ESM:** No tiene default export. Usar `createRequire`.
- **🔴 `package.json` sin `"type": "module"`:** Server.js con `import` crash en contenedor.
- **🔴 `.env` en `.dockerignore`:** El token NAN_API no llega al contenedor. Quitarlo.
- **🔴 `.env` con literal `${VAR}`:** Verificar que contiene el token real, no el literal.
- **🔴 `express.static` captura rutas:** Si hay un archivo estático que coincide con una ruta API, sirve el archivo en vez de la ruta. Definir rutas API ANTES de `express.static`.
- **⚠️ NaN no hereda env vars:** El contenedor necesita `.env` copiado o variables configuradas en el dashboard NaN.
- **⚠️ Build Kaniko exitoso ≠ deploy exitoso:** El build puede pasar pero el contenedor crashar al arrancar. Verificar logs del contenedor, no solo del build.
- **⚠️ Deploy automático no siempre funciona:** NaNBuilders puede no tener auto-deploy configurado. Preguntar al usuario si quiere deploy o solo descarga directa.
- **⚠️ Colores genéricos vs reales:** Sin extracción visual de colores, la IA siempre genera azul/naranja por defecto. La extracción Median Cut del canvas del PDF es la única forma de que la IA use los colores reales de la marca.
- **🔴 Median Cut con filtro elimina colores reales:** El algoritmo original filtraba: `brightness > 240` (blancos), `brightness < 15` (negros), `saturation < 0.08` (grises). Esto ELIMINABA verdes, pastels, y colores desaturados que son legítimos en diseños reales. **Solución:** NO FILTRAR. Devolver todos los colores de los 15 buckets y dejar al usuario decidir cuáles usar. El filtro de saturación es el más dañino — un verde claro como `#81C784` tiene saturación ~0.35 y se filtraba.
- **⚠️ pdf-parse v1.1.1 funciona igual que v1.1.4:** Ambas versiones v1.x usan la misma API (`require('pdf-parse')` como función). No hay necesidad de forzar 1.1.4 específicamente — cualquier v1.x sirve. Lo crítico es NO usar v2.x.
- **⚠️ NaNBuilders .env no se hereda:** Las variables de entorno del host NO están disponibles en el contenedor Docker. El `.env` debe copiarse al contenedor (via `COPY .env .` en Dockerfile) O configurarse en el dashboard NaN (pestaña Env). Si el `.env` está en `.gitignore`, no llega al contenedor por el repo — hay que usar el dashboard NaN.
- **⚠️ `write_file` y regex:** `write_file` puede doble-escapar backslashes en regex. Si necesitas limpiar `<think>` tags, usa `indexOf`/`substring` en vez de RegExp. Ejemplo:
  ```javascript
  // ❌ Regex — puede fallar con doble-escaping
  const clean = content.replace(new RegExp('<think>[\\s\\S]*?</think>', 'g'), '');
  // ✅ indexOf — robusto
  const start = content.indexOf('<think>');
  const end = content.indexOf('</think>') + 8;
  const clean = (start >= 0 && end > 8) ? content.substring(0, start) + content.substring(end) : content;
  ```
- **⚠️ Colores CSS en el HTML generado:** El prompt de generación DEBE incluir los colores como variables CSS explícitas (`:root { --primary: #xxx }`) y exigir su uso en TODOS los elementos. Sin esto, la IA usa azul genérico aunque le des colores en el prompt.
- **🔴 Módulos nativos (`canvas`, `pdfjs-dist`) fallan en Alpine Linux:** Dockerfiles con `node:20-alpine` NO tienen Python ni build tools. Paquetes que necesitan compilación nativa (como `canvas` que usa node-gyp) fallan con `error command sh -c prebuild-install` o `gyp ERR! find Python`. **Solución:** NO instalar `canvas` ni `pdfjs-dist` en el `package.json` del servidor. `pdfjs-dist` se carga vía CDN en el navegador (client-side). Si se necesita renderizado server-side de PDFs, usar `puppeteer` o `playwright` en vez de `canvas`.
- **⚠️ Prompt de generación debe incluir GUÍA DE DISEÑO COMPLETA:** Sin instrucciones específicas de layout, tipografía, botones, cards y animaciones, la IA genera HTML genérico que no se parece al PDF. El prompt DEBE incluir secciones dedicadas para: colores (CSS variables), tipografía (pesos, tamaños, line-height), layout (max-width, grid gap, padding), botones (primario/secundario/hover), cards (glass, border-radius, shadow), animaciones (fade-in, transiciones), y fidelidad al original (copiar texto exacto, mismos colores, mismo estilo).

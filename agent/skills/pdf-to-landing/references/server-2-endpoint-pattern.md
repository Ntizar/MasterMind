# Server.js — Orden correcto de declaraciones (ESM)

## El bug

Cuando `write_file` reescribe un `server.js`, es fácil poner las rutas ANTES de las definiciones de `const`. En ESM con `const`, esto causa `ReferenceError` porque `const` tiene temporal dead zone (TDZ) — no se puede usar antes de la línea donde se define.

```javascript
// ❌ MAL — upload se usa antes de definirse
app.post('/api/analyze', upload.single('pdf'), handleAnalyze);  // ReferenceError!
const upload = multer({ storage, limits: { fileSize: 20 * 1024 * 1024 } });
```

## El orden correcto

```javascript
// 1. Imports
import express from 'express';
import multer from 'multer';
import cors from 'cors';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

// 2. Constants base
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const pdfParse = require('pdf-parse');
const app = express();
const PORT = process.env.PORT || 3000;

// 3. Middleware base
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// 4. Multer (ANTES de usar en rutas)
fs.mkdirSync(path.join(__dirname, 'uploads'), { recursive: true });
const storage = multer.diskStorage({ /* ... */ });
const upload = multer({ storage, limits: { fileSize: 20 * 1024 * 1024 } });

// 5. Funciones auxiliares (getNanToken, extractPdfText, analyzeDesign, etc.)
function getNanToken() { /* ... */ }
async function extractPdfText(fileBuffer) { /* ... */ }
async function analyzeDesign(text, fileName) { /* ... */ }
async function generateLandingHTML(design) { /* ... */ }

// 6. Handlers (definidos ANTES de usar en app.post)
async function handleAnalyze(req, res) { /* ... */ }
async function handleGenerate(req, res) { /* ... */ }

// 7. Rutas API (ANTES de express.static)
app.post('/api/analyze', upload.single('pdf'), handleAnalyze);
app.post('/api/generate', handleGenerate);

// 8. Static files (DESPUÉS de rutas API)
app.use(express.static(path.join(__dirname, 'public')));

// 9. Health check
app.get('/healthz', (req, res) => { /* ... */ });

// 10. Start
app.listen(PORT, () => { /* ... */ });
```

## Por qué este orden

| Sección | ¿Por qué aquí? |
|---------|----------------|
| Imports | Siempre primero |
| Constants base | Necesarios para todo lo demás |
| Middleware base | `cors()`, `json()` — antes de rutas |
| Multer | `upload` se usa en `app.post()` — definir ANTES |
| Funciones auxiliares | `handleAnalyze` llama a `analyzeDesign` — definir ANTES |
| Handlers | Se referencian en `app.post()` — definir ANTES |
| Rutas API | ANTES de `express.static` para evitar captura |
| Static | DESPUÉS de rutas API |
| Health check | Después de static |
| Start | Siempre último |

## Verificación post-escritura

```bash
# 1. Sintaxis
node --check server.js

# 2. Orden correcto
python3 -c "
with open('server.js') as f:
    content = f.read()
upload_def = content.index('const upload = multer')
route_analyze = content.index(\"app.post('/api/analyze'\")
print('upload before route:', upload_def < route_analyze)
"

# 3. No doble-escape de backslashes
grep -n '\\\\\\\\' server.js  # Si hay resultados, hay doble-escape
```

## Regex: usar indexOf en vez de RegExp

Para patrones simples como limpiar `<think>` tags, usar `indexOf`/`substring` en vez de `new RegExp`:

```javascript
// ❌ Riesgoso con write_file (doble-escape de backslashes)
const thinkRegex = new RegExp('<think>[\\\\s\\\\S]*?</think>', 'g');
clean = clean.replace(thinkRegex, '');

// ✅ Seguro — sin regex, sin escaping
const thinkStart = clean.indexOf('<think>');
const thinkEnd = clean.indexOf('</think>');
if (thinkStart !== -1 && thinkEnd !== -1) {
  clean = clean.substring(0, thinkStart) + clean.substring(thinkEnd + 8);
}
```

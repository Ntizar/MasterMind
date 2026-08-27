# pdf-parse — Compatibilidad v1 vs v2

## v1.1.x (recomendado para este proyecto)

```javascript
const pdfParse = require('pdf-parse');

// En handler Express:
const data = await pdfParse(fileBuffer);
const text = data.text;
```

- Export default es una función
- `data.text` contiene el texto extraído
- `data.numpages`, `data.numrender`, `data.info` también disponibles
- Versión fija: `"pdf-parse": "1.1.4"` en package.json

## v2.x (NO compatible con v1)

```javascript
const { PDFParse } = require('pdf-parse');

// En handler Express:
const parser = new PDFParse({ data: fileBuffer });
const result = await parser.getText();  // { text: "...", ... }
await parser.destroy();
const text = result.text;
```

- NO tiene default export → `require('pdf-parse')` returns `module.exports`
- Clase `PDFParse` se importa con destructuring `{ PDFParse }`
- Constructor recibe `{ data: Buffer }` (objeto, no argumento directo)
- `getText()` retorna `{ text: "...", pages: [...], ... }`
- `destroy()` es obligatorio para liberar recursos
- Más verbose, más pasos, diferente API

## Cómo evitar sorpresas

1. **Fijar versión en package.json:** `"pdf-parse": "1.1.4"` (no `"^1.1.4"`)
2. **Verificar tras install:** `npm list pdf-parse` → debe mostrar `1.1.4`
3. **Si aparece 2.x:** `npm install pdf-parse@1.1.4` explícitamente
4. **Lockfile:** `npm ci` con `package-lock.json` respeta la versión exacta
5. **Test rápido:** Subir un PDF y verificar que el texto se extrae sin errores

## Errores típicos

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError: pdfParse is not a function` | pdf-parse v2 instalado | `npm install pdf-parse@1.1.4` |
| `Cannot destructure property 'text' of undefined` | `data` es undefined porque v2 retorna differently | Verificar API de la versión instalada |
| `PDFParse is not a constructor` | Usando sintaxis v2 con v1 instalado | Revertir a `const pdfParse = require('pdf-parse')` |
| `bad XRef entry` | PDF corrupto o v1.1.1 con bug conocido | Usar v1.1.4, probar con otro PDF |

## Nota sobre `bad XRef entry` en v1.1.1

`pdf-parse@1.1.1` tiene un bug conocido con ciertos PDFs que lanzan `bad XRef entry`. v1.1.4 corrige esto. Siempre usar v1.1.4 o superior (dentro de v1.x).

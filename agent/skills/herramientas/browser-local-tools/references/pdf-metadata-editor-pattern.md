# PDF Metadata Editor — Patrón completo

Visor y editor de metadatos PDF en navegador. Ejemplo real: [VisorMetadatosPDF](https://github.com/Ntizar/VisorMetadatosPDF).

## Stack

| Librería | CDN | Uso |
|----------|-----|-----|
| pdf-lib@1.17.1 | jsdelivr | Leer/escribir Info dict estándar + custom fields |
| pdf.js@3.11.174 | jsdelivr | XMP metadata + page labels + page count |
| JSZip@3.10.1 | jsdelivr | Empaquetar ZIP descargable |

## Arquitectura

```
index.html (autocontenido, ~32KB)
├── CSS inline (Kaizen style)
├── HTML: drop-zone + toolbar + file-list + editor
└── JS: CONFIG → STATE → parser → renderer → export → drag-drop → init
```

## Metadatos extraídos

### Estándar (Info dict, editables)
- `/Title`, `/Author`, `/Subject`, `/Keywords`
- `/CreationDate`, `/ModDate`

### Solo lectura (generados por sistema)
- `/Creator` (app que creó el original)
- `/Producer` (app que generó el PDF)

### Extra
- Campos personalizados del Info dictionary (leer con `info.entries()`, escribir con `info.set(PDFName.of(key), PDFString.of(value))`)
- XMP metadata (Dublin Core, PDF/X, etc.) — solo lectura vía DOMParser+TreeWalker
- Page Labels (i, ii, 1, 2, 3...) — vía `pdfDoc.getPageLabels()`

## Lectura de campos personalizados (Info dict)

```javascript
const infoRef = pdfDoc.context.trailerInfo.Info;
if (infoRef) {
    const info = pdfDoc.context.lookup(infoRef);
    if (info && typeof info.entries === 'function') {
        const stdKeys = new Set(['/Title','/Author','/Subject','/Keywords',
            '/Creator','/Producer','/CreationDate','/ModDate']);
        for (const [k, v] of info.entries()) {
            if (!stdKeys.has(k.value)) {
                customFields[k.value] = pdfObjStr(v);
            }
        }
    }
}
```

## Escritura de campos personalizados

```javascript
const infoRef = pdfDoc.context.trailerInfo.Info;
if (infoRef) {
    const info = pdfDoc.context.lookup(infoRef);
    if (info) {
        for (const [k, v] of Object.entries(customFields)) {
            info.set(PDFLib.PDFName.of(k), PDFLib.PDFString.of(v));
        }
    }
}
```

## UX Pattern: File list + inline editor

1. Drop zone → parse all PDFs → render file list
2. Click file → show editor panel below
3. Edit fields inline → track changes per file
4. Export individual (download PDF) or batch (ZIP)

### Change detection
```javascript
a.tieneCambios = JSON.stringify(a.metadatos.estandar) !== JSON.stringify(a.originales.estandar)
              || JSON.stringify(a.metadatos.personalizados) !== JSON.stringify(a.originales.personalizados);
```

### Reset to original
```javascript
a.metadatos.estandar = { ...a.originales.estandar };
a.metadatos.personalizados = { ...a.originales.personalizados };
a.tieneCambios = false;
```

## Export flow

```javascript
async function aplicarMetadatos(a) {
    const pdfDoc = await PDFLib.PDFDocument.load(a.bytesOrig);
    // Standard fields via setters
    if (m.title) pdfDoc.setTitle(m.title);
    // ... etc
    // Custom fields via Info dict
    const info = pdfDoc.context.lookup(pdfDoc.context.trailerInfo.Info);
    for (const [k, v] of Object.entries(a.metadatos.personalizados)) {
        info.set(PDFLib.PDFName.of(k), PDFLib.PDFString.of(v));
    }
    return await pdfDoc.save({ useObjectStreams: true });
}
```

## Custom Fields CRUD (add/rename/delete)

### Siempre visible: la sección de personalizados

La sección "Campos Personalizados" debe renderizarse SIEMPRE, aunque esté vacía. Incluir botón "+ Añadir campo" visible en todo momento. El usuario crea campos cuando quiera, sin barreras.

```javascript
// ❌ MAL — Solo muestra si ya hay campos
if (Object.keys(metadatos.personalizados).length > 0) {
    renderCustomFields();
}

// ✅ BIEN — Siempre visible con botón de añadir
renderCustomFields(); // Siempre se renderiza
```

### Renombrar campo: pattern data-oldkey + delete + add

pdf-lib NO tiene API para renombrar claves en el Info dictionary. La solución es: borrar la clave vieja + crear la nueva con el mismo valor.

```javascript
function updCampoNombre(key, nuevoNombre, a) {
    const ck = a.metadatos.personalizados;
    const oldVal = ck[key]; // Guardar valor
    const cleanName = nuevoNombre.replace(/[^a-zA-Z0-9_-]/g, ''); // Sanitizar
    
    if (!cleanName) return; // Nombre vacío → ignorar
    if (cleanName === key) return; // Sin cambio
    if (ck.hasOwnProperty(cleanName)) {
        alert('Ya existe un campo con ese nombre');
        return; // Duplicado → revertir
    }
    
    delete ck[key];    // Borrar viejo
    ck[cleanName] = oldVal; // Crear nuevo
    // Actualizar data-oldkey en el DOM sin re-renderizar editor
    el.setAttribute('data-oldkey', cleanName);
}
```

### CRUD functions pattern

```javascript
function addCampoCustom(a) {
    let n = 1;
    while (a.metadatos.personalizados.hasOwnProperty('campo_' + n)) n++;
    a.metadatos.personalizados['campo_' + n] = '';
    renderLista(a); renderToolbar(a);
    // Auto-focus en el input del nuevo campo
    setTimeout(() => {
        const input = document.querySelector(`input[data-key="campo_${n}"]`);
        if (input) { input.focus(); input.select(); }
    }, 50);
}

function removeCampoCustom(key, a) {
    delete a.metadatos.personalizados[key];
    renderLista(a); renderToolbar(a);
}
```

### UI: nombre editable con input en vez de label

En lugar de `<label>` estático para el nombre del campo, usar `<input>` para que sea editable inline:

```html
<div class="custom-field-row">
    <input class="field-name-input" data-oldkey="campo_1" 
           value="campo_1" oninput="updCampoNombre(...)">
    <input class="field-value" data-key="campo_1" value="...">
    <button class="btn-del" onclick="removeCampoCustom(...)">✕</button>
</div>
```

### Pitfall: NO re-renderizar editor al renombrar

Cuando el usuario está editando un nombre de campo y hace `oninput`, NO re-renderizar el editor completo porque se pierde el foco del input. Solo re-renderizar la lista y la toolbar:

```javascript
function updCampoNombre(key, newName, a) {
    // ... rename logic ...
    renderLista(a);   // ✅ Actualiza badges, detección cambios
    renderToolbar(a); // ✅ Actualiza botones
    // ❌ NO llamar renderEditor(a) — pierde el foco del input
}
```

### Change detection con campos personalizados

```javascript
a.tieneCambios = JSON.stringify(a.metadatos.estandar) !== JSON.stringify(a.originales.estandar)
              || JSON.stringify(a.metadatos.personalizados) !== JSON.stringify(a.originales.personalizados);
```

## Pitfalls

- **pdf-lib load options:** Usar `{ ignoreEncryption: true }` para PDFs que solo tienen metadatos protegidos
- **pdf.js worker:** Siempre `workerSrc = ''` para compatibilidad con `file://`
- **pdf-lib save re-encode:** El PDF se re-encode completo. Contenido preservado, firmas perdidas
- **XMP editing:** pdf-lib NO escribe XMP. Solo Info dict. Para XMP se necesita manipulación XML directa
- **PDFs > 50MB:** Pueden congelar el navegador. Mostrar aviso
- **Duplicate files:** Detectar por nombre de archivo, no por contenido

## Referencia

- Repo: https://github.com/Ntizar/VisorMetadatosPDF
- Pages: https://ntizar.github.io/VisorMetadatosPDF/
- Código fuente: `index.html` (autocontenido, 32KB)

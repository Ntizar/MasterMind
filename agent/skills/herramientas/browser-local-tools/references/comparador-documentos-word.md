# Referencia: Comparador de Documentos Word vs Word

## Caso de uso
David necesita comparar documentos Word legales (adendas, contratos) en masa.
Originalmente eran Word vs PDF, pero pdf.js falla con Acrobat PDFMaker.

## Solución implementada

### Paso 1: Convertir PDFs a Word
`convertir_pdfs_a_word.bat` — usa LibreOffice headless para convertir PDFs a .docx
```bat
for %%f in (*.pdf) do "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to docx "%%f"
```

### Paso 2: Comparar Word vs Word
`comparar_docs.html` — HTML autocontenido con mammoth.js embebido (~649 KB total)

## Detalles técnicos
- **mammoth.js** embebido inline (626 KB) — descargado de cdnjs, pegado dentro del `<script>`
- **Comparación:** diff por palabras (algoritmo LCS), NO diff carácter a carácter
- **Filtrado de ruido:** URLs, sellos CVE, headers de página, firmas, separadores
- **Similarity %:** muestra porcentaje de similitud (✅/🟡/🟠/🔴)
- **Diferencias legibles:** frases agrupadas ("Lo que AÑADE/ELIMINA el Doc B")

## Evolución del algoritmo (importante)

### v1: Diff carácter a carácter (MAL)
Comparaba texto normalizado sin espacios, carácter por carácter.
Resultado: bloques ilegibles como `...ciontransformacionyresilienciaporlacomunida...`
**El usuario se frustró:** "así no se que puede ser lo que es distinto"

### v2: Diff por palabras con LCS (BIEN)
1. Eliminar ruido (URLs, CVE, headers)
2. Convertir texto a array de palabras (sin tildes, sin puntuación)
3. Algoritmo LCS (Longest Common Subsequence) entre arrays de palabras
4. Agrupar cambios consecutivos en frases
5. Mostrar como "➕ Lo que AÑADE" / "❌ Lo que ELIMINA"

**Lección:** Siempre comparar por palabras para documentos de texto. El diff carácter a carácter solo sirve para código o datos estructurados.

## Ruido específico de documentos certificados (Xunta de Galicia)
Los documentos Word certificados electrónicamente tienen estos artefactos:
- **Sello CVE:** `[As copias en papel deste documento teñen a condició](https://sede.xunta.gal/cve?idcve=...)`
- **URL de verificación:** `https://sede.xunta.gal/cve?idcve=hsBta0M3hZR1`
- **Texto:** "As copias en papel deste documento teñen a condición de copia e serán verificables a través deste código"
- Aparecen como hipervínculos en Word → mammoth.js los extrae como texto con formato markdown `[texto](url)`

## Pitfalls descubiertos
1. **CDN no funciona al compartir** → siempre embeber libs
2. **pdf.js no extrae texto de PDFs Acrobat PDFMaker** → convertir a Word primero
3. **pdf.js Worker falla desde file://** → deshabilitar worker con `workerSrc = ''`
4. **Diff carácter a字符 es inútil para documentos** → siempre usar diff por palabras (LCS)
5. **Los documentos Word certificados tienen ruido CVE** → filtrar URLs y sellos antes de comparar

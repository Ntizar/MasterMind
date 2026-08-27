# Extracción de Colores desde Manual de Marca PDF

## Caso de uso
Una empresa tiene su manual de marca en PDF y necesitamos los colores oficiales (HEX, RGB, CMYK, Pantone) para crear un design system.

## Herramientas disponibles

| Herramienta | Disponible | Notas |
|------------|-----------|-------|
| `pdftotext` (poppler-utils) | ✅ pero puede fallar | Requiere `libpoppler.so` — a veces falta |
| PyMuPDF (`fitz`) | ✅ via venv | `/opt/hermes/.venv/bin/python3` tiene fitz |
| `mutool` (mupdf-tools) | ❌ binary missing | Package instalado pero binario no disponible |
| `strings` + grep | ✅ siempre | Funciona pero extrae poco texto |
| Browser PDF viewer | ✅ siempre | Sirve para navegar pero no para extraer texto |

## Flujo recomendado

### 1. Intentar pdftotext primero (rápido)
```bash
pdftotext manual-marca.pdf - 2>/dev/null | grep -i -E "pantone|rgb|hex|cmyk"
```

### 2. Fallback: PyMuPDF via venv (más robusto)
```bash
/opt/hermes/.venv/bin/python3 -c "
import fitz, json
doc = fitz.open('manual-marca.pdf')
results = []
for i, page in enumerate(doc):
    text = page.get_text()
    for line in text.split('\n'):
        line_lower = line.lower().strip()
        if any(k in line_lower for k in ['pantone', 'rgb', 'hex', 'cmyk', 'color', '#']):
            results.append({'page': i+1, 'text': line.strip()})
    # También extraer fills de dibujos vectoriales
    drawings = page.get_drawings()
    for d in drawings:
        for item in d.get('items', []):
            if item[0] == 'f':  # fill
                color = item[1]
                if color and color != (1, 1, 1):  # skip blanco
                    r, g, b = [int(c*255) for c in color[:3]]
                    hex_color = f'#{r:02x}{g:02x}{b:02x}'
                    results.append({'page': i+1, 'type': 'vector_fill', 'rgb': f'({r},{g},{b})', 'hex': hex_color})
json.dump(results, open('/tmp/color-results.json', 'w'), indent=2, ensure_ascii=False)
print(json.dumps(results, indent=2))
"
```

### 3. Renderizar páginas + vision_analyze (si el PDF es imagen)
```bash
/opt/hermes/.venv/bin/python3 -c "
import fitz
doc = fitz.open('manual-marca.pdf')
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    pix.save(f'/tmp/page_{i+1}.png')
    print(f'Guardado /tmp/page_{i+1}.png')
"
# Luego usar vision_analyze en cada imagen
```

### 4. delegate_task para análisis complejo
Si el PDF es largo o tiene múltiples secciones, delegar a un subagente que pueda iterar sin saturar el contexto principal.

## Ejemplo real: Ineco

- **PDF:** `INECO_MANUAL_de_MARCA.pdf` (754KB, 1 página muy larga verticalmente)
- **Problema:** `pdftotext` falló (missing `libpoppler.so.147`), `mutool` no disponible
- **Solución:** delegate_task con PyMuPDF via venv
- **Resultado:** 4 colores oficiales extraídos + 4 secundarios de fills vectoriales

### Colores extraídos
| Color | HEX | Pantone | CMYK |
|-------|-----|---------|------|
| Azul Ineco | #1A4488 | 7687 C | C:99 M:78 Y:14 K:2 |
| Rojo Ineco | #CB1823 | 485 C | C:13 M:99 Y:90 K:3 |
| Azul Medio | #3463AC | — | — |
| Azul Claro | #6B96CF | — | — |

### Secundarios (fills vectoriales, sin etiquetas de texto)
| Color | HEX |
|-------|-----|
| Rojo fondo | #CE2230 |
| Azul fondo | #3069B2 |
| Azul claro fondo | #6292CC |
| Gris | #6F7373 |

## Pitfalls

1. **PyMuPDF no está en system Python** — usar `/opt/hermes/.venv/bin/python3`
2. **PDFs escaneados** — `get_text()` devuelve vacío. Renderizar a PNG + vision_analyze
3. **PDFs con fuentes embebidas** — texto extraído puede tener caracteres raros. Usar OCR como fallback
4. **Fills vectoriales vs texto** — los colores en fills pueden no coincidir con los valores RGB del texto (diferente color space). El texto del manual es la fuente de verdad
5. **read_file() de Hermes** — devuelve contenido CON números de línea. NUNCA usar para copiar CSS/HTML. Usar `open().read()` en Python directamente

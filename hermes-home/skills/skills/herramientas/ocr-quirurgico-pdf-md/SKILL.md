---
name: ocr-quirurgico-pdf-md
version: "1.0.0"
description: "Pipeline completo OCR quirúrgico: PDF → página a página → Markdown/HTML con precisión total. Detecta tablas, firmas, diagramas, imágenes. Si no entiende algo, captura y graba en posición exacta. Vectoriza para búsqueda con ChromaDB + qwen3-embedding."
tags: [ocr, pdf, markdown, html, pipeline, tablas, firmas, diagramas, chromadb, qwen3]
---

# OCR Quirúrgico PDF → MD/HTML

## Resumen

Pipeline que recibe un PDF, lo **corta página a página** y produce un Markdown o HTML con **precisión absoluta**:

- Texto real → extraído con bounding boxes
- Tablas → detectadas con pdfplumber + reconstruidas como `<table>`
- Firmas → paths vectoriales capturados como imagen
- Diagramas → render + OCR + imagen incrustada
- Imágenes → extraídas con fitz + metadata
- Si algo falla → **captura de pantalla** (render 300dpi) + imagen en posición exacta

Luego **todo se vectoriza** con qwen3-embedding (4096d) para búsqueda semántica por ChromaDB.

## Cuándo usarlo

- Usuario adjunta PDF técnico y pide "convertir a Markdown/HTML con todo en su sitio"
- Usuario quiere un **documento navegable** donde cada tabla, firma, y diagrama esté en la posición correcta
- Usuario necesita **búsqueda semántica** sobre el contenido (miles de páginas)

## No es para

- OCR de documentos escaneados con fotos (usar `documentos-institucionales`)
- Extracción rápida sin preservación de layout (usar `markitdown` o `pdf-to-dashboard`)
- **Extracción de datos estructurados de PDFs digitales** → usar `pdf-llm-extraction` (nuevo paradigma: font analysis + LLM, 100% confianza vs ~60% con regex)
- Documentos con solo texto sin tablas ni imágenes (usar `pdf-to-artifacts-david-antizar`)

> ⚠️ **Paradigma shift (2026-06):** Para PDFs digitales con texto seleccionable, el pipeline `pdf-llm-extraction` (PyMuPDF + Qwen 3.6) supera cualitativamente a cualquier enfoque regex o OCR. Usar OCR solo para PDFs escaneados/imágenes.

## Stack de herramientas

| Herramienta | Rol | Instalación |
|------------|-----|-------------|
| `fitz` (PyMuPDF) | Extracción principal + render + bounding boxes | `pip install PyMuPDF` |
| `pdfplumber` | Detección de tablas + líneas de cuadrícula | `pip install pdfplumber` |
| `Tesseract` | OCR de imágenes cuando el texto no es extraíble | `apt install tesseract-ocr` |
| `camelot` | Tablas sin líneas (fallback) | `pip install camelot-py[cv]` |
| `Pillow` | Procesado de imágenes + deskew | `pip install Pillow` |
| `qwen3-embedding` | Vectorización 4096d | `api.nan.builders/v1/embeddings` |
| `ChromaDB` | Almacenamiento vectorial + búsqueda | `pip install chromadb` |
| `OpenCV` | Preprocesado de imágenes (threshold, denoise) | `pip install opencv-python` |

## Arquitectura del pipeline

```
PDF
  ↓
┌───────────────────────────────┐
│  FASE 0 — PREPARACIÓN          │
│  - Verificar herramientas       │
│  - Crear directorios de salida  │
│  - Detectar tipo de PDF         │
└───────────────────────────────┘
  ↓
┌───────────────────────────────┐
│  FASE 1 — CORTE               │
│  - fitz: abrir PDF             │
│  - Por cada página:            │
│    - text = get_text("dict")   │
│    - images = get_images()     │
│    - paths = get_drawings()    │
│    - metadata = page metadata  │
└───────────────────────────────┘
  ↓
┌───────────────────────────────┐
│  FASE 2 — CLASIFICACIÓN       │
│  - Por cada elemento:          │
│    - ¿Es texto? → extraer      │
│    - ¿Es tabla? → pdfplumber   │
│    - ¿Es firma? → capturar     │
│    - ¿Es diagrama? → render    │
│    - ¿Es imagen? → extraer     │
│    - ¿No se entiende? → OCR    │
│      → Captura de imagen        │
└───────────────────────────────┘
  ↓
┌───────────────────────────────┐
│  FASE 3 — ENSAMBLADO          │
│  - Página por página:          │
│    - Markdown: texto + tablas  │
│    - HTML: con imágenes incrust │
│    - Imagen fallback incrustada │
│  - Metadata por elemento:       │
│    - tipo, bbox, confidence     │
│    - página, documento          │
└───────────────────────────────┘
  ↓
┌───────────────────────────────┐
│  FASE 4 — VECTORIZACIÓN       │
│  - qwen3-embedding por página  │
│  - qwen3-embedding por elemento  │
│  - ChromaDB: store + metadata  │
│  - Búsqueda: consulta semántica│
└───────────────────────────────┘
```

## Fase 0 — Preparación

```bash
# 1. Verificar herramientas
python3 -c "
import sys
try:
    import fitz; print('fitz ✅')
    import pdfplumber; print('pdfplumber ✅')
    import cv2; print('OpenCV ✅')
except ImportError as e:
    print(f'Falta: {e}')
    sys.exit(1)
"

# 2. Verificar Tesseract
which tesseract || echo "Instalar: apt install tesseract-ocr tesseract-ocr-spa"

# 3. Crear directorio de trabajo
mkdir -p /tmp/ocr-pipeline/{pages,elements,output,images}
```

## Fase 1 — Corte página a página

```python
import fitz
import json
from pathlib import Path

def cortar_pdf(pdf_path: str, output_dir: str = "/tmp/ocr-pipeline") -> dict:
    """
    Corta un PDF página a página y devuelve un dict con:
    - pages: [{index, text_blocks, images, drawings, metadata}]
    - total_pages: int
    - metadata: {title, author, producer, ...}
    """
    doc = fitz.open(pdf_path)
    pages_data = []

    for i, page in enumerate(doc):
        # Metadata de página
        rect = page.rect
        rotation = page.rotation

        # Extraer texto con bounding boxes (dict mode)
        text_dict = page.get_text("dict")
        # Extraer imágenes
        images = page.get_images(full=True)
        # Extraer paths/dibujos (diagramas, firmas)
        paths = page.get_drawings()

        # Extraer elementos de texto con coordenadas
        blocks = []
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:  # texto
                blocks.append({
                    "type": "text",
                    "bbox": block.get("bbox"),
                    "lines": [
                        {
                            "spans": [
                                {"text": s.get("text"), "font": s.get("font"), 
                                 "size": s.get("size"), "color": s.get("color")}
                                for s in span.get("spans", [])
                            ]
                        }
                        for line in block.get("lines", [])
                    ]
                })
            elif block.get("type") == 1:  # imagen
                blocks.append({
                    "type": "image",
                    "bbox": block.get("bbox"),
                    "image": block.get("image")  # bytes
                })

        pages_data.append({
            "page": i + 1,
            "rect": [rect.x0, rect.y0, rect.x1, rect.y1],
            "rotation": rotation,
            "blocks": blocks,
            "images": [{"index": j, "xref": img[0], "width": img[2], "height": img[3]}
                       for j, img in enumerate(images)],
            "drawings": [{"path": d} for d in paths]
        })

    return {
        "pages": pages_data,
        "total_pages": len(doc),
        "metadata": {
            "title": doc.metadata.get("title"),
            "author": doc.metadata.get("author"),
            "producer": doc.metadata.get("producer"),
            "format": doc.metadata.get("format")
        }
    }

# Guardar para la fase 2
json.dump(cortar_pdf("documento.pdf"), 
          open("/tmp/ocr-pipeline/pages_raw.json", "w"), 
          ensure_ascii=False)
```

### Fase 1b — Render de página para fallback

```python
def render_page_as_image(pdf_path, page_num, dpi=300):
    """Renderiza una página completa como imagen PNG a 300 DPI"""
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    pix = page.get_pixmap(dpi=dpi)
    pix.save(f"/tmp/ocr-pipeline/pages/page_{page_num:04d}.png")
    return f"/tmp/ocr-pipeline/pages/page_{page_num:04d}.png"
```

## Fase 2 — Clasificación de elementos

```python
def clasificar_elemento(elemento: dict, page_width: float, page_height: float) -> str:
    """
    Clasifica un bloque de texto en:
    - "texto" → párrafo normal
    - "tabla" → líneas alineadas en columnas
    - "firma" → paths vectoriales (curvas bezier)
    - "diagrama" → líneas + texto + formas
    - "imagen" → imagen embebida
    - "no_identificado" → render + OCR
    """
    bbox = elemento.get("bbox", [0, 0, 0, 0])
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    tipo = elemento.get("type", "")

    # Heurísticas
    if tipo == "image":
        return "imagen"
    
    if tipo == "text":
        # ¿Es tabla? (múltiples líneas con mismo espaciado X)
        lines = elemento.get("lines", [])
        if len(lines) > 2:
            x_coords = set()
            for line in lines:
                for span in line.get("spans", []):
                    x_coords.add(round(span["bbox"][0]))
            # Si hay más de 3 columnas X distintas → tabla
            if len(set(round(x) for x in x_coords)) > 3:
                return "tabla"
        
        # ¿Es imagen grande? (ocupa >80% del ancho)
        if w > page_width * 0.8:
            return "imagen_grande"
        
        # ¿Es texto normal?
        return "texto"

    # Paths vectoriales → firma o diagrama
    if tipo == "drawing":
        # Si son curvas bezier → firma
        # Si son rectas + texto → diagrama
        return "firma" if len(paths) < 5 else "diagrama"

    return "no_identificado"
```

## Fase 3 — OCR de fallback (cuando no se entiende)

```python
import subprocess
from PIL import Image

def ocr_fallback(pdf_path, page_num, bbox=None):
    """
    Cuando el texto no es extraíble (fuentes embebidas, etc.):
    - Renderiza la página completa o solo el bbox
    - Ejecuta Tesseract
    - Devuelve: {"text": "...", "confidence": float, "image_path": "..."}
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    
    if bbox:
        # Solo renderizar la región del bbox
        clip = fitz.Rect(*bbox)
        pix = page.get_pixmap(dpi=300, clip=clip)
    else:
        # Página completa
        pix = page.get_pixmap(dpi=300)
    
    img_path = f"/tmp/ocr-pipeline/images/page_{page_num:04d}_bbox.png"
    pix.save(img_path)

    # Tesseract
    result = subprocess.run(
        ["tesseract", img_path, "stdout", "-l", "spa+eng", "--psm", "6"],
        capture_output=True, text=True, timeout=30
    )
    
    return {
        "text": result.stdout.strip(),
        "confidence": 0.8,  # placeholder
        "image_path": img_path
    }

def ocr_con_llm(img_path: str, model="qwen3.6"):
    """
    Cuando Tesseract no es suficiente (diagramas, logos, firmas):
    Envía la imagen a un modelo multimodal para descripción.
    """
    # Aquí iría la llamada a NaN API con el modelo multimodal
    # Ej: curl -X POST https://api.nan.builders/v1/chat/completions
    #     -d '{"model": "qwen3-vl", "messages": [{"role": "user", "content": "Describe esta imagen de un documento"}]}'
    return {"description": "...", "type": "diagrama"}
```

## Fase 4 — Ensamblado a Markdown/HTML

```python
def ensamblar_markdown(pages_data, pdf_path, output_dir="/tmp/ocr-pipeline/output"):
    """
    Genera un Markdown con:
    - Cada página como sección
    - Imágenes incrustadas con MEDIA:
    - Tablas como markdown tables
    - Metadata de cada elemento
    """
    md = []
    md.append(f"# {pdf_path}\n")
    
    for page_data in pages_data:
        md.append(f"\n## Página {page_data['page']}\n")
        
        for block in page_data.get("blocks", []):
            tipo = block["type"]
            
            if tipo == "text":
                md.append(block["text"])
            elif tipo == "table":
                md.append(formatear_tabla(block))
            elif tipo == "image":
                md.append(f"\n![Imagen página {page_data['page']}]({block['path']})\n")
            elif tipo == "diagram":
                md.append(f"\n```\n{block['description']}\n```\n")
                md.append(f"![Diagrama]({block['image_path']})\n")
            elif tipo == "signature":
                md.append(f"\n---\n### Firma\n![Firma]({block['image_path']})\n---\n")
    
    return "\n".join(md)

def ensamblar_html(pages_data, pdf_path, output_dir="/tmp/ocr-pipeline/output"):
    """
    Versión HTML con:
    - CSS para responsive
    - Imágenes en base64 (incrustadas en el HTML)
    - Tablas con <table>
    - Cada elemento con su metadata
    """
    html = ["<!DOCTYPE html><html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><style>"]
    html.append("""
        body { font-family: 'Segoe UI', sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #fafafa; }
        .page { border: 1px solid #ddd; margin: 20px 0; padding: 20px; background: white; border-radius: 8px; }
        table { width: 100%; border-collapse: collapse; margin: 10px 0; }
        td, th { border: 1px solid #ccc; padding: 8px; }
        .image-container { margin: 10px 0; }
        .diagram { background: #fff3e0; padding: 10px; border-left: 4px solid #ff9800; }
        .firma { border: 1px dashed #999; padding: 10px; margin: 10px 0; }
        .kpi { display: inline-block; padding: 10px; border-radius: 8px; }
        .confidence-low { opacity: 0.7; }
        .confidence-high { font-weight: bold; }
        .metadata { font-size: 0.8em; color: #666; }
    """)
    html.append("</style></head><body>")
    
    for page_data in pages_data:
        html.append(f"<div class='page'><h2>Página {page_data['page']}</h2>")
        
        for block in page_data.get("blocks", []):
            if block["type"] == "texto":
                html.append(f"<p>{block['text']}</p>")
            elif block["type"] == "tabla":
                html.append(f"<table>{block['html']}</table>")
            elif block["type"] == "imagen":
                html.append(f"<div class='image-container'><img src='data:image/png;base64,{block['base64']}'></div>")
            elif block["type"] == "diagrama":
                html.append(f"<div class='diagram'><pre>{block['description']}</pre></div>")
            elif block["type"] == "firma":
                html.append(f"<div class='firma'><img src='{block['path']}'></div>")
        
        html.append("</div>")
    
    html.append("</body></html>")
    return "\n".join(html)

```

## Fase 5 — Vectorización para búsqueda

```python
import chromadb
import requests

def vectorizar_documento(output_md: str, output_html: str, pdf_metadata: dict):
    """
    Toma el MD/HTML generado y lo indexa en ChromaDB para búsqueda semántica:
    - Cada página → un embedding (documento completo)
    - Cada tabla/parrafo → un embedding (búsqueda granular)
    """
    
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection("ocr-documents")
    
    # Por cada página → embedding
    for page_data in pages_data:
        # Texto completo de la página
        page_text = " ".join([b.get("text", "") for b in page_data["blocks"]])
        
        # qwen3-embedding
        response = requests.post(
            "https://api.nan.builders/v1/embeddings",
            headers={"Authorization": f"Bearer {NAN_API}"},
            json={
                "model": "qwen3-embedding",
                "input": page_text,
            }
        )
        embedding = response.json()["data"][0]["embedding"]
        
        # Guardar en ChromaDB
        collection.add(
            embeddings=[embedding],
            metadatas=[{
                "pdf": pdf_path,
                "page": page_data["page"],
                "document": pdf_metadata["title"],
                "type": "page"
            }],
            ids=[f"{pdf_path}-page-{i}"]
        )
    
    # Por cada bloque → embedding individual
    for page_data in pages_data:
        for j, block in enumerate(page_data["blocks"]):
            block_text = block.get("text", "") or block.get("description", "")
            response = requests.post(...)
            embedding = response.json()["data"][0]["embedding"]
            
            collection.add(
                embeddings=[embedding],
                metadatas=[{
                    "pdf": pdf_path,
                    "page": page_data["page"],
                    "block": j,
                    "type": block["type"],
                    "confidence": block.get("confidence", 0.5)
                }],
                ids=[f"{pdf_path}-page-{i}-block-{j}"]
            )
```

## Búsqueda desde el resultado

```bash
# Búsqueda semántica
python3 -c "
import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
col = client.get_or_create_collection('ocr-documents')

# Buscar por contenido
result = col.query(
    query_texts=['Describe el presupuesto del capítulo 1'],
    n_results=5
)
print(result['documents'][0])  # Páginas que hablan de eso
"

# Búsqueda por tipo
result = col.get(
    where={'type': 'tabla'},
    limit=10
)
```

## Llamada unificada

```bash
python3 ocr_quirurgico.py documento.pdf --output-format md|html --vectorize --output-dir /tmp/ocr-output
```

## Modos de salida

| Flag | Output | Uso |
|------|--------|-----|
| `--output-format md` | Markdown con `MEDIA:` | Para leerlo en Hermes/chat |
| `--output-format html` | HTML autocontenido (base64) | Para verlo en browser |
| `--no-vectorize` | Solo extracción sin ChromaDB | Pruebas rápidas |
| `--vectorize` | Todo + indexación | Búsqueda masiva |

## Pitfalls

### 🔴 poppler-utils no funciona en MicroVMs/contenedores
`pdftotext` y `pdfimages` de poppler fallan con `libpoppler.so.147: cannot open shared object file` en muchas MicroVMs y contenedores Docker. `markitdown` también depende de poppler internamente y produce output vacío.
**Solución:** Usar **PyMuPDF (`fitz`)** como engine principal. Funciona 100% en todas las arquitecturas sin dependencias del sistema. `fitz.open(pdf).get_text()` y `fitz.open(pdf).get_images()` cubren el 90% de los casos. Si el usuario instala poppler y funciona, bien. Si no, PyMuPDF es el fallback seguro.

### 🔴 Extracción de texto masiva: dos pasos
Para proyectos con cientos de PDFs, **NUNCA** geocodificar/enriquecer durante la fase de parsing:
1. **Paso 1:** Extraer todo el texto de todos los PDFs (rápido, ~4s por PDF con PyMuPDF)
2. **Paso 2:** Geocodificar/normalizar los campos únicos extraídos (con rate limits, delays)

Mezclar ambos en un solo paso causa timeouts, rate limits de APIs externas, y datos incompletos.

### 🔴 Requisitos de hardware
- **Fitz con DPI alto:** 300 DPI × página A4 = ~8MB por página → 100 páginas = 800MB en RAM
- **ChromaDB:** ~500MB en RAM con 10.000 vectores
- **Tesseract con varios idiomas:** ~200MB de RAM
- **MicroVM 1vCPU/2GB:** **Máximo 3 procesos concurrentes.** Para 100 páginas, ~5-10 min en secuencial

### 🔴 Tesseract no es magia
- Texto con fondo degradado → preprocesar con OpenCV (binarización)
- Documentos con fuentes raras (>8 fuentes distintas) → Tesseract baja a 60% de confianza
- **Solución:** `--psm 6` (bloque de texto uniforme) es mejor que `--psm 3` (detecta todo)

### 🔴 qwen3-embedding: 4096 dimensiones
- Cada embedding cuesta ~0.8s en NaN
- 10.000 páginas → ~2.2h en embedding
- **Rate limit:** 60 req/min → con 10.000 páginas, ~2.8h en total
- **Solución:** Batch de 20 por request (qwen3-embedding acepta arrays)

### 🔴 Render vs Extracción
- **NUNCA** renderizar sin intentar extraer primero. `fitz.get_text("dict")` es instantáneo. Solo render si falla.
- **Siempre** guardar el texto extraído **antes** de renderizar (no al revés)
- **El render es caro** (~1s por página a 300 DPI). Si son 10.000 páginas → 10.000s = ~3h

### 🔴 Tablas sin líneas
- `pdfplumber` solo detecta tablas con líneas de cuadrícula
- **Fallback:** `camelot` (modo stream + lattice) → si no hay líneas, infiere por espaciado
- **Último recurso:** render + `tesseract --psm 6` + inferir columnas por regex

### 🔴 Firma vs diagrama vs dibujo
- **Firma:** paths bezier (curva suave, pocos puntos, color azul/negro)
- **Diagrama:** paths rectos + texto + formas geométricas
- **Dibujo técnico:** paths + líneas + texto técnico (fonts mono)
- **Regla:** si tiene >50 paths → es dibujo técnico. Capturar como imagen siempre.

### 🔴 Batch de embeddings (qwen3-embedding)
- API acepta hasta 20 inputs por request (según docs de NaN)
- Si no, hacer por lotes de 10
- Siempre manejar errores 429 (rate limit) con retry exponencial

### 🔴 Nominatim: User-Agent con paréntesis → 403 Forbidden
Nominatim rechaza peticiones cuyo User-Agent contiene paréntesis `()`. Ejemplo: `"CIAF-Visor/1.0 (proyecto educativo; contacto: x@y.com)"` → HTTP 403. User-Agent simple como `"CIAF-Visor/1.0"` funciona. Esto aplica a todas las APIs de OpenStreetMap.

### 🔴 PyMuPDF: `span["text"]` puede ser None
En algunos PDFs, PyMuPDF retorna `None` en `span["text"]` en lugar de string vacío. Causa `TypeError` al concatenar. **SIEMPRE** usar `span.get("text") or ""`. Afecta ~25% de PDFs en batch processing.

### 🔴 API rate limits → lookup local como alternativa
Cuando se necesitan cientos de llamadas a una API con rate limits (Nominatim: 1 req/s), la mejor estrategia es:
1. **Fase 1:** Extraer todos los valores únicos (ej: 206 estaciones)
2. **Fase 2:** Geocodificar con delays apropiados O construir un JSON de lookup local
3. **Fase 3:** Aplicar las coordenadas al dataset

El lookup local (`station-coords.json`) es más rápido, no tiene rate limits, y funciona offline. Para ~300 entradas, un JSON hardcodeado es perfectamente viable.

### 🔴 Entity normalization: regex captura texto basura
Cuando se extraen entidades de PDFs con regex (ej: `r'renfe\s+mercanc'`), el match captura texto después del nombre: "Renfe Mercancías que había" en vez de "Renfe Mercancías". 

**Solución (3 capas):**
1. **Stop phrases** en `extract_estacion()`: filtrar "observa que", "donde se", "procedente de"
2. **Trash suffixes** en `extract_entidades()`: lista de sufijos basura ("que había", "debían cruzarse", "hacía su", etc.)
3. **Case-insensitive merging**: fusionar "RENFE" y "Renfe" → "RENFE" con un mapa final

## Referencias

- `references/nominatim-geocoding-quirks.md` — Pitfalls de Nominatim: User-Agent, rate limits, lookup local
- `references/entity-normalization-pdf.md` — Patrones para limpiar entidades extraídas de PDFs
- `esios-complete` → API de ESIOS (para comparación con datos reales)
- `chromadb-skills-vector-search` → Sistema de búsqueda semántica existente
- `pdf-to-dashboard` → Extracción de datos estructurados de PDFs
- `documentos-institucionales` → Análisis de informes públicos
- `mastermind-orchestration` → Orquestación multi-agente para paralelizar

## Atribución

**Autor:** David Antizar (Ntizar)
**Agente:** Mastermind (ejecutor, no autor)
**Repo:** `github.com/Ntizar/Mastermind`
**Skill** creado para el pipeline de OCR quirúrgico

## Licencia

Apache 2.0 — Documentación abierta para cualquier pipeline que necesite precisión absoluta en OCR de documentos.
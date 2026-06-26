# Microsoft Markitdown

**URL:** https://github.com/microsoft/markitdown
**Categoría:** Listas/Colecciones / Herramientas
**Estrellas:** 125,333
**Lenguaje:** Python

## ¿Qué hace?
MarkItDown es una utilidad ligera de Python que convierte **más de 20 tipos de archivos** a Markdown para alimentar LLMs y pipelines de análisis de texto. Soporta PDFs, Word (DOCX), Excel (XLSX/XLS), PowerPoint (PPTX), imágenes (EXIF + OCR vía LLM), audio (transcripción), HTML, YouTube, EPUBs, ZIP, CSV, JSON, XML, Jupyter Notebooks, mensajes de Outlook y más. Usa `magika` para detección automática de formato y prioriza conversores por tipo de archivo. Es comparable a `textract` pero con foco en preservar estructura (encabezados, listas, tablas, enlaces) como Markdown, optimizado para consumo por LLMs (token-efficient).

## Casos de uso
1. **Ingesta de documentos en RAG:** Convertir PDFs, Word y Excel a Markdown para cargar en un vector store y alimentar un pipeline RAG con LLMs.
2. **Extracción de transcripciones de YouTube:** Obtener título, descripción y transcripción completa de videos de YouTube en un solo paso.
3. **Procesamiento de imágenes con LLM Vision:** Extraer metadatos EXIF y generar descripciones de imágenes usando GPT-4o u otros clientes OpenAI compatibles.
4. **Transcripción de audio:** Convertir archivos WAV/MP3 a texto usando SpeechRecognition + PyDub.
5. **Azure Cloud Integration:** Usar Azure Document Intelligence o Azure Content Understanding para conversión de alta calidad con campos estructurados (YAML front matter) y análisis multimodal.
6. **CLI rápido:** Pipeline de shell `cat archivo.pdf | markitdown > salida.md` para conversión ad-hoc sin código.
7. **Plugins de terceros:** Extender con formatos personalizados (ej. RTF, OCR con LLM) usando el sistema de plugins basado en entry points.

## Snippets útiles

### Conversión básica de archivos locales
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("documento.pdf")
print(result.markdown)  # o result.text_content (alias deprecated)
```

### Conversión con LLM para descripciones de imágenes
```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="Describe esta imagen en español de forma detallada."
)
result = md.convert("foto.jpg")
print(result.markdown)
```

### Conversión de URL remota
```python
from markitdown import MarkItDown

md = MarkItDown()
# Soporta http, https, file:, data: URIs
result = md.convert("https://ejemplo.com/documento.pdf")
print(result.markdown)
```

### Conversión de stream (bytes en memoria)
```python
import requests
from markitdown import MarkItDown

response = requests.get("https://ejemplo.com/archivo.xlsx")
md = MarkItDown()
result = md.convert(response)  # acepta requests.Response directamente
print(result.markdown)
```

### Conversión segura con API estrecha (security best practice)
```python
from markitdown import MarkItDown

md = MarkItDown()
# convert_local() solo acepta archivos locales — más seguro que convert()
result = md.convert_local("/ruta/segura/documento.docx")
print(result.markdown)
```

### Conversión desde stdin (pipe)
```python
import sys
from markitdown import MarkItDown, StreamInfo

md = MarkItDown()
result = md.convert_stream(
    sys.stdin.buffer,
    stream_info=StreamInfo(extension=".pdf")  # hint para pipe
)
print(result.markdown)
```

### Azure Document Intelligence
```python
from markitdown import MarkItDown

md = MarkItDown(
    docintel_endpoint="https://<tu-recurso>.cognitiveservices.azure.com/"
)
result = md.convert("factura.pdf")
print(result.markdown)
```

### Azure Content Understanding (campos estructurados)
```python
from markitdown import MarkItDown

md = MarkItDown(
    cu_endpoint="https://<tu-recurso>.cognitiveservices.azure.com/",
    cu_analyzer_id="mi-analizador-facturas"
)
result = md.convert("factura.pdf")
# El output incluye YAML front matter con campos extraídos:
# ---
# contentType: document
# fields:
#   VendorName: CONTOSO LTD.
#   InvoiceDate: '2019-11-15'
# ---
print(result.markdown)
```

### Conversión de YouTube (título + descripción + transcripción)
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("https://www.youtube.com/watch?v=VIDEO_ID")
print(result.markdown)
# Incluye: título, metadata (views, duration), descripción y transcripción completa
```

### Crear plugin personalizado (ej. RTF)
```python
# pyproject.toml:
# [project.entry-points."markitdown.plugin"]
# rtf = "my_plugin:register_converters"

from markitdown import MarkItDown, DocumentConverter, DocumentConverterResult, StreamInfo
from striprtf.striprtf import rtf_to_text

class RtfConverter(DocumentConverter):
    def accepts(self, file_stream, stream_info, **kwargs):
        ext = (stream_info.extension or "").lower()
        return ext in [".rtf"]

    def convert(self, file_stream, stream_info, **kwargs):
        text = file_stream.read().decode(stream_info.charset or "utf-8")
        return DocumentConverterResult(markdown=rtf_to_text(text))


def register_converters(markitdown: MarkItDown, **kwargs):
    markitdown.register_converter(RtfConverter())
```

## Cómo integrarlo en proyectos

### Instalación
```bash
# Todo incluido (recomendado para desarrollo)
pip install 'markitdown[all]'

# Solo formatos específicos (producción, menor dependencia)
pip install 'markitdown[pdf,docx,xlsx]'
```

### Estructura de conversores (para extender)
Cada conversor sigue el patrón:
- `accepts(file_stream, stream_info, **kwargs)` → `bool`: decide si puede manejar el archivo
- `convert(file_stream, stream_info, **kwargs)` → `DocumentConverterResult`: realiza la conversión

Los conversores se registran con prioridad (menor número = mayor prioridad). Built-ins se ordenan así:
- `PRIORITY_SPECIFIC_FILE_FORMAT` (0): conversores específicos (PDF, DOCX, XLSX, etc.)
- `PRIORITY_GENERIC_FILE_FORMAT` (10): conversores genéricos (texto plano, HTML, ZIP)

### Consideraciones de seguridad
- `convert()` es permisivo (acepta paths, URLs, streams). Para entornos no confiables, usa `convert_local()` o `convert_stream()` con control explícito.
- Sanitiza inputs en aplicaciones server-side: valida paths, limita esquemas URI, bloquea acceso a metadata-services.
- MarkItDown usa `magika` para detección de tipo de archivo desde el contenido binario, no solo extensiones.

### Integración con LangChain / AutoGen
MarkItDown está construido por el equipo de AutoGen (Microsoft). Se integra naturalmente con LangChain's `UnstructuredLoader` o cualquier pipeline que acepte Markdown como entrada.

### Docker
```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < archivo.pdf > salida.md
```

### Línea de comandos
```bash
# Conversión básica
markitdown archivo.pdf -o salida.md

# Pipe desde stdin
cat archivo.pdf | markitdown > salida.md

# Con hint de extensión (útil para stdin)
cat archivo | markitdown -x .pdf > salida.md

# Con plugins habilitados
markitdown --use-plugins archivo.pdf

# Listar plugins instalados
markitdown --list-plugins
```

## Fecha de aprendizaje: 2026-05-27

# Formatos Soportados — Converters y Dependencias

## Resumen de Todos los Converters

| # | Converter | Clase | MIME / Extensiones | Prioridad | Dependencias |
|---|-----------|-------|-------------------|-----------|-------------|
| 1 | Plain Text | `PlainTextConverter` | `text/*`, `application/json`, `application/markdown`, `.txt`, `.md`, `.json`, `.jsonl` | 10 (generic) | `charset-normalizer` (core) |
| 2 | ZIP | `ZipConverter` | `application/zip`, `application/x-tar`, `application/x-rar`, etc. | 10 (generic) | `defusedxml` (core) |
| 3 | HTML | `HtmlConverter` | `text/html`, `application/xhtml+xml` | 10 (generic) | `beautifulsoup4`, `markdownify` (core) |
| 4 | RSS | `RssConverter` | `application/rss+xml`, `application/atom+xml` | 0 (specific) | `beautifulsoup4` (core) |
| 5 | Wikipedia | `WikipediaConverter` | URLs de Wikipedia | 0 (specific) | `requests` (core) |
| 6 | YouTube | `YouTubeConverter` | URLs de YouTube | 0 (specific) | `youtube-transcript-api` ([youtube-transcription]) |
| 7 | Bing SERP | `BingSerpConverter` | URLs de Bing | 0 (specific) | `requests` (core) |
| 8 | Jupyter Notebook | `IpynbConverter` | `application/x-ipynb+json`, `.ipynb` | 0 (specific) | `json` (stdlib) |
| 9 | DOCX | `DocxConverter` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `.docx` | 0 (specific) | `mammoth~=1.11.0`, `lxml` ([docx]) |
| 10 | XLSX | `XlsxConverter` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `.xlsx` | 0 (specific) | `pandas`, `openpyxl` ([xlsx]) |
| 11 | XLS | `XlsConverter` | `application/vnd.ms-excel`, `.xls` | 0 (specific) | `pandas`, `xlrd` ([xls]) |
| 12 | PPTX | `PptxConverter` | `application/vnd.openxmlformats-officedocument.presentationml.presentation`, `.pptx` | 0 (specific) | `python-pptx` ([pptx]) |
| 13 | Audio | `AudioConverter` | `audio/*` | 0 (specific) | `pydub`, `SpeechRecognition` ([audio-transcription]) |
| 14 | Imagen | `ImageConverter` | `image/jpeg`, `image/png`, `.jpg`, `.jpeg`, `.png` | 0 (specific) | `exiftool` (binario opcional) |
| 15 | PDF | `PdfConverter` | `application/pdf`, `application/x-pdf`, `.pdf` | 0 (specific) | `pdfminer.six>=20251230`, `pdfplumber>=0.11.9` ([pdf]) |
| 16 | Outlook MSG | `OutlookMsgConverter` | `application/vnd.ms-outlook`, `.msg` | 0 (specific) | `olefile` ([outlook]) |
| 17 | EPUB | `EpubConverter` | `application/epub+zip`, `.epub` | 0 (specific) | `defusedxml` (core) |
| 18 | CSV | `CsvConverter` | `text/csv`, `.csv` | 0 (specific) | `pandas` (core via [xlsx]) |
| 19 | Document Intelligence | `DocumentIntelligenceConverter` | Varios (configurable) | 0 (specific) | `azure-ai-documentintelligence`, `azure-identity` ([az-doc-intel]) |
| 20 | Content Understanding | `ContentUnderstandingConverter` | Varios (configurable) | 0 (specific) | `azure-ai-contentunderstanding>=1.2.0b1`, `azure-identity` ([az-content-understanding]) |

## Dependencias Core (siempre instaladas)

```
beautifulsoup4
requests
markdownify
magika~=0.6.1
charset-normalizer
defusedxml
```

## Extras Opcionales

| Extra | Paquetes | Formatos Habilitados |
|-------|----------|---------------------|
| `[all]` | Todos los de abajo | Todos los formatos |
| `[pptx]` | `python-pptx` | PowerPoint (.pptx) |
| `[docx]` | `mammoth~=1.11.0`, `lxml` | Word (.docx) |
| `[xlsx]` | `pandas`, `openpyxl` | Excel moderno (.xlsx) |
| `[xls]` | `pandas`, `xlrd` | Excel antiguo (.xls) |
| `[pdf]` | `pdfminer.six>=20251230`, `pdfplumber>=0.11.9` | PDF (.pdf) |
| `[outlook]` | `olefile` | Outlook MSG (.msg) |
| `[audio-transcription]` | `pydub`, `SpeechRecognition` | Audio WAV/MP3 (.wav, .mp3) |
| `[youtube-transcription]` | `youtube-transcript-api~=1.0.0` | Transcripción de YouTube |
| `[az-doc-intel]` | `azure-ai-documentintelligence`, `azure-identity` | Azure Document Intelligence |
| `[az-content-understanding]` | `azure-ai-contentunderstanding>=1.2.0b1`, `azure-identity` | Azure Content Understanding |

## Detalles por Formato

### PDF (`PdfConverter`)

- **MIME prefixes:** `application/pdf`, `application/x-pdf`
- **Extensiones:** `.pdf`
- **Dependencias:** `pdfminer.six>=20251230`, `pdfplumber>=0.11.9`
- **Notas:** Usa pdfplumber como motor principal, pdfminer como fallback. Maneja tablas con conversión a Markdown table.

### Word DOCX (`DocxConverter`)

- **MIME:** `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- **Extensiones:** `.docx`
- **Dependencias:** `mammoth~=1.11.0`, `lxml`
- **Notas:** Mammoth convierte DOCX a HTML interno, luego markdownify a Markdown.

### Excel XLSX (`XlsxConverter`)

- **MIME:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Extensiones:** `.xlsx`
- **Dependencias:** `pandas`, `openpyxl`
- **Notas:** Usa pandas para leer hojas de cálculo, convierte cada hoja a tablas Markdown.

### Excel XLS (`XlsConverter`)

- **MIME:** `application/vnd.ms-excel`
- **Extensiones:** `.xls`
- **Dependencias:** `pandas`, `xlrd`
- **Notas:** Para archivos Excel antiguos (.xls), usa xlrd como motor de lectura.

### PowerPoint PPTX (`PptxConverter`)

- **MIME:** `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- **Extensiones:** `.pptx`
- **Dependencias:** `python-pptx`
- **Notas:** Extrae texto de cada slide, incluye notas del presentador si existen.

### Imágenes (`ImageConverter`)

- **MIME prefixes:** `image/jpeg`, `image/png`
- **Extensiones:** `.jpg`, `.jpeg`, `.png`
- **Dependencias:** `exiftool` (herramienta externa opcional para metadata)
- **Notas:** Extrae metadata EXIF (ImageSize, Title, Caption, Keywords, GPSPosition, etc.). Si se configura `llm_client` y `llm_model`, describe la imagen con un modelo multimodal.

### Audio (`AudioConverter`)

- **MIME:** `audio/*`
- **Extensiones:** `.wav`, `.mp3`, `.ogg`, `.flac`, `.mp4`, `.m4a`
- **Dependencias:** `pydub`, `SpeechRecognition`
- **Notas:** Extrae metadata EXIF + transcripción de voz a texto usando SpeechRecognition.

### HTML (`HtmlConverter`)

- **MIME:** `text/html`, `application/xhtml+xml`
- **Extensiones:** `.html`, `.htm`
- **Dependencias:** `beautifulsoup4`, `markdownify` (core)
- **Notas:** BeautifulSoup parsea el HTML, markdownify convierte a Markdown.

### CSV (`CsvConverter`)

- **MIME:** `text/csv`
- **Extensiones:** `.csv`
- **Dependencias:** `pandas`
- **Notas:** Lee con pandas, convierte cada fila a tabla Markdown.

### Jupyter Notebook (`IpynbConverter`)

- **MIME:** `application/x-ipynb+json`
- **Extensiones:** `.ipynb`
- **Dependencias:** `json` (stdlib)
- **Notas:** Extrae celdas de código y markdown del notebook.

### EPUB (`EpubConverter`)

- **MIME:** `application/epub+zip`
- **Extensiones:** `.epub`
- **Dependencias:** `defusedxml` (core)
- **Notas:** Descomprime ZIP, extrae capítulos XHTML y los convierte a Markdown.

### ZIP (`ZipConverter`)

- **MIME prefixes:** `application/zip`, `application/x-tar`, `application/x-rar-compressed`, `application/gzip`, `application/x-7z-compressed`, `application/x-bzip2`, `application/x-xz`, `application/zstd`
- **Extensiones:** `.zip`, `.tar`, `.gz`, `.7z`, `.bz2`, `.xz`, `.zst`
- **Dependencias:** `defusedxml` (core), `zipfile` (stdlib)
- **Notas:** Itera sobre el contenido del archivo comprimido, convierte cada archivo interno recursivamente.

### YouTube (`YouTubeConverter`)

- **URLs:** URLs de YouTube
- **Dependencias:** `youtube-transcript-api~=1.0.0`
- **Notas:** Extrae transcripción/subtítulos del video de YouTube.

### Wikipedia (`WikipediaConverter`)

- **URLs:** URLs de Wikipedia
- **Dependencias:** `requests` (core)
- **Notas:** Extrae contenido de páginas de Wikipedia.

### Outlook MSG (`OutlookMsgConverter`)

- **MIME:** `application/vnd.ms-outlook`
- **Extensiones:** `.msg`
- **Dependencias:** `olefile`
- **Notas:** Parsea archivos de mensaje de Outlook (OLE compound document).

### Azure Document Intelligence (`DocumentIntelligenceConverter`)

- **Tipos configurables:** PDF, DOCX, PPTX, XLSX, imágenes, HTML
- **Dependencias:** `azure-ai-documentintelligence`, `azure-identity`
- **Notas:** Conversión en la nube con análisis de layout avanzado. Se configura con `docintel_endpoint`.

### Azure Content Understanding (`ContentUnderstandingConverter`)

- **Tipos configurables:** Documentos, imágenes, audio, video
- **Dependencias:** `azure-ai-contentunderstanding>=1.2.0b1`, `azure-identity`
- **Notas:** Análisis multimodal en la nube con extracción de campos estructurados (YAML front matter). Se configura con `cu_endpoint`.

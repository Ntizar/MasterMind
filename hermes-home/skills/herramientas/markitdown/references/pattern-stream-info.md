# Patrón StreamInfo + Detección de MIME Types con Magika + Manejo de Streams

## StreamInfo (Dataclass Inmutable)

`StreamInfo` almacena metadatos sobre un stream de archivo. Es inmutable (`frozen=True`) y usa campos opcionales.

```python
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(kw_only=True, frozen=True)
class StreamInfo:
    """The StreamInfo class is used to store information about a file stream.
    All fields can be None, and will depend on how the stream was opened.
    """

    mimetype: Optional[str] = None
    extension: Optional[str] = None
    charset: Optional[str] = None
    filename: Optional[str] = None       # From local path, url, or Content-Disposition header
    local_path: Optional[str] = None     # If read from disk
    url: Optional[str] = None            # If read from url

    def copy_and_update(self, *args, **kwargs):
        """Copy the StreamInfo object and update it with given StreamInfo
        instance and/or other keyword arguments."""
        new_info = asdict(self)

        for si in args:
            assert isinstance(si, StreamInfo)
            new_info.update({k: v for k, v in asdict(si).items() if v is not None})

        if len(kwargs) > 0:
            new_info.update(kwargs)

        return StreamInfo(**new_info)
```

### Uso de `copy_and_update()`

```python
# Base guess from file path
base_guess = StreamInfo(
    local_path="/path/to/file.pdf",
    extension=".pdf",
    filename="file.pdf",
)

# Merge with additional info
enhanced = base_guess.copy_and_update(mimetype="application/pdf", url="https://example.com/file")
# Result: StreamInfo(mimetype="application/pdf", extension=".pdf", filename="file.pdf",
#                    local_path="/path/to/file.pdf", url="https://example.com/file")
```

## Detección de MIME Types: Capas de Detección

MarkItDown usa un enfoque de múltiples capas:

### Capa 1: Extensión del archivo → MIME (mimetypes)

```python
import mimetypes

# From extension to MIME
if base_guess.extension is not None:
    _m, _ = mimetypes.guess_type("placeholder" + base_guess.extension, strict=False)
    if _m is not None:
        enhanced_guess = enhanced_guess.copy_and_update(mimetype=_m)

# From MIME to extension
if base_guess.mimetype is not None and base_guess.extension is None:
    _e = mimetypes.guess_all_extensions(base_guess.mimetype, strict=False)
    if len(_e) > 0:
        enhanced_guess = enhanced_guess.copy_and_update(extension=_e[0])
```

### Capa 2: Magika (ML-based file type detection)

Magika es el detector principal, basado en ML de Google. Se usa para analizar el contenido binario del stream.

```python
import magika

self._magika = magika.Magika()

# Identify from stream content
result = self._magika.identify_stream(file_stream)

# Check result
if result.status == "ok" and result.prediction.output.label != "unknown":
    mime_type = result.prediction.output.mime_type
    extensions = result.prediction.output.extensions  # list of str
    is_text = result.prediction.output.is_text
```

### Capa 3: Detección de Charset (charset-normalizer)

Solo para archivos de texto detectados por Magika:

```python
import charset_normalizer

# Read first 4k bytes to guess charset
stream_page = file_stream.read(4096)
charset_result = charset_normalizer.from_bytes(stream_page).best()

if charset_result is not None:
    charset = charset_result.encoding
```

### Capa 4: Normalización de Charset

```python
import codecs

def _normalize_charset(self, charset: str | None) -> str | None:
    """Normalize a charset string to a canonical form."""
    if charset is None:
        return None
    try:
        return codecs.lookup(charset).name
    except LookupError:
        return charset
```

## Pipeline Completo: `_get_stream_info_guesses()`

Este es el método central que combina todas las capas de detección:

```python
def _get_stream_info_guesses(
    self, file_stream: BinaryIO, base_guess: StreamInfo
) -> List[StreamInfo]:
    """
    Given a base guess, attempt to guess or expand on the stream info
    using the stream content (via magika).
    """
    guesses: List[StreamInfo] = []

    # Enhance base guess with extension/MIME cross-references
    enhanced_guess = base_guess.copy_and_update()

    if base_guess.mimetype is None and base_guess.extension is not None:
        _m, _ = mimetypes.guess_type("placeholder" + base_guess.extension, strict=False)
        if _m is not None:
            enhanced_guess = enhanced_guess.copy_and_update(mimetype=_m)

    if base_guess.mimetype is not None and base_guess.extension is None:
        _e = mimetypes.guess_all_extensions(base_guess.mimetype, strict=False)
        if len(_e) > 0:
            enhanced_guess = enhanced_guess.copy_and_update(extension=_e[0])

    # Call magika to guess from stream content
    cur_pos = file_stream.tell()
    try:
        result = self._magika.identify_stream(file_stream)
        if result.status == "ok" and result.prediction.output.label != "unknown":
            # For text files, also guess charset
            charset = None
            if result.prediction.output.is_text:
                file_stream.seek(cur_pos)
                stream_page = file_stream.read(4096)
                charset_result = charset_normalizer.from_bytes(stream_page).best()
                if charset_result is not None:
                    charset = self._normalize_charset(charset_result.encoding)

            guessed_extension = None
            if len(result.prediction.output.extensions) > 0:
                guessed_extension = "." + result.prediction.output.extensions[0]

            # Check compatibility between base guess and magika guess
            compatible = True
            if base_guess.mimetype is not None and base_guess.mimetype != result.prediction.output.mime_type:
                compatible = False
            if base_guess.extension is not None and base_guess.extension.lstrip(".") not in result.prediction.output.extensions:
                compatible = False
            if base_guess.charset is not None and self._normalize_charset(base_guess.charset) != charset:
                compatible = False

            if compatible:
                # Single compatible guess
                guesses.append(StreamInfo(
                    mimetype=base_guess.mimetype or result.prediction.output.mime_type,
                    extension=base_guess.extension or guessed_extension,
                    charset=base_guess.charset or charset,
                    filename=base_guess.filename,
                    local_path=base_guess.local_path,
                    url=base_guess.url,
                ))
            else:
                # Incompatible: add both guesses
                guesses.append(enhanced_guess)
                guesses.append(StreamInfo(
                    mimetype=result.prediction.output.mime_type,
                    extension=guessed_extension,
                    charset=charset,
                    filename=base_guess.filename,
                    local_path=base_guess.local_path,
                    url=base_guess.url,
                ))
        else:
            guesses.append(enhanced_guess)
    finally:
        file_stream.seek(cur_pos)  # Always restore stream position

    return guesses
```

## Manejo de Diferentes Tipos de Fuente

`MarkItDown.convert()` acepta 4 tipos de fuente y enruta al método correcto:

```python
def convert(
    self,
    source: Union[str, requests.Response, Path, BinaryIO],
    *,
    stream_info: Optional[StreamInfo] = None,
    **kwargs: Any,
) -> DocumentConverterResult:

    # Local path (str or Path)
    if isinstance(source, str):
        if source.startswith(("http:", "https:", "file:", "data:")):
            return self.convert_uri(source, stream_info=stream_info, **kwargs)
        else:
            return self.convert_local(source, stream_info=stream_info, **kwargs)

    elif isinstance(source, Path):
        return self.convert_local(source, stream_info=stream_info, **kwargs)

    # HTTP response object
    elif isinstance(source, requests.Response):
        return self.convert_response(source, stream_info=stream_info, **kwargs)

    # Binary stream
    elif hasattr(source, "read") and callable(source.read) and not isinstance(source, io.TextIOBase):
        return self.convert_stream(source, stream_info=stream_info, **kwargs)

    else:
        raise TypeError(f"Invalid source type: {type(source)}.")
```

### `convert_local()` — Archivos locales

```python
def convert_local(self, path: Union[str, Path], *, stream_info: Optional[StreamInfo] = None, **kwargs):
    # Build base guess from path
    base_guess = StreamInfo(
        local_path=path,
        extension=os.path.splitext(path)[1],
        filename=os.path.basename(path),
    )
    if stream_info is not None:
        base_guess = base_guess.copy_and_update(stream_info)

    with open(path, "rb") as fh:
        guesses = self._get_stream_info_guesses(file_stream=fh, base_guess=base_guess)
        return self._convert(file_stream=fh, stream_info_guesses=guesses, **kwargs)
```

### `convert_stream()` — Streams binarios

```python
def convert_stream(self, stream: BinaryIO, *, stream_info: Optional[StreamInfo] = None, **kwargs):
    # If stream is not seekable, buffer it entirely into BytesIO
    if not stream.seekable():
        buffer = io.BytesIO()
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            buffer.write(chunk)
        buffer.seek(0)
        stream = buffer

    guesses = self._get_stream_info_guesses(
        file_stream=stream, base_guess=stream_info or StreamInfo()
    )
    return self._convert(file_stream=stream, stream_info_guesses=guesses, **kwargs)
```

### `convert_response()` — Objetos requests.Response

```python
def convert_response(self, response: requests.Response, *, stream_info: Optional[StreamInfo] = None, **kwargs):
    # Extract MIME and charset from Content-Type header
    mimetype = None
    charset = None
    if "content-type" in response.headers:
        parts = response.headers["content-type"].split(";")
        mimetype = parts.pop(0).strip()
        for part in parts:
            if part.strip().startswith("charset="):
                charset = part.split("=")[1].strip()

    # Extract filename from Content-Disposition header
    filename = None
    extension = None
    if "content-disposition" in response.headers:
        m = re.search(r"filename=([^;]+)", response.headers["content-disposition"])
        if m:
            filename = m.group(1).strip("\"'")
            _, extension = os.path.splitext(filename)

    # Fallback: extract from URL
    if filename is None:
        parsed_url = urlparse(response.url)
        _, extension = os.path.splitext(parsed_url.path)
        if len(extension) > 0:
            filename = os.path.basename(parsed_url.path)

    base_guess = StreamInfo(
        mimetype=mimetype, charset=charset, filename=filename,
        extension=extension, url=response.url,
    )

    # Read response into buffer
    buffer = io.BytesIO()
    for chunk in response.iter_content(chunk_size=512):
        buffer.write(chunk)
    buffer.seek(0)

    guesses = self._get_stream_info_guesses(file_stream=buffer, base_guess=base_guess)
    return self._convert(file_stream=buffer, stream_info_guesses=guesses, **kwargs)
```

### `convert_uri()` — URIs (file:, data:, http:, https:)

```python
def convert_uri(self, uri: str, *, stream_info: Optional[StreamInfo] = None, **kwargs):
    uri = uri.strip()

    if uri.startswith("file:"):
        netloc, path = file_uri_to_path(uri)
        return self.convert_local(path, stream_info=stream_info, **kwargs)

    elif uri.startswith("data:"):
        mimetype, attributes, data = parse_data_uri(uri)
        base_guess = StreamInfo(mimetype=mimetype, charset=attributes.get("charset"))
        return self.convert_stream(io.BytesIO(data), stream_info=base_guess, **kwargs)

    elif uri.startswith(("http:", "https:")):
        response = self._requests_session.get(uri, stream=True)
        response.raise_for_status()
        return self.convert_response(response, stream_info=stream_info, **kwargs)

    else:
        raise ValueError(f"Unsupported URI scheme: {uri.split(':')[0]}")
```

## Resumen del Pipeline

```
convert(source)
    │
    ├─ local path  → convert_local()
    ├─ URL         → convert_uri() → convert_response()
    ├─ data: URI   → convert_uri() → convert_stream()
    ├─ requests.Response → convert_response()
    └─ BinaryIO    → convert_stream()
        │
        └─ _get_stream_info_guesses()
            │
            ├─ Capa 1: mimetypes (ext ↔ MIME)
            ├─ Capa 2: magika.identify_stream() (ML-based)
            ├─ Capa 3: charset-normalizer (text files)
            └─ Capa 4: codecs.normalize (canonical charset)
        │
        └─ _convert(file_stream, stream_info_guesses)
            │
            └─ For each guess → For each converter (sorted by priority)
                ├─ converter.accepts(file_stream, stream_info)
                └─ converter.convert(file_stream, stream_info) → DocumentConverterResult
```

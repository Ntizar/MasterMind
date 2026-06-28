# Patrón DocumentConverter + DocumentConverterResult + Sistema de Plugins

## DocumentConverterResult

Clase resultado que encapsula la conversión a Markdown. Solo el parámetro `markdown` es obligatorio; el `title` es opcional.

```python
from typing import Optional

class DocumentConverterResult:
    """The result of converting a document to Markdown."""

    def __init__(
        self,
        markdown: str,
        *,
        title: Optional[str] = None,
    ):
        """
        Initialize the DocumentConverterResult.

        The only required parameter is the converted Markdown text.
        The title, and any other metadata that may be added in the future, are optional.

        Parameters:
        - markdown: The converted Markdown text.
        - title: Optional title of the document.
        """
        self.markdown = markdown
        self.title = title

    @property
    def text_content(self) -> str:
        """Soft-deprecated alias for `markdown`. New code should migrate to using `markdown` or __str__."""
        return self.markdown

    @text_content.setter
    def text_content(self, markdown: str):
        """Soft-deprecated alias for `markdown`. New code should migrate to using `markdown` or __str__."""
        self.markdown = markdown

    def __str__(self) -> str:
        """Return the converted Markdown text."""
        return self.markdown
```

## DocumentConverter (Clase Base Abstracta)

Cada convertidor debe implementar `accepts()` y `convert()`. El patrón es:

1. **`accepts()`** — decide rápidamente si este convertidor puede manejar el archivo basado en `stream_info.mimetype`, `stream_info.extension`, `stream_info.url` o `stream_info.filename`.
2. **`convert()`** — realiza la conversión real y retorna `DocumentConverterResult`.

**Regla crítica:** `accepts()` **nunca debe avanzar la posición del stream**. Si necesita leer bytes para determinar compatibilidad, debe restaurar la posición antes de retornar.

```python
from typing import Any, BinaryIO, Optional
from ._stream_info import StreamInfo


class DocumentConverter:
    """Abstract superclass of all DocumentConverters."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        """
        Return a quick determination on if the converter should attempt converting the document.
        This is primarily on `stream_info` (typically, `stream_info.mimetype`, `stream_info.extension`).
        In cases where the data is retrieved via HTTP, the `stream_info.url` might also be referenced.
        Finally, `stream_info.filename` can be used when the filename is well-known (e.g., Dockerfile).

        NOTE: The method signature matches convert() for assurance that if accepts() returns True,
              convert() will also be able to handle the document.

        IMPORTANT: Read operations advance file_stream position. In these cases, the position
        MUST be reset before returning, because convert() may be called immediately after.

        E.g.,
            cur_pos = file_stream.tell()
            data = file_stream.read(100)
            file_stream.seek(cur_pos)
        """
        raise NotImplementedError(
            f"The subclass, {type(self).__name__}, must implement the accepts() method."
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        """
        Convert a document to Markdown text.

        Raises:
        - FileConversionException: If the mimetype is recognized but conversion fails.
        - MissingDependencyException: If required dependency is not installed.
        """
        raise NotImplementedError("Subclasses must implement this method")
```

## Ejemplo Real: ImageConverter

Patrón típico de un convertidor que usa MIME prefixes y extensiones:

```python
from typing import BinaryIO, Any
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "image/jpeg",
    "image/png",
]

ACCEPTED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


class ImageConverter(DocumentConverter):
    """
    Converts images to markdown via EXIF metadata extraction and
    LLM-based description (if llm_client is configured).
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # ... extract metadata, describe with LLM, build markdown ...
        pass
```

## Ejemplo Real: PlainTextConverter

Convertidor genérico con prioridad baja (se ejecuta como fallback):

```python
from charset_normalizer import from_bytes
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/",
    "application/json",
    "application/markdown",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".txt", ".text", ".md", ".markdown", ".json", ".jsonl",
]


class PlainTextConverter(DocumentConverter):
    """Anything with content type text/plain"""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # If we have a charset, we can safely assume it's text
        if stream_info.charset is not None:
            return True

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False
```

## Sistema de Registro de Convertidores

La clase `MarkItDown` mantiene una lista ordenada por prioridad de `ConverterRegistration`:

```python
from dataclasses import dataclass
from typing import List, Any, Union

# Lower priority values are tried first.
PRIORITY_SPECIFIC_FILE_FORMAT = 0.0    # e.g., .docx, .pdf, .xlsx
PRIORITY_GENERIC_FILE_FORMAT = 10.0    # Near catch-all converters (text/*, etc.)

@dataclass(kw_only=True, frozen=True)
class ConverterRegistration:
    """A registration of a converter with its priority and other metadata."""
    converter: DocumentConverter
    priority: float

class MarkItDown:
    def __init__(self, *, enable_builtins: Union[None, bool] = None, **kwargs):
        self._converters: List[ConverterRegistration] = []
        if enable_builtins is None or enable_builtins:
            self.enable_builtins(**kwargs)

    def register_converter(
        self,
        converter: DocumentConverter,
        *,
        priority: float = PRIORITY_SPECIFIC_FILE_FORMAT,
    ) -> None:
        """
        Register a converter with a given priority. Lower values = higher priority.
        New converters are inserted at position 0 (most recently registered wins).
        """
        self._converters.insert(
            0, ConverterRegistration(converter=converter, priority=priority)
        )
```

## Ejecución del Pipeline de Conversión

El motor `_convert()` itera sobre guesses de MIME y convertidores ordenados por prioridad:

```python
def _convert(
    self, *, file_stream: BinaryIO, stream_info_guesses: List[StreamInfo], **kwargs
) -> DocumentConverterResult:
    res: Union[None, DocumentConverterResult] = None
    failed_attempts: List[FailedConversionAttempt] = []

    # Converters sorted by priority (stable sort)
    sorted_registrations = sorted(self._converters, key=lambda x: x.priority)
    cur_pos = file_stream.tell()

    for stream_info in stream_info_guesses + [StreamInfo()]:
        for converter_registration in sorted_registrations:
            converter = converter_registration.converter

            # Check if converter handles this file
            _accepts = converter.accepts(file_stream, stream_info, **kwargs)
            assert cur_pos == file_stream.tell(), \
                f"{type(converter).__name__}.accept() should NOT change the file_stream position"

            if _accepts:
                try:
                    res = converter.convert(file_stream, stream_info, **kwargs)
                except Exception:
                    failed_attempts.append(
                        FailedConversionAttempt(converter=converter, exc_info=sys.exc_info())
                    )
                finally:
                    file_stream.seek(cur_pos)

            if res is not None:
                # Normalize: strip trailing whitespace, collapse multiple blank lines
                res.text_content = "\n".join(
                    [line.rstrip() for line in re.split(r"\r?\n", res.text_content)]
                )
                res.text_content = re.sub(r"\n{3,}", "\n\n", res.text_content)
                return res

    if len(failed_attempts) > 0:
        raise FileConversionException(attempts=failed_attempts)
    raise UnsupportedFormatException(
        "Could not convert stream to Markdown. Filetype not supported."
    )
```

## Sistema de Plugins (Entry Points)

Los plugins se cargan vía `entry_points` del grupo `markitdown.plugin`:

```python
from importlib.metadata import entry_points

_plugins: Union[None, List[Any]] = None

def _load_plugins() -> Union[None, List[Any]]:
    """Lazy load plugins from entry_points group 'markitdown.plugin'."""
    global _plugins
    if _plugins is not None:
        return _plugins

    _plugins = []
    for entry_point in entry_points(group="markitdown.plugin"):
        try:
            _plugins.append(entry_point.load())
        except Exception:
            warn(f"Plugin '{entry_point.name}' failed to load ... skipping")

    return _plugins
```

Cada plugin debe tener un método `register_converters(markitdown_instance, **kwargs)` que llame a `md.register_converter()`.

## Excepciones

```python
class MarkItDownException(Exception):
    """Base exception class for MarkItDown."""
    pass

class MissingDependencyException(MarkItDownException):
    """Converter's required dependency is not installed. Converter is skipped."""
    pass

class UnsupportedFormatException(MarkItDownException):
    """No suitable converter was found for the given file."""
    pass

class FileConversionException(MarkItDownException):
    """A suitable converter was found but conversion failed."""
    def __init__(self, message: Optional[str] = None,
                 attempts: Optional[List[FailedConversionAttempt]] = None):
        self.attempts = attempts
```

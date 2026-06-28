# ASR Backend Pattern — VoiceListener

## Patrón para añadir un nuevo backend ASR a FreeHands

El `VoiceListener` en `whisper_listener.py` soporta múltiples backends ASR (speech recognition). El patrón de adición es:

### 1. Añadir parámetros al `__init__`
```python
def __init__(self, ..., backend: str = "faster_whisper", new_backend_param: str | None = None):
    self.backend = backend
    self.new_backend_param = new_backend_param
```

### 2. Dispatch en `start()`
```python
def start(self) -> "VoiceListener":
    import sounddevice as sd
    if self.backend == "vosk":
        return self._start_vosk()
    # ... existing faster_whisper path
```

### 3. Método `_start_{backend}()`
- Importar backend lazy (dentro del método, no módulo-level)
- Configurar `sounddevice.InputStream` con callback
- Crear recognizer/model
- Iniciar thread daemon con `_loop_{backend}()`

### 4. Loop del backend
Mismo patrón que `_loop()`:
1. Leer chunk de audio de `self._audio`
2. Silencio detection (RMS < 0.006)
3. Transcripción → `parse_voice_command()`
4. Si hay acción → `self.commands.put(VoiceCommand(...))`

### 5. Perfil
Añadir campo en `Profile` (profiles/store.py): `voice_{backend}_param: str = ""`

### 6. main.py
Pasar el nuevo parámetro al `VoiceListener()` constructor.

### 7. Tests
- Mock imports con `sys.modules`
- Para bloquear import: `sys.meta_path.insert(0, finder)` / `.remove(finder)`
- NUNCA `monkeypatch.setattr(__builtins__, "__import__", ...)` — `__builtins__` es un dict en este sandbox

## Archivos modificados típicos
- `voice/whisper_listener.py` — nuevo método + loop
- `profiles/store.py` — nuevo campo de config
- `main.py` — pasar config al listener
- `tests/test_voice_commands.py` — tests de integración

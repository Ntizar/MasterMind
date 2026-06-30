# Patrón: Sistema de Plugins FreeHands

Sistema extensible para inyectar lógica custom en cada etapa del pipeline FreeHands.

## API Principal

### FreeHandsPlugin (clase base)

```python
class FreeHandsPlugin(ABC):
    name: str = "unnamed_plugin"
    version: str = "0.0.0"
    description: str = ""
    enabled_by_default: bool = True
    priority: int = 100  # menor = ejecuta antes

    # Lifecycle
    def on_load(self) -> None: ...
    def on_unload(self) -> None: ...

    # Pipeline hooks (todos opcionales, passthrough por defecto)
    def on_frame(self, frame, ctx) -> Any: ...
    def on_gaze(self, cursor, ctx) -> tuple[int, int] | None: ...
    def on_filter(self, cursor, ctx) -> tuple[int, int] | None: ...
    def on_gesture(self, gesture, confidence, ctx) -> tuple[str | None, float]: ...
    def on_fusion(self, cursor, gesture, action, ctx) -> tuple[...]: ...
    def on_action(self, action, ctx) -> str | None: ...
    def on_overlay(self, ctx) -> None: ...
```

### PluginContext

```python
@dataclass
class PluginContext:
    frame: Any = None                    # numpy.ndarray | None
    cursor: tuple[int, int] | None = None
    gesture: str | None = None
    action: str | None = None
    blink: bool = False
    blink_event: str | None = None
    voice_action: str | None = None
    state: str = "active"
    metadata: dict[str, Any] = {}        # compartido entre plugins
```

### PluginLoader

```python
loader = PluginLoader(plugins_dir="/path/to/plugins")
loader.register(MyPlugin())            # registro manual
loader.register_class(MyPlugin)        # registro de clase (instancia al cargar)
loader.discover_from_directory()       # auto-descubrir .py en directorio
count = loader.load()                  # instancia + on_load + ordena por priority
loader.run_all(ctx)                    # ejecuta todos los hooks del frame
loader.unload()                        # on_unload + limpia
```

## Hooks ejecutables (todos opcionales)

Los hooks se ejecutan **solo si están override** — el base class retorna passthrough.
El loader detecta override comparando `plugin.hook.__func__ is not FreeHandsPlugin.hook`.

## Ejemplo: plugin que suprime acciones

```python
class ActionSuppressor(FreeHandsPlugin):
    name = "suppressor"
    version = "1.0.0"

    def on_action(self, action, ctx):
        if action == "zoom_in":
            return None  # suprime
        return action
```

## Ejemplo: plugin que modifica cursor

```python
class CursorOffset(FreeHandsPlugin):
    name = "cursor_offset"
    priority = 10

    def on_gaze(self, cursor, ctx):
        if cursor:
            return (cursor[0] + 10, cursor[1] + 20)
        return cursor
```

## Ejemplo: plugin que escribe metadata

```python
class MetadataWriter(FreeHandsPlugin):
    name = "metadata_writer"

    def on_gaze(self, cursor, ctx):
        ctx.metadata["cursor_seen"] = cursor
        ctx.metadata["plugin_ran"] = True
        return cursor
```

## Reglas

1. **Excepciones aisladas** — un hook que falla no rompe otros plugins
2. **Orden por priority** — plugins con priority menor ejecutan primero
3. **Modificación in-place** — `ctx` se modifica durante `run_all()`, cada hook ve los cambios previos
4. **Descubrimiento automático** — archivos `.py` en `plugins_dir` se importan, clases `FreeHandsPlugin` subclase se registran
5. **Archivos privados** — los que empiezan con `_` se saltan en discovery
6. **Configuración** — `profile.plugins_dir` configura la ruta; por defecto `src/freehands/plugins/`

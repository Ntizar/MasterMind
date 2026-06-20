# execute_code `read_file` — Límite de 500 líneas y truncamiento silencioso

## El incidente (AdelaCRM, 2026-06-15)

Se usó `execute_code` con `read_file` para modificar el import de `src/db.ts`. El script hizo:

```python
from hermes_tools import read_file, write_file
content = read_file('/path/to/db.ts')
lines = content['content'].split('\n')
# modificar lines[3]...
write_file('/path/to/db.ts', '\n'.join(lines))
```

**Resultado:** `db.ts` pasó de ~1.550 líneas a 501 líneas. Se perdió TODO el trabajo de sesiones anteriores.

**Causa raíz:** `read_file()` en Hermes tools por defecto solo devuelve **500 líneas** (parámetro `limit` con default=500). El archivo original tenía ~1.550 líneas, pero solo se leyeron las primeras 500. Al hacer `write_file()` con 500 líneas, se sobrescribió el archivo completo truncado.

## Síntomas

- El archivo se reduce a ~500 líneas después de un `write_file` desde `execute_code`
- Las funciones/sectiones que estaban después de la línea 500 desaparecen
- No hay error ni advertencia — el truncamiento es silencioso

## Prevención

### Opción 1: Usar `read_file` con `limit` explícito

```python
from hermes_tools import read_file
# Siempre especificar limit suficiente
content = read_file('/path/to/file', limit=2000)  # o más si es necesario
```

### Opción 2: Usar `terminal` con `cat` para archivos grandes

```python
from hermes_tools import terminal
result = terminal('cat /path/to/db.ts')
lines = result['output'].split('\n')
```

### Opción 3: Usar `patch` en vez de `execute_code` para ediciones localizadas

No reescribir el archivo entero. Usar `patch()` (reemplazo de texto exacto) o `write_file` directo desde el agente principal (sin `execute_code`).

### Opción 4: Verificar antes de escribir

```python
from hermes_tools import read_file, terminal

# Contar líneas del archivo original
line_count = int(terminal(f'wc -l < {path}')['output'].strip())
print(f"Archivo tiene {line_count} líneas")

# Leer con límite suficiente
content = read_file(path, limit=line_count + 100)
lines = content['content'].split('\n')
print(f"Leídas {len(lines)} líneas")

if len(lines) < line_count:
    print(f"⚠️ ADVERTENCIA: Solo se leyeron {len(lines)} de {line_count} líneas. No escribir!")
```

## Cuándo usar cada herramienta

| Herramienta | Seguridad | Caso de uso |
|-------------|-----------|-------------|
| `patch()` (agente principal) | ✅ Alta — fuzzy matching, no reescribe completo | Ediciones localizadas (<50 líneas) |
| `write_file()` (agente principal) | ⚠️ Media — reescribe completo | Archivos nuevos o reconstrucción completa |
| `execute_code` | 🔴 Baja — `read_file` limita a 500 líneas | Sólo si se verifica el tamaño completo antes |
| `terminal('sed/awk')` | 🔴 Baja — propenso a errores de regex | Evitar, preferir `patch` |

## Verificación después de recovery

Cuando se pierde contenido por este error:

1. **No tocar más el archivo** — el daño ya está hecho
2. **Recuperar del commit más reciente:** `git restore <file>` o `git checkout HEAD -- <file>`
3. **Identificar qué se perdió:** comparar con archivos hermanos (route imports, types, server.ts)
4. **Reconstruir** usando los imports de las rutas como especificación de lo que necesita el sistema
5. **Hacer commit ANTES de cualquier edición grande** para tener un punto de restauración
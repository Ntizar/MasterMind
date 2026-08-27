# Line Number Prefix Corruption — Detección y corrección

## Problema

Archivos HTML contienen prefijos de línea tipo `N|` o `   N|` al inicio de cada línea. Esto causa:
- **CSS roto** — los números dentro de `<style>` se interpretan como texto CSS inválido
- **Texto visible** — los números aparecen como contenido visible en la página (ej: "52|", "53|")
- **HTML parcialmente funcional** — la estructura base puede funcionar pero el estilo está destruido

**Origen típico:** Alguien usó una herramienta de visualización de código (editor, terminal con `read_file`, viewer) que prependía números de línea, y el output se guardó como el archivo real. También ocurre con scripts de generación que incorporan el output de `cat -n` o similar.

**Ejemplo real (DeSumarIntegrar):**
```
1|<!DOCTYPE html>
     2|<html lang="es">
     3|<head>
     4|<meta charset="UTF-8">
```
Los primeros 6 archivos del proyecto estaban así — el CSS entero era ilegible.

## Detección

```bash
# Detección rápida: buscar líneas que empiezan con número+pipe
grep -rlP '^\s*\d+\|' *.html

# Contar cuántas líneas afectadas por archivo
for f in *.html; do
  count=$(grep -cP '^\s*\d+\|' "$f" 2>/dev/null)
  [ "$count" -gt 0 ] && echo "❌ $f: $count líneas"
done
```

```python
import re, os

def detect_line_number_corruption(content):
    """Detecta prefijos de línea N| en el contenido HTML."""
    lines_with_nums = re.findall(r'^\s*\d+\|', content, re.MULTILINE)
    return len(lines_with_nums)

# Uso
for f in sorted(os.listdir('.')):
    if not f.endswith('.html'): continue
    content = open(f).read()
    count = detect_line_number_corruption(content)
    if count > 0:
        print(f"❌ {f}: {count} líneas con prefijos")
```

## Corrección

```python
import re

def strip_line_numbers(content):
    """Elimina prefijos de línea N| de todo el contenido."""
    return re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)
```

**La regex `^\s*\d+\|` cubre:**
- `1|` (sin espacios)
- `     2|` (con espacios)
- Cualquier combinación de espacios + dígitos + pipe

**⚠️ Cuidado:** No confundir con archivos donde `|` es parte legítima del contenido (tablas Markdown, etc.). En HTML puro, `|` al inicio de línea es casi siempre corrupción.

## Diferenciación con `read_file` de Hermes

El tool `read_file` de Hermes **siempre** prependea números de línea con `|` al output. Esto es normal del tool, NO indica corrupción del archivo. Para verificar si el archivo real está corrupto, usar `terminal("head -5 archivo.html")` que no añaden números.

**Trampa conocida:** Si se verifica el archivo con `read_file` y se ve `1|<!DOCTYPE`, parecería corrupto pero puede ser solo el formato del tool. **Siempre usar `terminal()` para verificar el contenido real.**

## Verificación post-fix

```python
# Confirmar que no queda ningún prefijo
for f in os.listdir('.'):
    if not f.endswith('.html'): continue
    content = open(f).read()
    if re.findall(r'^\s*\d+\|', content, re.MULTILINE):
        print(f"❌ {f} AÚN CORROMPIDO")
print("✅ Todos limpios")
```

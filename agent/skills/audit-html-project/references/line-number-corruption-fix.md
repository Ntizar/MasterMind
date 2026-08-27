# Line Number Corruption Fix — Prefijos `N|` en HTML

## Problema

Archivos HTML contienen prefijos de línea como `52|` o `     3|` al inicio de cada línea. Esto causa:
- **CSS roto** — los números dentro de `<style>` rompen reglas CSS
- **Texto visible** — los números se renderizan como contenido visible en la página
- **HTML parcialmente válido** — el navegador intenta renderizar pero muestra basura

**Causa común:** Alguna herramienta escribe el output de `read_file()` (que prependea `N|` para display) de vuelta al archivo con `write_file()`.

**Ejemplo real:** `s09-bachiller.html` tenía 131 líneas con prefijos `N|`, `eso1-3-proporcionalidad.html` tenía 274.

## Detección

```bash
# Buscar archivos con prefijos de línea
for f in *.html; do
  count=$(grep -cP '^\s*\d+\|' "$f" 2>/dev/null)
  [ "$count" -gt 0 ] && echo "❌ $f: $count líneas con números"
done
```

```python
import re, os

def detect_line_number_corruption(content):
    """Cuenta líneas con prefijo N| al inicio"""
    return len(re.findall(r'^\s*\d+\|', content, re.MULTILINE))

html_dir = "/path/to/project"
for f in sorted(os.listdir(html_dir)):
    if f.endswith('.html'):
        with open(os.path.join(html_dir, f), 'r', errors='replace') as fh:
            content = fh.read()
        count = detect_line_number_corruption(content)
        if count > 0:
            print(f"❌ {f}: {count} líneas corruptas")
```

## Corrección

```python
import re

def strip_line_numbers(content):
    """Elimina prefijos N| al inicio de cada línea"""
    return re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)

# Para un archivo individual
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()
cleaned = strip_line_numbers(content)
with open(path, 'w', encoding='utf-8') as f:
    f.write(cleaned)
```

## Corrección batch

```python
import re, os

base = "/path/to/project"
html_files = [f for f in os.listdir(base) if f.endswith('.html')]

for fname in html_files:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    count = len(re.findall(r'^\s*\d+\|', content, re.MULTILINE))
    if count > 0:
        cleaned = re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"✅ {fname}: {count} prefijos eliminados → {len(cleaned)} bytes")
```

## Verificación post-fix

```python
# Confirmar que no queda ningún prefijo
for f in html_files:
    with open(os.path.join(base, f), 'r') as fh:
        content = fh.read()
    remaining = len(re.findall(r'^\s*\d+\|', content, re.MULTILINE))
    if remaining > 0:
        print(f"❌ {f}: AÚN CORROMPIDO ({remaining} restantes)")
```

## Patrón vs CSS double-braces

Ambos son "artifacts de herramienta que rompen HTML":
- **`{{}}`** → viene de Jinja/Python template escaping → SOLO afecta CSS
- **`N|`** → viene de `read_file()` output escrito de vuelta → afecta TODO el archivo (CSS + HTML content)

Diferencia clave: `N|` corrupta tanto el CSS como el contenido visible. `{{}}` solo rompe el CSS pero el contenido HTML se ve normal.

## Prevención

- **NUNCA** escribir el output directo de `read_file()` de vuelta al archivo con `write_file()`
- `read_file()` prependea números de línea para display — son artefactos de herramienta, no contenido real
- Si necesitas leer y reescribir un archivo, usar `read_file()` para entender, luego `patch()` o `write_file()` con contenido limpio

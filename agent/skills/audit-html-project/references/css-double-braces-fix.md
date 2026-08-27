# CSS Double Braces Fix — Patrón de corrección batch

## Problema

Archivos HTML generados por scripts Python/Jinja/templating engines pueden contener `{{` y `}}` en lugar de `{` y `}` en bloques `<style>`. Esto rompe TODOS los estilos CSS.

**Ejemplo real:** `b03-01-isometrica-ejes.html` tenía 46 reglas CSS con `{{` en vez de `{`.

## Detección

```bash
# Buscar {{ dentro de bloques style
grep -n '{{' *.html | grep -A2 -B2 'style'
```

```python
import re

def find_double_braces_in_css(content):
    """Detecta {{}} dentro de bloques <style>"""
    style_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if not style_match:
        return []
    style_content = style_match.group(1)
    issues = []
    for i, line in enumerate(style_content.split('\n')):
        if '{{' in line:
            issues.append((i, line.strip()))
    return issues
```

## Corrección batch

```python
import re
import os

def fix_double_braces_in_style(content):
    """Reemplaza {{ y }} por { y } SOLO dentro de <style> tags"""
    def replace_in_style(match):
        style_tag = match.group(0)
        style_content = match.group(1)
        style_content = style_content.replace('{{', '{').replace('}}', '}')
        return f'<style>{style_content}</style>'
    
    return re.sub(r'<style[^>]*>(.*?)</style>', replace_in_style, content, flags=re.DOTALL)

# Batch fix
base = "/root/workspace/DibujoTecnico"
for fname in os.listdir(base):
    if fname.endswith('.html'):
        path = os.path.join(base, fname)
        with open(path) as f:
            content = f.read()
        
        issues = find_double_braces_in_css(content)
        if issues:
            fixed = fix_double_braces_in_style(content)
            with open(path, 'w') as f:
                f.write(fixed)
            print(f"✅ {fname}: {len(issues)} reglas corregidas")
```

## Verificación post-fix

```bash
# Confirmar que no queda ningún {{ en style tags
grep -n '{{' *.html | grep -A1 -B1 'style'
# Debe no devolver nada
```

## Notas

- **NUNCA** reemplazar `{{` en HTML content (puede ser texto legítimo del curso)
- **SOLO** dentro de bloques `<style>` o `<style ...>`
- Este bug es específico de generadores que usan Python string formatting con `{{` para escapar llaves literales
- En el template CSS base del curso Dibujo Técnico, las llaves CSS son `{}` normales, nunca `{{}}`

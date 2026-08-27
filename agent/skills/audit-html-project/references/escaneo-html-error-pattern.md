# Patrón de Escaneo HTML

Scripts y patrones para detectar errores en proyectos HTML educativos.

## Escaneo de errores básicos

```python
import os, re
from collections import defaultdict

base = "/path/to/project"
html_files = [f for f in os.listdir(base) if f.endswith('.html')]
all_set = set(html_files)

for f in sorted(html_files):
    path = os.path.join(base, f)
    with open(path, 'r') as fh:
        content = fh.read()
    
    issues = []
    if "David Antizar" not in content:
        issues.append("Sin atribución")
    if re.search(r'href="#">\s*Siguiente', content):
        issues.append("Siguiente → #")
    if issues:
        print(f"  {f}: {', '.join(issues)}")
```

## Detección de enlaces malformados (falta >)

Patrón de generación automática donde el `>` de cierre se pierde:

```python
# MAL: <a href="file.html"Siguiente: ...</a>
# BIEN: <a href="file.html">Siguiente: ...</a>

malformed = []
for f in html_files:
    with open(os.path.join(base, f)) as fh:
        content = fh.read()
    # Buscar href="..." sin > antes del espacio o texto
    for match in re.finditer(r'href="([^"]+\.html)"([^\s>])', content):
        malformed.append((f, match.group(1), match.group(2)))

print(f"Enlaces malformados: {len(malformed)}")
for src, target, char in malformed:
    print(f"  {src}: href=\"{target}\"{char}")
```

## Corrección de enlaces malformados

```python
for f, target, char in malformed:
    path = os.path.join(base, f)
    with open(path, 'r') as fh:
        content = fh.read()
    # Añadir > que falta
    content = content.replace(f'href="{target}"{char}', f'href="{target}">{char}')
    with open(path, 'w') as fh:
        fh.write(content)
```

## Detección de inconsistencias estructurales

```python
estructura = defaultdict(list)
for f in html_files:
    with open(os.path.join(base, f)) as fh:
        content = fh.read()
    
    has_nav = '<nav' in content
    has_header = '<header' in content
    has_footer = '<footer' in content
    has_main = '<main' in content
    
    key = f"nav={'✅' if has_nav else '❌'} header={'✅' if has_header else '❌'} footer={'✅' if has_footer else '❌'} main={'✅' if has_main else '❌'}"
    estructura[key].append(f)

print("Estructuras HTML:")
for key, files in estructura.items():
    print(f"  {key}: {len(files)} archivos")
```

## Corrección de navegación

```python
broken = {
    's01-9-medidas-longitud.html': {'prev': 's01-8-medidas-tamano-peso.html', 'next': 's01-10-patrones.html'},
}

for f, info in broken.items():
    path = os.path.join(base, f)
    with open(path, 'r') as fh:
        content = fh.read()
    content = re.sub(r'href="#">\s*(Siguiente)', f'href="{info["next"]}"\\1', content)
    if info['prev']:
        content = re.sub(r'href="#">\s*(Anterior)', f'href="{info["prev"]}"\\1', content)
    with open(path, 'w') as fh:
        fh.write(content)
```

## Páginas de volumen como índices

Deben tener: header, intro box con objetivos, grid de sesiones, resumen, navegación, footer con atribución.
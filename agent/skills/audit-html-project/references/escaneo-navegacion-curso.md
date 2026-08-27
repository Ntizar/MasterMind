# Escaneo de Navegación de Curso Educativo

Patrones y scripts para auditar la navegación de cursos educativos multi-nivel.

## Detectar cadenas paralelas desconectadas

```python
import os, re, glob

base = "/path/to/project"
html_files = sorted(glob.glob(os.path.join(base, '*.html')))
html_basenames = [os.path.basename(f) for f in html_files]
all_set = set(html_basenames)

# Construir mapa de enlaces
all_links = {}
for fname in html_basenames:
    with open(os.path.join(base, fname)) as f:
        content = f.read()
    hrefs = re.findall(r'href="([^"]*\.html)"', content)
    hrefs = [h.split('#')[0].split('?')[0] for h in hrefs]
    all_links[fname] = hrefs

# 1. Enlaces rotos
print("=== ENLACES ROTOS ===")
for src, targets in all_links.items():
    for t in targets:
        if t not in all_set:
            print(f"  ❌ {src} → {t}")

# 2. Clasificar páginas
def classify(fname, content):
    hrefs = re.findall(r'href="([^"]+\.html)"', content)
    session_links = [h for h in hrefs if h not in ('INDEX.html', fname, 'index.html')]
    if len(session_links) >= 5:
        return 'indice'
    elif len(session_links) <= 3:
        return 'sesion'
    return 'indefinido'

print("\n=== CLASIFICACION ===")
for fname in html_basenames:
    with open(os.path.join(base, fname)) as f:
        content = f.read()
    cls = classify(fname, content)
    if cls != 'indefinido':
        title = re.search(r'<title>(.*?)</title>', content)
        t = title.group(1)[:60] if title else '?'
        print(f"  [{cls}] {fname} → {t}")

# 3. Detectar cadenas paralelas (ej: s01-1primaria vs s01-1-contar-0-10)
print("\n=== CADENAS PARALELAS ===")
# Cadena A: archivos que terminan en 'primaria.html' o 'eso.html' o 'bachiller.html' o 'carrera.html'
chain_a = sorted([f for f in html_basenames if re.search(r'(primaria|eso|bachiller|carrera)\.html$', f)])
# Cadena B: archivos con patrón sXX-YY-tema.html
chain_b = sorted([f for f in html_basenames if re.match(r's\d+-\d+-[a-z]', f)])

if chain_a and chain_b:
    # Verificar si alguna página de A enlaza a B
    connected = False
    for src in chain_a:
        with open(os.path.join(base, src)) as f:
            content = f.read()
        for target in chain_b:
            if target in content:
                print(f"  ✅ {src} → {target}")
                connected = True
    if not connected:
        print(f"  ❌ CADENAS DESCONECTADAS: {len(chain_a)} páginas en cadena A, {len(chain_b)} en cadena B, 0 enlaces entre ellas")
        print(f"     Cadena A: {', '.join(chain_a[:5])}...")
        print(f"     Cadena B: {', '.join(chain_b[:5])}...")

# 4. Verificar transiciones entre niveles
print("\n=== TRANSICIONES ENTRE NIVELES ===")
# Obtener última página de cada nivel y verificar su enlace "Siguiente"
for fname in html_basenames:
    with open(os.path.join(base, fname)) as f:
        content = f.read()
    # Buscar "Siguiente →" con href
    next_match = re.search(r'Siguiente.*?href="([^"]+\.html)"', content)
    if next_match:
        target = next_match.group(1)
        if target not in all_set:
            print(f"  ❌ {fname} → Siguiente: {target} (NO EXISTE)")
```

## Verificar consistencia README vs realidad

```python
# Extraer archivos mencionados en README.md
with open(os.path.join(base, 'README.md')) as f:
    readme = f.read()

# Buscar patrones como "s01-1primaria.html ← 1º Primaria"
readme_files = re.findall(r'(\S+\.html)\s*[←\-]', readme)
for f in readme_files:
    if f not in all_set:
        print(f"  ❌ README menciona {f} pero no existe")
    else:
        # Verificar que la descripción coincide
        with open(os.path.join(base, f)) as fh:
            content = fh.read()
        cls = classify(f, content)
        # Buscar qué dice el README sobre este archivo
        desc_match = re.search(re.escape(f) + r'\s*[←\-]+\s*(.*?)$', readme, re.MULTILINE)
        desc = desc_match.group(1).strip() if desc_match else ''
        if 'índice' in desc.lower() and cls == 'sesion':
            print(f"  ⚠️ README dice que {f} es índice, pero es una sesión")
        if 'sesión' in desc.lower() and cls == 'indice':
            print(f"  ⚠️ README dice que {f} es sesión, pero es un índice")
```

## Caso real: Proyecto "De Sumar a Integrar"

En la auditoría del proyecto matemáticas se encontraron:

| Problema | Severidad | Detalle |
|----------|-----------|---------|
| `s01-4primaria.html` → `s01-5primaria.html` | 🔴 Crítico | El archivo no existe |
| `s02-7primaria.html` → `s03-1primaria.html` | 🔴 Crítico | El archivo no existe (el índice real es `s03-3primaria.html`) |
| Cadenas paralelas 1º Primaria | 🟡 Importante | `s01-1primaria` (cadena A) y `s01-1-contar-0-10` (cadena B) sin enlaces entre sí |
| 1º-3º sin índice de nivel | 🟡 Importante | INDEX.html enlaza a sesiones individuales en lugar de índices |
| README desactualizado | 🟢 Menor | Describe `s01-1primaria.html` como índice cuando es sesión |
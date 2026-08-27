# Rebuild Navigation — Técnica batch para reconstruir navegación rota

Cuando la navegación de un proyecto HTML está rota sistemáticamente (la mayoría de enlaces Anterior/Siguiente apuntan a archivos incorrectos), usar esta técnica para reconstruirla de una vez.

## Diagnóstico

Síntomas:
- Todos los "Siguiente" apuntan al archivo incorrecto
- El orden de navegación no coincide con el orden lógico/numérico
- `s01-10` aparece después de `s01-1` en vez de después de `s01-9`

Causa raíz: `sorted()` ordena alfabéticamente, no numéricamente.

## Técnica de reconstrucción

### Paso 1: Construir mapa de navegación correcto

```python
import os, re
from collections import defaultdict

base = "/path/to/project"
html_files = sorted([f for f in os.listdir(base) if f.endswith('.html')])

# Extraer nivel y número de cada archivo
levels = defaultdict(list)
for f in html_files:
    if re.match(r's\d+-\d+-[a-z]', f):  # sesiones detalladas
        match = re.match(r'(s\d+)-(\d+)-', f)
        if match:
            level = match.group(1)
            num = int(match.group(2))  # ← CLAVE: convertir a int para sorting numérico
            levels[level].append((num, f))

# Ordenar NUMÉRICAMENTE dentro de cada nivel
for level in levels:
    levels[level].sort(key=lambda x: x[0])  # ← x[0] es el número entero

# Construir pares de navegación
nav_map = {}
for level in sorted(levels.keys()):
    sessions = [f for _, f in levels[level]]
    for i, f in enumerate(sessions):
        prev_session = sessions[i-1] if i > 0 else None
        next_session = sessions[i+1] if i < len(sessions)-1 else None
        nav_map[f] = {
            'prev': prev_session,
            'next': next_session,
            'is_first': i == 0,
            'is_last': i == len(sessions)-1
        }
```

### Paso 2: Generar HTML de navegación

```python
# Mapa de índices de nivel
level_index_map = {
    's01': 's01-1primaria-index.html',
    's02': 's02-2primaria-index.html',
    # ...
}

for f in nav_map:
    filepath = os.path.join(base, f)
    with open(filepath, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read()
    
    nav = nav_map[f]
    level_match = re.match(r'(s\d+)-', f)
    level = level_match.group(1) if level_match else None
    index_file = level_index_map.get(level, 'INDEX.html')
    
    # Construir navegación de 3 partes
    nav_parts = []
    
    # Izquierda: Anterior o Índice
    if nav['prev']:
        nav_parts.append(f'<a href="{nav["prev"]}">← Anterior</a>')
    else:
        nav_parts.append(f'<a href="{index_file}">← Índice del nivel</a>')
    
    # Centro: Índice (solo si no es primera ni última para evitar duplicación)
    if not nav['is_first'] and not nav['is_last']:
        nav_parts.append(f'  <a href="{index_file}" style="color:#94a3b8;font-size:0.85rem">📋 Índice del nivel</a>')
    
    # Derecha: Siguiente o Volver
    if nav['next']:
        nav_parts.append(f'<a href="{nav["next"]}">Siguiente →</a>')
    else:
        nav_parts.append(f'<a href="{index_file}">Volver al índice →</a>')
    
    new_nav = '<div class="nav">\n' + '\n'.join(nav_parts) + '\n</div>'
    
    # Reemplazar nav existente
    old_nav = re.search(r'<div class="nav">.*?</div>', content, re.S)
    if old_nav:
        new_content = content[:old_nav.start()] + new_nav + content[old_nav.end():]
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
```

### Paso 3: Manejar transiciones entre niveles

La última sesión de cada nivel necesita un enlace especial a la primera del siguiente nivel:

```python
# Después del batch fix general, sobrescribir las transiciones
transitions = [
    ('s01-10-patrones.html', 's02-1-sumas-llevadas.html', '2º Primaria'),
    ('s06-10-repasos-primaria.html', 's07-1eso.html', '1º ESO'),
    # ...
]

for src, target, label in transitions:
    with open(os.path.join(base, src), 'r') as f:
        content = f.read()
    
    # Reemplazar "Volver al índice" con enlace al siguiente nivel
    old_pattern = f'<a href="{index_file}">Volver al índice →</a>'
    new_link = f'<a href="{target}">{label} →</a>'
    content = content.replace(old_pattern, new_link)
    
    with open(os.path.join(base, src), 'w') as f:
        f.write(content)
```

## Verificación post-rebuild

```python
# Verificar que la navegación es correcta
for f in nav_map:
    with open(os.path.join(base, f)) as fh:
        content = fh.read()
    
    nav_match = re.search(r'<div class="nav">(.*?)</div>', content, re.S)
    if nav_match:
        nav = nav_match.group(0)
        # Verificar que los targets existen
        links = re.findall(r'href="([^"]*)"', nav)
        for link in links:
            if link != '#' and not os.path.exists(os.path.join(base, link)):
                print(f'❌ {f}: enlace roto → {link}')
```

## Ejemplo real: DeSumarIntegrar

- **Problema:** 73 sesiones con navegación rota (todos los "Siguiente" apuntaban al archivo incorrecto)
- **Causa:** `sorted()` alfabético ponía `s01-10` antes de `s01-2`
- **Solución:** Reconstrucción completa con sorting numérico
- **Resultado:** 73/73 sesiones con navegación correcta, 0 enlaces rotos

## Pitfalls

- **NO parchear individualmente** — Si 50+ archivos tienen el mismo patrón de error, reconstruir de una vez
- **Transiciones entre niveles** — La última sesión de cada nivel necesita trato especial (enlace al siguiente nivel, no al índice)
- **Prueba de sanity** — Después del rebuild, verificar manualmente que `s01-10` viene después de `s01-9`, no antes

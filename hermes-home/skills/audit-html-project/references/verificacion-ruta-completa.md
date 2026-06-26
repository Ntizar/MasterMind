# Verificación de Ruta Completa de Navegación

Script para verificar que la navegación completa de un curso educativo funciona:
INDEX → índice de nivel → sesión → vuelta al índice → INDEX → siguiente nivel.

## Script de verificación completo

```python
import os, re

base = "/path/to/project"
html_files = sorted([f for f in os.listdir(base) if f.endswith('.html') and f != 'index.html'])
all_set = set(html_files)

# ============================================================
# 1. MAPA DE NAVEGACION
# ============================================================
nav_map = {}
for fname in html_files:
    with open(os.path.join(base, fname)) as f:
        content = f.read()
    
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1) if title_m else 'SIN TITLE'
    hrefs = re.findall(r'href="([^"]*\.html)"', content)
    hrefs = [h.split('#')[0].split('?')[0] for h in hrefs]
    nav_links = re.findall(r'(?:Anterior|Siguiente).*?href="([^"]*\.html)"', content)
    back_links = re.findall(r'Volver al [íi]ndice.*?href="([^"]*\.html)"', content)
    
    nav_map[fname] = {
        'title': title[:60],
        'all_links': hrefs,
        'nav_prev_next': nav_links,
        'back_to_index': back_links,
        'broken': [h for h in hrefs if h not in all_set]
    }

# ============================================================
# 2. MAPA DE CADA SESION A SU INDICE DE NIVEL
# ============================================================
level_index_map = {
    # 1º Primaria
    's01-1-contar-0-10.html': 's01-1primaria-index.html',
    's01-2-contar-10-100.html': 's01-1primaria-index.html',
    # ... todas las sesiones mapeadas
}

# ============================================================
# 3. CADENA DE NIVELES (anterior/siguiente)
# ============================================================
level_chain = [
    ('s01-1primaria-index.html', None, 's02-2primaria-index.html', '1º Primaria', '2º Primaria'),
    ('s02-2primaria-index.html', 's01-1primaria-index.html', 's03-3primaria-index.html', '1º Primaria', '3º Primaria'),
    ('s03-3primaria-index.html', 's02-2primaria-index.html', 's04-4primaria.html', '2º Primaria', '4º Primaria'),
    ('s04-4primaria.html', 's03-3primaria-index.html', 's05-5primaria.html', '3º Primaria', '5º Primaria'),
    ('s05-5primaria.html', 's04-4primaria.html', 's06-6primaria.html', '4º Primaria', '6º Primaria'),
    ('s06-6primaria.html', 's05-5primaria.html', 's07-1eso.html', '5º Primaria', '1º ESO'),
    ('s07-1eso.html', 's06-6primaria.html', 's08-2-3eso.html', '6º Primaria', '2º-3º ESO'),
    ('s08-2-3eso.html', 's07-1eso.html', 's09-bachiller.html', '1º ESO', 'Bachiller'),
    ('s09-bachiller.html', 's08-2-3eso.html', 's10-1carrera.html', '2º-3º ESO', '1º Carrera'),
    ('s10-1carrera.html', 's09-bachiller.html', None, 'Bachiller', None),
]

# ============================================================
# 4. VERIFICACIONES
# ============================================================

print("=== 1. ENLACES ROTOS ===")
total_broken = 0
for fname in html_files:
    info = nav_map.get(fname, {})
    for link in info.get('broken', []):
        print(f"  ❌ {fname} → {link}")
        total_broken += 1
if total_broken == 0:
    print("  ✅ 0 enlaces rotos")

print("\n=== 2. INDEX.HTML → INDICES DE NIVEL ===")
with open(os.path.join(base, 'INDEX.html')) as f:
    index_content = f.read()
index_links = re.findall(r'href="([^"]*\.html)"', index_content)
index_broken = [h for h in index_links if h not in all_set]
if index_broken:
    print(f"  ❌ Enlaces rotos en INDEX: {index_broken}")

# Verificar que INDEX no enlaza a sesiones directas
level_indexes = set(level_index_map.values())
session_files = set(level_index_map.keys())
bad_index_links = session_files & set(index_links)
if bad_index_links:
    print(f"  ❌ INDEX enlaza a sesiones (no a índices): {bad_index_links}")
else:
    print(f"  ✅ INDEX solo enlaza a índices de nivel")

print("\n=== 3. CADA SESION → SU INDICE ===")
missing_back = []
for session, level_idx in level_index_map.items():
    fpath = os.path.join(base, session)
    if not os.path.exists(fpath):
        continue
    with open(fpath) as f:
        content = f.read()
    if level_idx not in content:
        missing_back.append(session)

if missing_back:
    print(f"  ❌ {len(missing_back)} sesiones sin enlace a su índice")
    for s in missing_back[:5]:
        print(f"     - {s}")
else:
    print(f"  ✅ Todas las sesiones enlazan a su índice")

print("\n=== 4. CADA INDICE → INDEX ===")
missing_index = []
for idx_file in set(level_index_map.values()):
    fpath = os.path.join(base, idx_file)
    if not os.path.exists(fpath):
        continue
    with open(fpath) as f:
        content = f.read()
    if 'INDEX.html' not in content:
        missing_index.append(idx_file)

if missing_index:
    print(f"  ❌ {len(missing_index)} índices sin enlace a INDEX")
else:
    print(f"  ✅ Todos los índices enlazan a INDEX")

print("\n=== 5. NAVEGACION ENTRE NIVELES ===")
for level_file, prev, next_level, prev_name, next_name in level_chain:
    fpath = os.path.join(base, level_file)
    if not os.path.exists(fpath):
        print(f"  ❌ {level_file}: no existe")
        continue
    with open(fpath) as f:
        content = f.read()
    
    has_prev = prev is None or prev in content
    has_next = next_level is None or next_level in content
    
    if has_prev and has_next:
        print(f"  ✅ {level_file}")
    else:
        missing = []
        if not has_prev and prev: missing.append(f"← {prev_name}")
        if not has_next and next_level: missing.append(f"{next_name} →")
        print(f"  ⚠️ {level_file}: falta {', '.join(missing)}")

print("\n=== 6. ENLACES HTML MALFORMADOS ===")
bad_count = 0
for fname in html_files:
    with open(os.path.join(base, fname)) as f:
        content = f.read()
    bad_links = re.findall(r'href="([^"]*\.html)"[^>\s]', content)
    if bad_links:
        print(f"  ❌ {fname}: {bad_links}")
        bad_count += 1
if bad_count == 0:
    print("  ✅ 0 enlaces malformados")

print(f"\n{'='*50}")
print(f"RESUMEN: {len(html_files)} archivos, {total_broken} enlaces rotos")
print(f"{'='*50}")
```

## Caso real: Proyecto "De Sumar a Integrar"

En la auditoría de navegación de junio 2026 se encontraron:

| Problema | Solución |
|----------|----------|
| INDEX.html enlazaba Bachiller → `s09-1-bachiller-limites.html` (sesión) | Cambiado a `s09-bachiller.html` (índice) |
| INDEX.html enlazaba Carrera → `s10-1-carrera-limites-multivariable.html` (sesión) | Cambiado a `s10-1carrera.html` (índice) |
| 93 sesiones sin enlace a su índice de nivel | Añadido `📋 Índice del nivel` en la barra de navegación |
| `s04-8-problemas-1-paso.html`: `href="..."Siguiente:` sin `>` | Corregida sintaxis HTML |
| `s02-7-dinero.html`: mismo error | Corregida sintaxis HTML |
| Índices 1º-3º sin navegación entre niveles | Añadidos enlaces ← anterior / siguiente → |
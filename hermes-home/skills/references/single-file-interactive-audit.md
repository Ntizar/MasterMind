# Single-File Interactive App Audit

Procedimiento para auditar aplicaciones web **monolíticas** (un solo archivo HTML con CSS+JS inline): visores interactivos, dashboards vanilla, herramientas de mapa, etc.

## Cuándo usar

- Un solo archivo HTML con CSS `<style>` + JS `<script>` inline
- El usuario reporta "no funciona" o "no hace lo que debería"
- Visores interactivos (Leaflet, Three.js, D3, etc.)
- Herramientas webapp con lógica JS compleja

## Diferencia con `audit-html-project` (multi-file)

| | Multi-file educativo | Single-file interactivo |
|---|---|---|
| Alcance | 10+ archivos | 1 archivo |
| Enfoque | grep batch, enlaces rotos | Lectura línea a línea, lógica JS |
| Errores típicos | href="#", navegación rota | Variables no declaradas, comillas rotas |

## Pasos

### 1. Lectura completa del archivo

Leer TODO el archivo con `read_file`. No usar grep para este tipo de archivos — la lógica está en JS inline y necesita contexto.

### 2. Análisis de variables y scope

Buscar variables usadas antes de declararse. `let` tiene hoisting de bloque: si se usa dentro de una función definida antes pero llamada después, funciona pero es anti-pattern. Declarar arriba con las demás variables globales.

### 3. Análisis de strings HTML generados dinámicamente

Buscar `innerHTML +=` y `htmlContent +=` que contengan atributos `onclick=` con comillas. Las comillas simples dentro de un string JS con comillas simples rompen el output HTML.

**Patrón roto:** `onclick="this.parentElement.classList.toggle('open')"` dentro de `'...'`
**Fix:** Escapar con `\'open\'` o usar template literals (backticks) para el string externo.

### 4. Análisis de lecturas duplicadas

Buscar el mismo archivo/endpoint leído múltiples veces en la misma función. Unificar en una sola lectura.

### 5. Análisis de limpieza de estado entre operaciones

Verificar que variables globales se limpian o no se solapan entre operaciones (ej: múltiples ZIPs GTFS).

### 6. Análisis de UX

Verificar:
- ¿Cierra panel con Escape? → Añadir `keydown` listener
- ¿Debounce en búsqueda? → Añadir `input` listener con `setTimeout`
- ¿Rate limiting de APIs externas? → Nominatim: 1 req/seg

### 7. Verificación post-fix

- No quedan referencias a variables eliminadas
- Balance de comillas en strings HTML generados
- Variables declaradas antes de su primer uso

## Checklist de errores comunes

| Error | Dónde buscar | Fix |
|-------|-------------|-----|
| Variable usada antes de declarar | `let X` vs `X[` | Mover al scope global |
| Comillas rotas en onclick | `htmlContent +=` con `onclick=` | Escapar o usar backticks |
| Lectura duplicada de datos | Mismo archivo 2x | Unificar |
| Estado global no limpio | Variables acumulativas | Limpiar o usar scope local |
| Sin Escape para cerrar paneles | Paneles fijos | Añadir `keydown` |
| Sin debounce en búsqueda | Input sin listener | Defer 500ms |
| KPI subcuenta entidades | `Set(r.entity)` solo primera | `flatMap(r.entities)` todas |

## Ejemplo real: GTFSSpain visor (2026-06-23)

1. `tripRouteMap` declarado en línea 1085, usado en 734 → movido a línea 523
2. `classList.toggle('open')` comillas rotas → escapado con `\\'open\\'`
3. `stop_times.txt` leído 2x → unificado
4. Sin Escape para cerrar panel → añadido `keydown`
5. Sin debounce en geocodificación → añadido `input` listener 500ms

---

## Data-Driven Visor Audit (JSON backend)

Visores que cargan datos desde múltiples archivos JSON tienen una clase distinta de problemas. Patrones extraídos de CIAF-visor (2026-06-26).

### Cuándo usar

- App carga 1+ archivos JSON (reports, memorias, index)
- Hay `enlaces` o campos de referencia en los JSON que el frontend podría usar
- El proyecto tiene PDFs/archivos descargables referenciados por los datos

### Checks específicos

#### 1. Consistencia entre fuentes de datos

Cuando hay múltiples JSON con datos solapados (ej: `reports/2024.json` y `memorias/2024.json`), **cruzar los datos** para detectar inconsistencias:

```python
for year in years:
    reports = json.load(f'reports/{year}.json')
    memoria = json.load(f'memorias/{year}.json')
    actual_count = len(reports)
    reported_count = memoria.get('total_accidents', 0)
    if actual_count != reported_count:
        print(f'❌ {year}: reports={actual_count}, memoria={reported_count}')
```

**Señal de datos fabricados**: si los aggregate counts no coinciden con los source data, los JSON de resumen probablemente son auto-generados/inventados.

#### 2. Enlaces no utilizados (frontend ignora JSON)

Verificar si el frontend usa los campos `enlaces` del JSON o si hardcodea URLs:

```python
# Encontrar campos enlaces en JSON
enlaces_fields = set()
for r in reports:
    enlaces_fields.update(r.get('enlaces', {}).keys())

# Verificar si el frontend los referencia
for field in enlaces_fields:
    if field not in frontend_js:
        print(f'⚠️ Campo enlaces.{field} existe en JSON pero no se usa en frontend')
```

**Patrón roto**: `enlaces.pdf_local` apunta a `pdfs/2025/2025-41-0522-if.pdf` pero el frontend siempre enlaza a la URL genérica del sitio oficial.

#### 3. Existencia de archivos referenciados

Si el JSON tiene `enlaces.pdf_local` u otros campos de path, verificar que los archivos existen en el repo:

```python
missing = []
for r in reports:
    pdf = r.get('enlaces', {}).get('pdf_local', '')
    if pdf and not os.path.isfile(os.path.join(repo_root, pdf)):
        missing.append(pdf)
print(f'PDFs referenciados pero inexistentes: {len(missing)}')
```

#### 4. Claridad de títulos

Verificar que los títulos de los informes son descriptivos, no solo nombres de archivo:

```python
unclear = [r for r in reports if not r.get('titulo') or 
           len(r['titulo']) < 10 or 
           any(x in r['titulo'] for x in ['if_', 'ciaf.pdf', '-if-'])]
```

**Criterio**: si el título parece un nombre de archivo en vez de una descripción humana, es 🟡 Mejora.

#### 5. Vistas ausentes por dimensiones clave

Verificar si los datos soportarían vistas adicionales que no existen:

```python
# ¿Hay entidades/empresas en los datos?
all_entities = set()
for r in reports:
    all_entities.update(r.get('entidades', []))

# ¿El frontend tiene vista por entidad?
if 'entity' not in frontend_filters and len(all_entities) > 3:
    print(f'💡 Datos tienen {len(all_entities)} entidades pero no hay vista por empresa')
```

### Ejemplo real: CIAF-visor (2026-06-26)

- 270 PDFs existen en repo, paths correctos en JSON → ✅
- Frontend ignora `enlaces.pdf_local`, siempre enlaza a URL genérica → ❌ enlace roto
- Memorias JSON dicen "58 accidents" pero solo hay 1 report → ❌ datos fabricados
- 13 informes con títulos tipo nombre de archivo → 🟡 mejoras
- 17 entidades pero sin vista por empresa → 💡 oportunidad
- 17 memorias PDFs en repo pero no enlazadas desde el visor → ❌ recurso desperdiciado

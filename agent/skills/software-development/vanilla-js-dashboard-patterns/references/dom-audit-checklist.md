# DOM Audit Checklist — vanilla-js-dashboard-patterns

Procedimiento de verificación automática de IDs DOM antes de probar un dashboard vanilla JS.

## Problema

Los módulos JS buscan IDs con `getElementById()` o `querySelector()`. Si un ID no existe en el HTML, el módulo falla silenciosamente (return early). El usuario ve una página vacía y no sabe por qué.

## Solución

Auditar TODOS los IDs buscados por los módulos contra los IDs presentes en el HTML **antes** de abrir el navegador.

## Script de auditoría

```python
import re
import glob

html = open('index.html').read()
html_ids = set(re.findall(r'id="([^"]+)"', html))

patterns = [
    r"getElementById\(['\"]([^'\"]+)['\"]\)",
    r"querySelector\(['\"]#([^'\"]+)['\"]\)",
    r"querySelectorAll\(['\"]#([^'\"]+)['\"]\)",
]

all_module_ids = set()
for jsfile in glob.glob('js/*.js'):
    js = open(jsfile).read()
    for pattern in patterns:
        ids = re.findall(pattern, js)
        for id_ in ids:
            if re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', id_) and len(id_) > 2:
                all_module_ids.add(id_)

missing = all_module_ids - html_ids

if missing:
    print(f"❌ {len(missing)} IDs faltantes:")
    for m in sorted(missing):
        print(f"  - {m}")
else:
    print("✅ Todos los IDs presentes")
```

## IDs dinámicos

Algunos IDs se generan dinámicamente (no están en HTML estático):
- `survey-form` → creado por `generateSurveyHTML()` al hacer clic en "Generar encuesta"
- `flota-item` → creado por `addFlotaItem()` al hacer clic en "Añadir vehículo"

**Regla:** Estos IDs NO deben estar en HTML estático. Pero el listener que los captura debe ejecutarse DESPUÉS de la inyección.

## localStorage audit

```python
ls_sets = set(re.findall(r"localStorage\.setItem\(['\"]([^'\"]+)['\"]", js))
ls_gets = set(re.findall(r"localStorage\.getItem\(['\"]([^'\"]+)['\"]", js))
for k in ls_sets:
    if k not in ls_gets:
        print(f"⚠️ '{k}' se SETea pero nunca se GETea")
```

## Canvas charts audit

```python
html_charts = set(re.findall(r'canvas id="([^"]+)"', html))
for jsfile in glob.glob('js/*.js'):
    js = open(jsfile).read()
    chart_gets = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js))
    for cid in html_charts:
        if cid not in chart_gets:
            print(f"⚠️ Canvas '{cid}' en HTML pero no buscado por JS")
```

## Estructura HTML verificada

```python
open_divs = html.count('<div')
close_divs = html.count('</div>')
open_forms = html.count('<form')
close_forms = html.count('</form>')
open_sections = html.count('<section')
close_sections = html.count('</section>')

assert open_divs == close_divs, f"divs: {open_divs} vs {close_divs}"
assert open_forms == close_forms, f"forms: {open_forms} vs {close_forms}"
assert open_sections == close_sections, f"sections: {open_sections} vs {close_sections}"
```

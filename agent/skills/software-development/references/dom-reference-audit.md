# DOM Reference Audit — Script de Auditoría

## Propósito
Cruzar TODOS los IDs buscados por `getElementById()` y `querySelector('#...')` de los módulos JS contra los IDs presentes en el HTML antes de desplegar.

## Script Python

```python
import re

# Leer HTML
html = open('/path/to/index.html').read()
html_ids = set(re.findall(r'id="([^"]+)"', html))

# Leer TODOS los módulos JS
module_files = [
    'js/main.js',
    'js/diagnostico.js',
    'js/dafo.js',
    'js/objetivos.js',
    'js/informe.js',
    'js/survey.js',
]

print("=== AUDITORÍA DE REFERENCIAS DOM ===\n")
all_ok = True

for mod in module_files:
    js = open(mod).read()
    # IDs buscados
    actual_ids = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js)
    query_ids = re.findall(r"querySelector\(['\"]#([^'\"]+)['\"]\)", js)
    all_ids = set(actual_ids + query_ids)
    
    missing = all_ids - html_ids
    if missing:
        print(f"❌ {mod}: IDs faltantes en HTML: {missing}")
        all_ok = False
    else:
        print(f"✅ {mod}: {len(all_ids)} IDs OK")

if all_ok:
    print("\n✅ TODAS LAS REFERENCIAS DOM CORRECTAS")
else:
    print("\n❌ HAY IDs QUE FALTAN EN EL HTML")
```

## Uso
```bash
python dom-audit.py
```

## Resultado esperado
Todos los módulos deben mostrar ✅. Si algún módulo muestra ❌, hay IDs que faltan en el HTML o que se renombraron.

## Pitfalls
- Los IDs que se generan **dinámicamente** (ej: `survey-form` creado por `generateSurveyHTML()`) NO pueden estar en el HTML estático. El script los detectará como faltantes, pero no son errores si se crean antes de ser buscados.
- Los canvas de Chart.js (`chart-modal`, `chart-co2e`, etc.) deben existir en el HTML y ser buscados por el módulo de gráficos.

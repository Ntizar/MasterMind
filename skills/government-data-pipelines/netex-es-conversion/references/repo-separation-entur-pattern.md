# Separación de monorepo en repos independientes — patrón Entur

## Contexto

Entur (Noruega) organiza sus proyectos NeTEx en repos separados: `netex-java-model` (modelo JAXB), `netex-validator-java` (validador), `netex-utils` (utilidades), `tiamat` (stop register). Cada repo es independiente con su propio README, LICENSE, CI y setup.

## Cuándo aplicar

- Un monorepo tiene componentes con responsabilidades claramente diferenciadas (spec, validador, convertidor ida, convertidor vuelta)
- Los componentes pueden usarse independientemente
- Quieres que cada componente tenga su propio README claro y su propia versión

## Patrón

### 1. Identificar componentes

```
Monorepo (Ntizar/netex)
├── spec/          → Repo 1: netex-es-spec
├── validator/     → Repo 2: netex-es-validator
├── converter/
│   ├── gtfs_reader.py    (modelo de datos — compartido)
│   ├── netex_writer.py   → Repo 3: gtfs-to-netex-es
│   ├── netex_reader.py   → Repo 4: netex-es-to-gtfs
│   └── gtfs_writer.py    → Repo 4: netex-es-to-gtfs
└── tests/         → Dividir según componente
```

### 2. Dependencias compartidas

En Python no hay paquetes Maven como en Java. Si dos repos necesitan el mismo modelo de datos (`gtfs_reader.py` con `GTFSFeed`, `Stop`, `Route`, etc.), se duplica en cada repo. Es un tradeoff: más mantenimiento vs independencia total.

Alternativa: crear un 5º repo `netex-es-model` como paquete pip instalable. Solo merece la pena si el modelo es grande y cambia frecuentemente.

### 3. Estructura de cada repo

```
netex-es-validator/
├── README.md          # Profesional, explica qué hace, cómo instalar, cómo usar
├── LICENSE            # MIT
├── .gitignore         # __pycache__/, *.pyc, .env
├── setup.py           # Instalable como paquete pip (entry_points para CLI)
├── validator/         # Código del componente
│   ├── __init__.py
│   ├── __main__.py    # python -m validator
│   ├── cli.py
│   ├── rules/
│   └── ...
└── tests/             # Tests del componente
    └── test_validator.py
```

### 4. README de cada repo

- Qué hace este componente específicamente
- Cómo instalarlo (dependencias mínimas)
- Cómo usarlo (CLI + API Python con ejemplos)
- Tabla de ecosistema: enlaces a los otros 3 repos
- Footer: "Hecho con ❤️ por David Antizar"

### 5. Crear repos en GitHub sin gh CLI

```python
import urllib.request, json

url = "https://api.github.com/user/repos"
data = json.dumps({
    "name": "netex-es-validator",
    "description": "Validador NeTEx-ES — 218 reglas en 18 módulos",
    "private": True,
    "auto_init": False
}).encode('utf-8')

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', f'token {GITHUB_TOKEN}')
req.add_header('Accept', 'application/vnd.github.v3+json')
resp = urllib.request.urlopen(req)
```

### 6. Push inicial

```bash
cd /tmp/repos/netex-es-validator
git init -b main
git add -A
git commit -m "netex-es-validator v3.5.0 - Validador NeTEx-ES"
git remote add origin https://{token}@github.com/Ntizar/netex-es-validator.git
git push -u origin main
```

### 7. Verificación independiente

Cada repo debe poder ejecutar sus tests sin el resto:
```bash
cd /tmp/repos/netex-es-validator
/opt/hermes/.venv/bin/python -m pytest tests/ -v
# 34 passed
```

## Pitfalls

- **Subagentes con rate limit:** Al delegar la creación de 3 repos en paralelo, 2 de 3 subagentes hicieron rate limit (HTTP 429). Hacer secuencial o con pausas si el modelo tiene rate limiting agresivo.
- **Branch `master` vs `main`:** `git init` puede crear `master` por defecto. Usar `git init -b main` o `git branch -m master main` antes del push.
- **`__pycache__` en el push:** Siempre limpiar antes de `git add -A` o tener `.gitignore` correcto.
- **Tests que dependen de test_samples:** Si los tests usan archivos de `test_samples/`, copiarlos al repo del tests, no solo el código.

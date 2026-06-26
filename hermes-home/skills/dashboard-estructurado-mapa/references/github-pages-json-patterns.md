# GitHub Pages y JSON — Patrones y pitfalls

## GitHub Pages NO sirve archivos .json

GitHub Pages devuelve 404 para archivos `.json` directamente. Soluciones:

### Opción 1: Datos embebidos en JS (recomendada para <1000 registros)
```javascript
// data.js — generado por pipeline
const REPORTS_DATA = [
  { id: "IF-41-2025", ... },
  ...
];
```
- Pros: Carga instantánea, sin CORS, sin fetch
- Contras: Repo más pesado, rebuild para cada cambio

### Opción 2: raw.githubusercontent.com
```javascript
fetch('https://raw.githubusercontent.com/USER/REPO/main/data/index.json')
```
- Pros: JSON real, versionado
- Contras: Latencia adicional, CORS funciona pero lento

### Opción 3: CDN con jsDelivr
```javascript
fetch('https://cdn.jsdelivr.net/gh/USER/REPO@main/data/index.json')
```
- Pros: Rápido, cacheado
- Contras: Retraso en actualizaciones (~5min)

### Opción 4: GitHub API (no recomendado para producción)
```javascript
fetch('https://api.github.com/repos/USER/REPO/contents/data/index.json')
  .then(r => r.json())
  .then(d => JSON.parse(atob(d.content)))
```
- Pros: Siempre actualizado
- Contras: Rate limit 60req/hora, lento

## Para colecciones grandes (>200 registros)

### JSON particionado por año
```
data/
├── index.json              ← ~50KB, metadatos mínimos
├── reports/
│   ├── 2009.json           ← Solo registros de 2009
│   ├── 2010.json
│   └── ...
└── relations.json          ← Cruzar entidades
```

**Flujo de carga:**
1. Cargar `index.json` una vez (para mapa + filtros)
2. Al hacer clic en un registro → cargar `reports/YYYY.json` solo si no está cacheado
3. `relations.json` se carga bajo demanda (al explore relaciones)

**Ventaja:** 50KB iniciales + lazy load = rápido incluso con 500+ registros.

## Sincronización JSON↔JS

Cuando los datos están embebidos en JS, mantener sincronización:

```bash
# Generar data.js desde index.json
python3 -c "
import json
with open('data/index.json') as f:
    data = json.load(f)
with open('js/data.js', 'w') as f:
    f.write(f'const REPORTS_DATA = {json.dumps(data, ensure_ascii=False)};\n')
"
```

**Pitfall:** No olvidar actualizar AMBOS archivos (JSON y JS) en cada cambio.

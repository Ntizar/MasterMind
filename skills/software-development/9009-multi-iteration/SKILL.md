---
name: 9009-multi-iteration
description: "Patrón genérico para ejecutar mejoras 9009 en múltiples iteraciones sobre cualquier proyecto — análisis rápido, plan de mejoras, implementación directa con patch/write_file, y verificación. Optimizado para ejecución directa (NO subagentes) en batches de 20 mejoras."
version: 1.0.0
author: Ntizar
tags: [software-development, 9009, improvement, iteration]

---

# 9009 Multi-Iteration — Mejora Continua Genérica

Patrón para ejecutar mejoras continuas en cualquier proyecto, con ejecución directa y múltiples iteraciones.

## 🎯 Cuándo usar

- Cuando el usuario pide "mejorar X proyecto" o "hacer Y procesos 9009"
- Cuando hay un proyecto existente que puede evolucionar
- Cuando se quiere un pipeline de mejora continua sin configurar cron

## ⚡ Patrón de ejecución (directo, NO subagentes)

### Regla de oro: Implementar directamente con patch/write_file

**Los subagentes FALLAN con timeout** en tareas de código extenso. Siempre implementar directamente.

### Flujo de 5 pasos:

```
1. Explorar proyecto → estructura, stack, archivos clave
2. Analizar → qué existe ya, qué falta, qué puede mejorarse
3. Planificar → lista de mejoras priorizadas (baja→alta dificultad)
4. Implementar → patch/write_file directo en archivos existentes
5. Commit + push → deploy automático si es NaN
```

### Paso 1: Exploración rápida

```bash
# Estructura
find . -not -path './.git/*' -not -path './node_modules/*' -not -path './__pycache__/*' | head -50

# Stack
cat package.json  # o pyproject.toml, Cargo.toml, requirements.txt

# Archivos principales
cat README.md
cat index.html  # o main.py, app.js, etc.
```

### Paso 2: Análisis de estado actual

Leer los archivos clave para saber qué ya existe:
- ¿Qué tabs/features ya están implementadas?
- ¿Qué endpoints existen?
- ¿Qué dependencias tiene el proyecto?
- ¿Hay tests? ¿Pasan?

### Paso 3: Generar plan de mejoras

Crear lista de mejoras priorizadas:
- **Baja dificultad primero** (victorias rápidas)
- **Mediana dificultad** después
- **Alta dificultad** al final

Cada mejora debe ser **atómica** (implementable en una sesión)

### Paso 4: Implementación directa

#### Patrón para proyectos frontend con tabs (esios-dashboard pattern):

**Nuevo endpoint backend:**
```javascript
// server.js — añadir ANTES del bloque "Start"
const { buildDominioSummary } = require('./src/domains/{dominio}/{dominio}.service');
app.get('/api/esios/{dominio}', async (req, res) => {
  const fecha = getRequestDate(req);
  const cacheKey = `{dominio}:${fecha}`;
  let data = cache.get(cacheKey);
  if (!data) {
    data = await buildDominioSummary(fecha, env.ESIOS_TOKEN);
    cache.set(cacheKey, data);
  }
  res.json(data);
});
```

**Nuevo servicio backend:**
```javascript
// src/domains/{dominio}/{dominio}.service.js
async function buildDominioSummary(fecha, token) {
  // Fetch datos externos o internos
  // Calcular stats
  // Devolver objeto con stats + datos horarios + resumen
}
module.exports = { buildDominioSummary };
```

**Nuevas tabs HTML:**
```html
<!-- index.html — añadir button en tabs -->
<button class="tab-btn" data-tab="{nombre}">🏷️ {Nombre}</button>

<!-- Añadir sección antes del footer -->
<div class="tab-section" id="section-{nombre}">
  <div class="metrics-grid" id="{nombre}Metrics">
    <div class="metric-card glass">
      <div class="metric-label">{Label}</div>
      <div class="metric-value" id="{nombre}Value">—</div>
    </div>
  </div>
  <div class="charts-grid">
    <div class="chart-card glass">
      <h3>{Gráfico}</h3>
      <div class="chart-wrapper"><canvas id="chart{Nombre}"></canvas></div>
    </div>
  </div>
</div>
```

**Nuevo archivo JS frontend:**
```javascript
// public/js/render-{dominio}.js
function render{Dominio}(data) {
  if (!data) return;
  // Actualizar métricas DOM
  // Crear/actualizar gráficos Chart.js
}

function cargarDatos{Dominio}() {
  fetch('/api/esios/{dominio}')
    .then(r => r.json())
    .then(data => render{Dominio}(data))
    .catch(err => console.warn('[{dominio}] Error:', err.message));
}
```

**Integrar en tab switching (ui.js):**
```javascript
// ui.js — dentro de setupTabs(), tras el bloque existente
if (tab === '{nombre}') cargarDatos{Dominio}();
```

**Incluir script en HTML (index.html):**
```html
<!-- Antes de </body> -->
<script src="js/render-{dominio}.js"></script>
```

#### Patrón para proyectos backend (Python/Node):

1. Crear módulo/servicio en `src/domains/{tema}/`
2. Añadir endpoints en `app.py` o `server.js`
3. Añadir tests en `tests/`
4. Commit + push

### Paso 5: Verificación y deploy

```bash
cd /root/workspace/{PROYECTO}
git add -A
git commit -m "9009: {descripción de la mejora}"
git push
```

## 🔍 Fuentes de datos externas sin API key

### Yahoo Finance
```javascript
// Sin API key, sin dependencias
const url = `https://query1.finance.yahoo.com/v8/finance/chart/${TICKER}?range=30d&interval=1d`;
// Parsear timestamps y quotes del JSON resultante
```

### ESIOS/REE
```javascript
// Usar convertEsiosValue() para normalizar unidades
const val = convertEsiosValue(indicatorId, rawValue);
```

## 📊 Correlación Pearson en JavaScript

```javascript
function calcularCorrelacionPearson(x, y) {
  const pairs = [];
  for (let i = 0; i < x.length; i++) {
    if (x[i] != null && y[i] != null) pairs.push([x[i], y[i]]);
  }
  if (pairs.length < 3) return null;

  const n = pairs.length;
  const sumX = pairs.reduce((s, p) => s + p[0], 0);
  const sumY = pairs.reduce((s, p) => s + p[1], 0);
  const sumXY = pairs.reduce((s, p) => s + p[0] * p[1], 0);
  const sumX2 = pairs.reduce((s, p) => s + p[0] * p[0], 0);
  const sumY2 = pairs.reduce((s, p) => s + p[1] * p[1], 0);

  const num = n * sumXY - sumX * sumY;
  const den = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
  if (den === 0) return null;
  return Math.round((num / den) * 100) / 100;
}

function interpretarCorrelacion(r) {
  if (r === null) return 'Sin datos';
  const abs = Math.abs(r);
  if (abs > 0.8) return 'Muy fuerte';
  if (abs > 0.6) return 'Fuerte';
  if (abs > 0.4) return 'Moderada';
  if (abs > 0.2) return 'Débil';
  return 'Muy débil / ninguna';
}
```

## 📋 Lista de mejoras típicas por tipo de proyecto

### Dashboard frontend (vanilla JS + Chart.js):
1. Exportar datos a CSV
2. Modo oscuro/claro
3. Heatmap de datos
4. Indicadores de tendencia (↑↓ %)
5. Zoom/pan en gráficos
6. Timestamp + enlace fuente
7. Comparativa día anterior
8. Performance ratio
9. Widget de clima/meteo
10. Tab de correlaciones
11. Gráficos de barras apiladas
12. Histogramas de distribución
13. Métricas de impacto/ahorro
14. Mapa SVG de datos geográficos
15. Panel debalancing/reservas

### Backend API (Node.js/Python):
1. Cache por fecha/timestamp
2. Endpoints nuevos por dominio
3. Servicios por dominio (separación de responsabilidades)
4. Validación de inputs
5. Manejo de errores centralizado
6. Health check endpoint
7. Rate limiting
8. Logging estructurado

### Análisis de datos:
1. Correlación Pearson entre variables
2. Estadísticas descriptivas (media, max, min, percentiles)
3. Series temporales
4. Predicciones simples (media móvil, tendencia lineal)
5. Normalización de unidades

## ⚠️ Pitfalls

1. **NUNCA usar subagentes** para código extenso — timeout seguro
2. **Chart.js:** destruir instancia previa con `charts.{nombre}?.destroy()` antes de `new Chart()`
3. **Patch vs write_file:** si el archivo es largo (>100 líneas) y el patch es grande, usar write_file completo
4. **Siempre leer el archivo completo** antes de patchear (no usar offset/limit)
5. **Git push siempre** después de commit para deploy en NaN
6. **Cache por fecha** para evitar llamadas duplicadas a APIs externas
7. **Carga lazy por tab** — solo cargar datos cuando el usuario cambia a esa tab
8. **Todo en castellano** — commits, notas, nombres de tabs, descripciones
9. **Verificar IDs de ESIOS antes de usarlos:** Los IDs 10035-10041 NO existen. ESIOS no tiene datos de temperatura/viento/humedad. Para clima usar Open-Meteo (ver `9009-mejora-continua:references/esios-no-clima-data.md`).
10. **SIEMPRE typecheck antes de push:** `npx vue-tsc --noEmit` (Vue) o `npx tsc --noEmit` (vanilla TS). Los tests pueden pasar pero el CI falla en typecheck. Ejecutar ambos: `npx vitest run && npx vue-tsc --noEmit` antes de commit+push.

## 🚀 Ejemplo de ejecución rápida

```
# 1. Explorar
find /root/workspace/{PROYECTO} -not -path '*/.git/*' -not -path '*/node_modules/*' | head -30
cat /root/workspace/{PROYECTO}/package.json

# 2. Leer archivos clave
read_file /root/workspace/{PROYECTO}/public/index.html
read_file /root/workspace/{PROYECTO}/server.js
read_file /root/workspace/{PROYECTO}/public/js/ui.js

# 3. Crear servicios nuevos
write_file /root/workspace/{PROYECTO}/src/domains/{dominio}/{dominio}.service.js

# 4. Añadir endpoints
patch /root/workspace/{PROYECTO}/server.js  # añadir antes de "Start"

# 5. Añadir tabs HTML
patch /root/workspace/{PROYECTO}/public/index.html  # añadir buttons + sections

# 6. Crear render JS
write_file /root/workspace/{PROYECTO}/public/js/render-{dominio}.js

# 7. Integrar en tab switching
patch /root/workspace/{PROYECTO}/public/js/ui.js

# 8. Incluir script en HTML
patch /root/workspace/{PROYECTO}/public/index.html  # añadir <script>

# 9. Commit + push
cd /root/workspace/{PROYECTO}
git add -A && git commit -m "9009: {dominio} - descripción" && git push
```

## 📚 Referencias

- `references/esios-dashboard-9009-pattern.md` — Patrón específico de esios-dashboard
- `mastermind:9009-mejora-continua` — Pipeline completo con cron
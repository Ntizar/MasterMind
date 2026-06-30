---
name: personal-tracking-database
version: "1.0.0"
description: "Patrón para construir sistemas de seguimiento personal con base de datos JSON estructurada + dashboard HTML interactivo + scripts de registro rápido. Reutilizable para dieta, finanzas, hábitos, productividad, etc."
tags: [tracking, database, json, dashboard, personal, patterns]
---

# Personal Tracking Database — Patrón de sistema de seguimiento

## Cuándo usarlo

El usuario quiere hacer seguimiento de algo personal (peso, dieta, finanzas, hábitos, deporte, sueño, etc.) y necesita:
- Una base de datos estructurada (no un markdown plano)
- Un dashboard visual para ver el progreso
- Scripts para registrar rápido
- Proyecciones o análisis

## Arquitectura estándar

```
/root/workspace/<proyecto>/
├── data/
│   └── database.json          ← Fuente de verdad única (JSON estructurado)
├── dashboard.html             ← Dashboard interactivo (Aurora + Chart.js)
├── scripts/
│   ├── registrar-<tipo1>.sh   ← Scripts de registro rápido
│   └── registrar-<tipo2>.sh
├── README.md
└── SEGUIMIENTO.md             ← Vista legible (generada, no editable)
```

## Principios

1. **JSON es la fuente de verdad** — nunca editar vistas generadas directamente
2. **Dashboard autocontenido** — un solo HTML que carga el JSON con fetch()
3. **Scripts de registro** — para cuando no hay dashboard abierto
4. **Aurora Design System** — para el dashboard (CDN, sin build)
5. **Chart.js** — para gráficos (vía CDN)
6. **Commit siempre** — cada cambio va a git

## Estructura JSON base

```json
{
  "meta": {
    "nombre": "Nombre del usuario",
    "fecha_inicio": "YYYY-MM-DD",
    "objetivo": "descripción",
    "version": "1.0.0"
  },
  "<entidad1>": [
    {"fecha": "YYYY-MM-DD", ...campos específicos...}
  ],
  "<entidad2>": [...]
}
```

### Reglas de diseño del JSON
- Arrays planos, no anidados (fáciles de filtrar con Array.filter)
- Fechas siempre en formato `YYYY-MM-DD`
- Sin valores null — usar 0 para numéricos, "" para strings
- `meta` siempre presente con versión semver

## Dashboard HTML — Plantilla

### Stack técnico
```html
<!-- Aurora CDN -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.next.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.data.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.ui.css">

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>

<!-- Body -->
<body class="nz" data-nz-theme="light" data-nz-skin="aurora">
```

### Secciones recomendadas
1. **KPIs principales** — valor actual, delta, objetivo (usar `.nz-kpi`, `.nz-stat-grid`)
2. **Gráfico de evolución** — línea temporal con Chart.js
3. **Desglose por categoría** — barras, donuts, según el dominio
4. **Proyecciones** — si aplica (3 ritmos: lento/medio/rápido)
5. **Timeline de eventos** — entrenamientos, hitos, etc.
6. **Resumen semanal** — tabla con métricas agregadas

### Patrón de carga de datos
```javascript
fetch('data/database.json')
  .then(r => r.json())
  .then(db => {
    renderDashboard(db);
  })
  .catch(err => {
    document.getElementById('loading').innerHTML =
      '<div class="nz-alert nz-alert--danger">Error cargando datos</div>';
  });
```

### Chart.js — Patrón seguro
```javascript
// Destruir chart anterior antes de crear nuevo
if (window.pesoChart) window.pesoChart.destroy();
window.pesoChart = new Chart(ctx, { ... });
```

## Scripts de registro — Patrón

Cada script debe:
1. Recibir datos como argumentos o pedirlos interactivamente
2. Leer database.json
3. Añadir el nuevo registro
4. Escribir database.json
5. Hacer git add + commit

```bash
#!/bin/bash
# registrar-ejemplo.sh — Registro rápido de [entidad]
# Uso: ./registrar-ejemplo.sh "2026-06-09" "valor" "notas"

DB="/root/workspace/proyecto/data/database.json"
TMP=$(mktemp)

python3 -c "
import json, sys
with open('$DB') as f:
    db = json.load(f)
db['entidad'].append({
    'fecha': sys.argv[1],
    'valor': float(sys.argv[2]),
    'notas': sys.argv[3] if len(sys.argv) > 3 else ''
})
with open('$DB', 'w') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)
" "$@"

cd /root/workspace/proyecto
git add data/database.json
git commit -m "Registro [entidad]: $(date +%Y-%m-%d)"
```

## Deploy en NaN — Actualización automática

Cuando el dashboard se deploya en NaN.builders, **cada push a GitHub triggera un redeploy automático** (polling cada 1-5 min). Esto permite actualizar datos sin tocar el dashboard:

### Flujo de actualización automática
1. **Actualizar `database.json`** con nuevos datos (por script, por chat, por API)
2. **`git add data/database.json && git commit -m "..."`**
3. **`git push origin main`** → NaN detecta cambio → reconstruye → redeploy
4. **Dashboard fresco** en `https://<app>-<owner>-<owner>.apps.nan.builders/`

### Dockerfile mínimo (Node.js + Express estático)
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --production
COPY . .
EXPOSE 5050
CMD ["node", "server.js"]
```

### server.js mínimo
```javascript
const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 5050;

app.use(express.static(path.join(__dirname)));
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'dashboard.html')));
app.listen(PORT, '0.0.0.0', () => console.log(`MastermindFit en puerto ${PORT}`));
```

### ⚠️ Pitfall: healthz endpoint
El server.js **debe incluir un endpoint `/healthz`** para que el HEALTHCHECK del Dockerfile funcione:
```javascript
app.get('/healthz', (req, res) => res.json({status: 'ok', uptime: process.uptime()}));
```
Sin él, NaN devuelve 404 en `/healthz` y el pod puede marcar el servicio como no saludable.

### Puerto
- Usar `process.env.PORT || 5050` como default
- El EXPOSE del Dockerfile debe coincidir con el puerto del espacio en NaN
- Ver skill `esios-nan-deploy` para detalles completos de deploy

## Proyecciones — Framework genérico

Cuando el sistema permite proyecciones (peso, ahorros, etc.):

### Técnica recomendada: regresión lineal (mínimos cuadrados)

Para calcular el ritmo real a partir de datos temporales con fluctuaciones diarias:

1. **Filtrar solo registros consistentes** — ej. solo pesajes de mañana (elimina ruido intra-día)
2. **Usar regresión lineal en vez de primer-último** — un simple `(first - last) / días` amplifica el ruido. La regresión lineal usa TODOS los puntos intermedios y da una tendencia robusta
3. **Multiplicar pendiente × 7** para obtener kg/semana

### Fórmula (mínimos cuadrados)

```javascript
function calcRitmoLineal(registros) {
  var datos = registros.filter(function(r){ return r.hora === 'mañana'; });
  if(datos.length < 2) return 0;
  var n = datos.length, sumX = 0, sumY = 0, sumXY = 0, sumXX = 0;
  var ref = new Date(datos[0].fecha);
  datos.forEach(function(d){
    var x = (new Date(d.fecha) - ref) / 86400000;
    sumX += x; sumY += d.peso_kg; sumXY += x*d.peso_kg; sumXX += x*x;
  });
  var pendiente = (n*sumXY - sumX*sumY) / (n*sumXX - sumX*sumX) || 0;
  return Math.max(0, -pendiente * 7); // kg/semana
}
```

### Escenarios de proyección

1. **Real (regresión lineal)** — calculado automáticamente de los datos reales
2. **Sostenible** — ritmo conservador
3. **Normal** — ritmo moderado
4. **Acelerado** — ritmo óptimo
5. **Agresivo** — ritmo máximo (solo para déficit extremo)

Siempre mostrar el real DESTACADO primero (morado/llamativo). Separar nítidamente los escenarios fijos del dato real.

### ⚠️ Pitfalls de proyecciones

- **`slice(-7)` NO son los últimos 7 días** — son las últimas 7 ENTRADAS. Si los datos son irregulares (saltos de días), usar la regresión lineal que considera TODOS los puntos, no solo 7
- **Datos con dos tomas/día** — si pesas mañana y tarde, filtrar solo mañana para consistencia. La regresión con dos puntos el mismo día infla artificialmente el dataset
- **Primera semana engaña** — los primeros días suelen tener mayor pérdida de agua. La regresión con más puntos suaviza este efecto
- **Mostrar número de semanas Y fecha concreta** — el usuario necesita visualizar cuándo llega
- **Poner el escenario real primero en la lista** — siempre debe ser el que ve nada más abrir

### Chart de proyecciones

```javascript
// Destruir anterior
if(charts.proyeccion) charts.proyeccion.destroy();
// Crear con datasets: real + 3-4 escenarios + línea objetivo
charts.proyeccion = new Chart(ctx, {
  type:'line',
  data:{labels:labels, datasets:[
    {label:'Real (regresión) X.XX kg/sem', data:dReal, borderColor:'#7c3aed', borderWidth:3,
     pointRadius:3, pointBackgroundColor:'#7c3aed'},
    // ... escenarios fijos ...
    {label:'Objetivo', data:Array(labels.length).fill(objetivo), borderColor:'#22c55e',
     borderDash:[8,4], pointRadius:0, borderWidth:2}
  ]}
});
```

La línea real debe ser la única con puntos visibles y trazo más grueso — resalta visualmente frente a las teóricas.

## Pitfalls

- **CORS en file://** — el dashboard necesita un servidor HTTP. Usar `python3 -m http.server`
- **Chart.js acumula instancias** — siempre destruir antes de recrear
- **JSON corrupto** — si el script de registro falla, el JSON puede quedar a medias. Usar escritura atómica (escribir a temp, luego renombrar)
- **Fechas inconsistentes** — forzar siempre YYYY-MM-DD, nunca DD/MM/YYYY ni timestamps
- **Git sin commit** — los scripts deben hacer commit automático, el usuario no se acuerda
- **Dashboard muy grande** — si el JSON crece mucho (>1MB), considerar lazy loading o paginación en el dashboard

## Referencias

- `references/dieta-dashboard-example.md` — Estructura real de database.json para MastermindFit (dieta+deporte+pasos)
- `references/linear-regression-projection.js` — Implementación completa de proyecciones con regresión lineal (helper + tabla + chart real)
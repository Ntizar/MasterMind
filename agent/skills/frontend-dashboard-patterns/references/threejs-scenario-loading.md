# Three.js — Escenarios JSON con Validación y Conversión de Parámetros

**Fecha de creación:** 2026-06-17  
**Proyecto:** WaveThree (Ntizar/WaveThree)  
**Contexto:** Conectar archivos JSON de escenarios de oleaje con un shader de océano Gerstner en Three.js.

## Problema

Un proyecto Three.js necesita cargar configuraciones de escena (parámetros de ola, viento, batimetría) desde archivos JSON en `data/scenarios/`. Los parámetros del JSON deben:
1. Validarse contra un schema esperado
2. Normalizarse a un formato consistente
3. Convertirse a parámetros del shader (Hs→amplitud, Tp→frecuencia, Dir→dirección)

## Solución — Patrón en 3 capas

### Capa 1: Schema de validación

```javascript
const REQUIRED_FIELDS = {
  id: 'string',
  label: 'string',
  location: 'string',
  time: 'string',
  wave: { hs: 'number', tp: 'number', dir: 'number' },
  wind: { speed: 'number', dir: 'number' },
};

function validateScenario(data) {
  const errors = [];
  // Validar campos escalares
  for (const [field, type] of Object.entries(REQUIRED_FIELDS)) {
    if (typeof type === 'string') {
      if (!(field in data) || typeof data[field] !== type) {
        errors.push(`Campo requerido: ${field} (${type})`);
      }
    } else {
      // Objeto anidado (wave, wind)
      if (!data[field] || typeof data[field] !== 'object') {
        errors.push(`Campo requerido: ${field} (objeto)`);
      } else {
        for (const [subField, subType] of Object.entries(type)) {
          if (!(subField in data[field]) || typeof data[field][subField] !== subType) {
            errors.push(`Campo requerido: ${field}.${subField} (${subType})`);
          }
        }
      }
    }
  }
  // Validaciones de rango
  if (data.wave) {
    if (data.wave.hs < 0 || data.wave.hs > 25) errors.push('Hs debe estar entre 0 y 25 m');
    if (data.wave.tp < 0 || data.wave.tp > 30) errors.push('Tp debe estar entre 0 y 30 s');
    if (data.wave.dir < 0 || data.wave.dir > 360) errors.push('Dir debe estar entre 0 y 360°');
  }
  if (data.wind) {
    if (data.wind.speed < 0 || data.wind.speed > 60) errors.push('Viento entre 0 y 60 m/s');
  }
  return { valid: errors.length === 0, errors };
}
```

### Capa 2: Normalización

```javascript
function normalizeScenario(raw) {
  return {
    id: raw.id,
    label: raw.label || raw.id,
    location: raw.location || 'Desconocida',
    time: raw.time || new Date().toISOString(),
    wave: {
      hs: raw.wave.hs,
      tp: raw.wave.tp,
      dir: raw.wave.dir,
      notes: raw.wave.notes || '',
    },
    wind: {
      speed: raw.wind.speed,
      dir: raw.wind.dir,
      notes: raw.wind.notes || '',
    },
    bathymetry: raw.bathymetry || null,
    structure: raw.structure || null,
  };
}
```

### Capa 3: Conversión a wave params

```javascript
function scenarioToWaveParams(scenario) {
  const { wave, wind } = scenario;
  return {
    amplitude: wave.hs,              // Hs → amplitud directa
    frequency: 1 / wave.tp,          // Tp → frecuencia (Hz)
    direction: wave.dir,             // Dirección en grados
    windSpeed: wind.speed,
    windDir: wind.dir,
  };
}
```

## Carga de lista de escenarios

Como el navegador no puede hacer `readdir` del filesystem, se usa una lista hardcodeada de IDs conocidos:

```javascript
export async function loadScenariosList(basePath = '../../data/scenarios') {
  const knownScenarios = [
    'temporal_2026_01_17_1200',
    'swell_atlantic',
    'calm_day',
    'storm_extreme',
  ];

  const results = [];
  for (const id of knownScenarios) {
    try {
      const url = `${basePath}/${id}.json`;
      const sc = await loadScenario(url);
      results.push({
        id: sc.id,
        label: sc.label,
        location: sc.location,
        time: sc.time,
      });
    } catch (err) {
      console.warn(`⚠️ Escenario omitido: ${id} — ${err.message}`);
    }
  }
  return results;
}
```

## Formato JSON de escenario

```json
{
  "id": "swell_atlantic",
  "label": "Mar de fondo atlántico",
  "location": "Cantábrico",
  "time": "2026-03-15T08:00:00Z",
  "wave": { "hs": 1.8, "tp": 12.5, "dir": 310 },
  "wind": { "speed": 5.0, "dir": 10 }
}
```

## Uso en main.js

```javascript
// 1. Cargar lista al inicio
const scenarios = await loadScenariosList();
populateScenarioSelector(scenarios);

// 2. Cargar primer escenario por defecto
await selectScenario(scenarios[0].id);

// 3. Al cambiar en el dropdown
document.getElementById('scenario-select').addEventListener('change', async (e) => {
  await selectScenario(e.target.value);
});

// 4. selectScenario conecta todo
async function selectScenario(id) {
  const sc = await loadScenarioFromId(id);
  const params = scenarioToWaveParams(sc);
  state.params.amplitude = params.amplitude;
  state.params.frequency = params.frequency;
  state.params.direction = params.direction;
  ocean.update(0, state.params);
  updateSliderLabels();
  updateScenarioMeta(sc);
}
```

## Mapeo de parámetros

| Campo JSON | Significado | Conversión | Parámetro shader |
|---|---|---|---|
| `wave.hs` | Altura significativa (m) | Directo | `amplitude` |
| `wave.tp` | Periodo pico (s) | `1/Tp` | `frequency` |
| `wave.dir` | Dirección (grados) | Directo | `direction` |
| `wind.speed` | Velocidad viento (m/s) | Directo | `windSpeed` |
| `wind.dir` | Dirección viento (grados) | Directo | `windDir` |

## Pitfalls

- **No usar `readdir` en el navegador** — el browser no tiene acceso al filesystem. Usar lista hardcodeada de IDs conocidos.
- **Validar ANTES de normalizar** — si el JSON tiene campos faltantes, la normalización puede crear objetos con `undefined`.
- **Rutas relativas** — `../../data/scenarios/` funciona con Vite alias `@data`, pero en deploy estático puede necesitar ajuste.
- **Error silencioso en `loadScenariosList`** — los escenarios que fallan se omiten con `console.warn`, no se lanzan excepciones. Esto permite que el selector se populatede solo con los escenarios válidos.
- **`ocean.update(t, params)` con params** — si no se pasan los params nuevos, el shader no se actualiza. Siempre llamar `ocean.update(t, state.params)` cuando los parámetros cambian.

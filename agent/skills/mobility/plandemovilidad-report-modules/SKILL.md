---
name: plandemovilidad-report-modules
description: Guía de la estructura modular del generador de informe PMST/PTST. Cómo navegar, crear/modificar capítulos, y entender el flujo de datos en js/report/
---

# PLANDEMOVILIDAD — Módulos del Informe (report/)

## Estructura de js/report/

```
js/report/
├── helpers.js      ← CONSTANTES + funciones compartidas (fmt, pct, safe, getCO2e...)
├── css.js          ← getCSS() — CSS embebido para el informe A4
├── index.js        ← Orquestador: generarInformeCompleto(app)
├── 00-portada.js   ← Portada con gradient azul
├── 01-indice.js    ← Índice de capítulos (no recibe app, solo genera HTML)
├── 02-resumen-ejecutivo.js
├── 03-marco-legal.js   ← No recibe app (información fija normativa)
├── 04-metodologia.js
├── 05-analisis-entorno.js
├── 06-caracterizacion-centro.js
├── 07-caracterizacion-empresa.js
├── 08-resultados-encuesta.js    ← 252 líneas (más de 200, pendiente refactor)
├── 09-reparto-modal.js
├── 10-distancias-tiempos.js
├── 11-huella-carbono.js
├── 12-aparcamiento.js
├── 13-transporte-publico.js
├── 14-infraestructura-ciclista.js
├── 15-analisis-dafo.js
├── 16-objetivos-smart.js
├── 17-plan-medidas.js
├── 18-plan-seguimiento.js
├── 19-cronograma.js
├── 20-presupuesto.js
└── 21-conclusiones.js
```

## Cómo se relacionan

```
helpers.js ←─── css.js              (sin dependencias)
     ↑                ↑
     └─── 00*.js ──┐  │
     └─── 01*.js ──┘  │
     └─── 02*.js ─────┘  (cada capítulo importa helpers)
     └─── ...            (cada capítulo importa helpers)
     └─── 21*.js ───────┘
              │
              ↓
          index.js ←─── helpers.js + css.js + todos los capítulos
              │
              ↓
          report.js (shim re-export)
```

## Cómo AÑADIR un nuevo capítulo

1. Crear `js/report/22-mi-capítulo.js`:
```js
import { fmt, pct, safe, safeNum, getCO2e, getResumen } from './helpers.js';

export function generarMiCapítulo(app) {
    // ... HTML template string
    return `<div class="chapter" id="chapter-22">...</div>`;
}
```

2. Añadir import en `js/report/index.js`:
```js
import { generarMiCapítulo } from './22-mi-capítulo.js';
```

3. Añadir llamada en `generarInformeCompleto()`:
```js
<!-- CAPÍTULO 22: MI CAPÍTULO -->
${generarMiCapítulo(app)}
```

## Cómo MODIFICAR un capítulo existente

Simplemente editar el archivo `.js` correspondiente en `js/report/`. Cada capítulo es autónomo — modificar uno no afecta a los demás.

## Si un capítulo crece > 200 líneas

Extraer sub-funciones internas al mismo archivo (no exportadas), o crear un helper inline:

```js
// helpers internos del capítulo (no exportados)
function calcularMetricas(app) { ... }
function generarTablaResumen(data) { ... }

export function generarCapítulo(app) {
    const metricas = calcularMetricas(app);
    return `...${generarTablaResumen(metricas)}...`;
}
```

## Si la función necesita datos que no están en helpers

Añadir la función a `helpers.js` SOLO si es usada por 2+ capítulos. Si es de un solo capítulo, mantenerla inline.

## Convenciones de nombres

- Archivos: `NN-nombre-con-guiones.js`
- Funciones exportadas: `generarNombreCapítulo(app)`
- Funciones helpers inline: `calcularX`, `generarY`, `formatZ`
- Variables de HTML: usar template literals con `${}`
- Clases CSS: usar clases predefinidas (ver skill plandemovilidad-patterns)

## Excepciones

- Capítulos 01 (índice) y 03 (marco legal) NO reciben `app` — son estáticos.
- Los demás capítulos reciben `app` y acceden a datos con `safe()`, `safeNum()`, `safeArr()`.
- helpers.js y css.js NO importan nada de otros módulos.
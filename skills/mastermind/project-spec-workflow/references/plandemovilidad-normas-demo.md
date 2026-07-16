# NORMAS.md — Ejemplo real: PLANDEMOVILIDAD v2.0

> Generado durante la Fase 1 (CSS fix) del rewrite de PLANDEMOVILIDAD.
> Archivo original: `https://github.com/Ntizar/PLANDEMOVILIDAD/blob/main/NORMAS.md`

## Estructura utilizada

El NORMAS.md tiene 224 líneas y 5 secciones:

1. **SAGRADO** — 8 archivos/áreas protegidos
2. **MODIFICABLE** — 4 archivos con protocolo de 5 pasos
3. **LIBRE** — 10 categorías de archivos nuevos
4. **REGLAS GENERALES** — CSS, JS, HTML, módulos, estado, atribución
5. **PROCESO DE CAMBIO** — 6-step checklist + grafo de dependencias

## Archivos SAGRADOS (ejemplo)

| Archivo | Razón |
|---------|-------|
| `css/style.css` | Alineado con HTML tras Phase 1 fix |
| `index.html` | Estructura DOM completa, 1062 líneas |
| `js/config.js` | Constantes, endpoints API, factores emisión MITECO |
| `js/utils.js` | Funciones puras sin dependencias |
| `js/graficas.js` | Chart.js, referencia canvas IDs específicos |
| `js/export.js` | PDF/DOCX/ZIP con atribución |
| CDN imports | Leaflet 1.9.4, Chart.js 4.4, JSZip 3.10 |
| `window.pmstApp` | Namespace global, HTML lo llama vía onclick |

## Archivos MODIFICABLES (ejemplo)

| Archivo | Por qué es delicado |
|---------|---------------------|
| `js/app.js` | Orquestador: inicializa todo, conecta módulos |
| `js/mapa.js` | Leaflet: isocronas, capas, markers |
| `js/diagnostico.js` | Cálculos: reparto modal, CO2e, KPIs |
| `js/survey.js` | Encuesta: RGPD, IndexedDB, validación |

## Reglas generales documentadas

- CSS: selectores por clase, NUNCA IDs para styling
- JS: exponer en `window.pmstApp` si HTML llama vía onclick
- HTML: no renombrar clases/IDs sin actualizar CSS
- Módulos: importar en index.html si es nuevo
- Estado: `window.pmstApp.appState` como fuente única
- Atribución: `'Hecho con ❤️ por David Antizar'` en exports

## Grafo de dependencias

```
index.html → css/style.css (selectores de clase)
index.html → js/app.js (onclick → window.pmstApp)
index.html → CDN: Leaflet, Chart.js, JSZip

js/app.js → js/config.js (import { CONFIG })
js/app.js → js/utils.js (utilidades)
js/app.js → js/graficas.js (crear gráficas)
js/app.js → js/mapa.js (iniciar mapa)
js/app.js → js/diagnostico.js (calcular indicadores)
js/app.js → js/export.js (generar documentos)

js/graficas.js → index.html canvas IDs
js/mapa.js → index.html div IDs
js/export.js → js/app.js (leer appState)
```

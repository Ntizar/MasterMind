# DataHub España — SPEC

> **Generado por:** Mastermind con skill `project-spec-workflow`
> **Fecha:** 2026-07-08
> **Propósito:** Documentar la arquitectura objetivo para estabilizar el proyecto y permitir iteraciones sin regresiones.

---

## Visión

Panel de datos en tiempo real de España: 17 pestañas, 30+ gráficos, 12+ APIs, mapa base IGN. Todo client-side, deploy en GitHub Pages.

## Alcance

### Sí hace
- Visualización de datos de España en 17 pestañas temáticas
- Mapa base IGN con capas (gris, topográfico, ortofoto)
- Click en provincia → sincronización de datos entre pestañas
- Gráficos Chart.js (línea, barra, doughnut, scatter)
- Fetch en vivo de APIs: Open-Meteo, ESIOS, USGS, INE, DGT, GBFS, Puertos del Estado
- Datos estáticos: embalses, DGT, demografía, catastro
- Reloj en vivo, indicador de actualización

### NO hace (non-goals)
- No tiene backend (todo client-side, proxy mínimo para CORS)
- No tiene login/usuarios
- No tiene modo offline
- No guarda favoritos ni preferencias de usuario
- No tiene notificaciones push
- No exporta datos (futuro)

## Pantallas

### Estructura: SPA con tabs
1. **Panel principal** — resumen nacional (energía, clima, población)
2. **Energía** — generación, demanda, precios, intercambios (ESIOS/REE)
3. **Clima** — temperatura, precipitación, viento por provincia (Open-Meteo)
4. **Agua** — niveles de embalses por cuenca
5. **Economía** — BOE/BORME, tipos de interés
6. **Economía Detallada** — indicadores INE
7. **Demografía** — población, densidad por provincia
8. **Población** — pirámide poblacional, evolución
9. **Bicicletas** — sistemas GBFS por ciudad
10. **Puertos** — tráfico portuario en vivo
11. **Ambiente** — calidad del aire, espacios naturales
12. **Catastro** — datos del Catastro por municipio
13. **Calidad Aire** — EEA / Open-Meteo AQ
14. **Terremotos** — USGS FDSNWS en tiempo real
15. **Tráfico DGT** — radares, ZBE
16. **Polen** — niveles de polen por provincia
17. **Inundaciones** — alertas de inundación

## Datos

| Fuente | Tipo | Actualización | Volumen |
|--------|------|---------------|---------|
| Open-Meteo (weather) | API REST | Tiempo real | 50 provincias |
| Open-Meteo (marine) | API REST | Tiempo real | Costas |
| Open-Meteo (air-quality) | API REST | Tiempo real | 50 provincias |
| Open-Meteo (flood) | API REST | Tiempo real | Nacional |
| Open-Meteo (soil) | API REST | Tiempo real | 50 provincias |
| Open-Meteo (pollen) | API REST | Diario | 50 provincias |
| ESIOS/REE | API REST (proxy) | Tiempo real | Nacional |
| USGS FDSNWS | API REST | Tiempo real | Nacional |
| INE | API REST | Bajo demanda | Nacional |
| DGT/NAP | JSON local + CKAN | Diario | Nacional |
| GBFS | API REST | Tiempo real | 68 sistemas |
| Puertos del Estado | API REST | Tiempo real | 28 puertos |
| Embalses | JSON local | Actualizado | 400+ embalses |
| Catastro (DGC) | API REST | On-demand | Por municipio |
| EEA Aire | API REST | Tiempo real | Estaciones |

## Arquitectura

### Estado actual (PROBLEMA)

```
index.html (11.538 líneas, 588KB)
├── 151 funciones inline
├── 62 fetch calls dispersos
├── 31 event listeners
├── HTML + CSS + JS todo mezclado
└── js/datahub.js (9.3KB) — solo factory Open-Meteo
```

**Problemas:**
- Monolito imposible de iterar sin romper
- Cada cambio toca 500+ líneas colindantes
- No se puede delegar trabajo en paralelo
- Bugs se acumulan en capas
- Imposible testear partes aisladas

### Arquitectura objetivo

```
DataHubEspana/
├── SPEC.md                    ← Este documento
├── index.html                 ← Solo estructura DOM + imports (<200 líneas)
├── css/
│   └── styles.css             ← Todos los estilos
├── js/
│   ├── state.js               ← Estado global + carga de datos
│   ├── api.js                 ← Fetch de todas las APIs
│   ├── map.js                 ← Mapa IGN (init, layers, provincia click)
│   ├── charts.js              ← Factory de gráficos Chart.js
│   ├── tabs.js                ← Gestión de pestañas + lazy render
│   ├── ui.js                  ← Panels, eventos, reloj, indicadores
│   ├── panels/
│   │   ├── energia.js         ← Lógica pestaña energía
│   │   ├── clima.js           ← Lógica pestaña clima
│   │   ├── agua.js            ← Lógica pestaña agua
│   │   ├── economia.js        ← Lógica pestaña economía
│   │   ├── demografia.js      ← Lógica pestaña demografía
│   │   ├── gbfs.js            ← Lógica pestaña bicicletas
│   │   ├── puertos.js         ← Lógica pestaña puertos
│   │   ├── ambiente.js        ← Lógica pestaña ambiente
│   │   ├── catastro.js        ← Lógica pestaña catastro
│   │   ├── calidad-aire.js   ← Lógica pestaña calidad aire
│   │   ├── terremotos.js      ← Lógica pestaña terremotos
│   │   ├── trafico.js         ← Lógica pestaña tráfico DGT
│   │   ├── polen.js           ← Lógica pestaña polen
│   │   └── inundaciones.js    ← Lógica pestaña inundaciones
│   └── main.js                ← Orquestador: init + wiring
├── data/
│   ├── geo/                   ← GeoJSON provincias (lazy load)
│   ├── dgt/                   ← Datos DGT (radares, ZBE)
│   ├── embalses/              ← Niveles de embalses
│   └── ...
├── proxy/                     ← Proxy mínimo para CORS (ESIOS)
└── README.md                  ← Docs generadas desde SPEC
```

### Capas y responsabilidades

| Capa | Archivo | Responsabilidad | NO hace |
|------|---------|----------------|---------|
| **Estado** | state.js | Estado global, flags de carga, datos cacheados | No renderiza, no hace fetch |
| **API** | api.js | Fetch de APIs, normalización de respuestas, error handling | No guarda estado, no renderiza |
| **Mapa** | map.js | Init Leaflet, capas IGN, click provincia, markers | No hace fetch, no gestiona tabs |
| **Gráficos** | charts.js | Factory Chart.js (crear, actualizar, destruir) | No hace fetch, no gestiona estado |
| **Tabs** | tabs.js | switchTab(), lazy render, flags _loaded | No renderiza contenido de tab |
| **UI** | ui.js | Reloj, indicadores, panels, eventos genéricos | No hace lógica de datos |
| **Panel** | panels/*.js | Lógica específica de cada pestaña | No toca otras pestañas |
| **Main** | main.js | Init, wiring, orquestación | No tiene lógica propia |

### Estado global

```javascript
// state.js — ÚNICA fuente de verdad del estado
const Estado = {
  // Datos
  datos: {
    provincias: null,        // GeoJSON cargado
    provinciaSeleccionada: null,  // ID de provincia activa
    clima: {},                // cache por provincia
    energia: null,           // datos ESIOS
    embalses: null,
    // ... un campo por fuente de datos
  },
  // UI
  ui: {
    tabActiva: 'panel',
    mapa: null,               // instancia Leaflet
    charts: {},               // { id: Chart instance }
    cargando: false,
  },
  // Flags de carga (lazy)
  cargado: {
    geo: false,
    energia: false,
    clima: false,
    // un flag por pestaña
  }
};
```

**Regla:** Ningún otro archivo modifica `Estado` directamente. Usan funciones de `state.js`: `setDato(clave, valor)`, `getDato(clave)`, `setTabActiva(id)`.

### Interfaces entre módulos

```
state.js expone:
  - Estado (objeto global)
  - setDato(clave, valor)
  - getDato(clave)
  - setTabActiva(id)
  - marcarCargado(modulo)

api.js expone:
  - fetchClima(provinciaId) → Promise<datos>
  - fetchEnergia() → Promise<datos>
  - fetchEmbalses() → Promise<datos>
  - ... (una función por API)

map.js expone:
  - initMapa(container)
  - setCapaIGN(tipo)  // 'gris' | 'topo' | 'orto'
  - onProvinciaClick(callback)
  - highlightProvincia(id)
  - clearHighlight()

charts.js expone:
  - crearChart(containerId, config) → Chart
  - actualizarChart(id, datos)
  - destruirChart(id)
  - destruirTodos()

tabs.js expone:
  - switchTab(id)
  - getTabActiva()
  - onTabChange(callback)

panels/*.js exponen:
  - init[Panel]()  // se llama una vez
  - render[Panel](provinciaId)  // se llama al cambiar provincia
  - unload[Panel]()  // opcional: cleanup
```

## Stack

- **Frontend:** Vanilla JS (sin framework), Leaflet 1.9.4, Chart.js 4.4.4, TopoJSON
- **Mapa:** IGN WMTS (gris, topográfico, ortofoto)
- **CSS:** Estilo Aurora Ntizar (azul #2563eb + naranja #f97316, liquid glass, bento grid)
- **Deploy:** GitHub Pages (estático, build_type: workflow)
- **Proxy:** Mínimo para CORS (ESIOS)

## Criterios de éxito

- Carga inicial < 3s con 17 pestañas registradas
- Click en provincia → sincronización < 500ms
- Switch de tab → render < 300ms (lazy load)
- Sin console errors en carga
- Funciona en móvil (responsive)
- Cada pestaña se puede testear/editar independientemente

## Anti-patrones (lo que evitamos)

- ❌ **Monolito index.html** — 11K líneas en un archivo es inmanejable
- ❌ **Estado global esparcido** — variables sueltas en scope global
- ❌ **`var charts = {}` sin `window.`** — pitfall conocido (ver SOUL.md)
- ❌ **`buildSummary()` recursivo** — causa OOM en NaN (ver SOUL.md)
- ❌ **Tab lazy-rendered marcada antes de tiempo** — solo marcar al terminar fetch (ver SOUL.md)
- ❌ **ESIOS `time_trunc=hour` suma, no promedia** — usar `convertEsiosValue()` (ver SOUL.md)
- ❌ **Fetch sin error handling** — toda llamada a API debe tener try/catch
- ❌ **Funciones de 200+ líneas** — si una función pasa de 50 líneas, trocearla

## Plan de extracción (monolito → modular)

### Fase 0: Backup
- Crear branch `refactor-modular` desde main
- Verificar que todo funciona antes de empezar

### Fase 1: Extracción CSS
- Sacar todo `<style>` de index.html → css/styles.css
- Verificar que visualmente no cambia nada
- Commit

### Fase 2: Extracción de estado
- Identificar todas las variables de estado global
- Crear state.js con el objeto Estado
- Reemplazar referencias en index.html
- Verificar que todo funciona
- Commit

### Fase 3: Extracción de API
- Identificar los 62 fetch calls
- Agrupar por fuente de datos
- Crear api.js con funciones por fuente
- Reemplazar fetch calls inline por llamadas a api.js
- Commit

### Fase 4: Extracción de mapa
- Sacar toda la lógica de Leaflet a map.js
- Exponer initMapa, setCapaIGN, onProvinciaClick
- Commit

### Fase 5: Extracción de gráficos
- Sacar toda la lógica de Chart.js a charts.js
- Exponer crearChart, actualizarChart, destruirChart
- Commit

### Fase 6: Extracción de tabs
- Sacar switchTab y lógica de pestañas a tabs.js
- Implementar lazy render con flags _loaded
- Commit

### Fase 7: Extracción de panels (uno por uno)
- Por cada pestaña (17 total):
  1. Identificar funciones que pertenecen a esa pestaña
  2. Crear panels/[nombre].js
  3. Mover funciones
  4. Verificar que esa pestaña funciona
  5. Commit
- **Importante:** Una pestaña por commit. Si algo rompe, revertir solo ese commit.

### Fase 8: Limpieza
- index.html debe quedar < 200 líneas (solo DOM + imports)
- Verificar que todo funciona end-to-end
- Merge a main
- Commit final

## Referencias

- **Proyectos similares del usuario:** GTFSSpain (visor transporte), GBFSSpain (visor bicicletas)
- **Skill de referencia:** `project-spec-workflow` (este documento es una demo de ese skill)
- **Skill de patrones:** `frontend-dashboard-patterns` (patrones de dashboard vanilla JS)
- **Design system:** Aurora Ntizar v5.2 (azul #2563eb + naranja #f97316, liquid glass)
- **Repo:** Ntizar/DataHubEspana
- **Pages:** https://ntizar.github.io/DataHubEspana/

---

*Hecho con ❤️ por David Antizar — Mastermind es ejecutor, David es autor.*

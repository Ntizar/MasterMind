---
name: navara-3d-globe-engine
version: "1.0.0"
description: "Use con Navara, el motor de globo 3D de MapLibre."
tags: [navara, maplibre, threejs, wasm, rust, geospatial, 3d-maps, globe, gis, 3d-tiles, vector-tiles]
related_skills: [threejs-3d-maps, photorealistic-3d-tiles-threejs, cesium-3d-tiles-vector-data, map33-js, espanatlas-architecture]
---

# Navara — motor de globo 3D extensible (MapLibre)

## Resumen

**Navara** (`maplibre/navara`, ~260⭐ en 2026-09-03, creado como `reearth/navara` y donado a la org MapLibre) resuelve el dilema clásico de los motores de mapa web: los declarativos fáciles de usar son difíciles de extender, y los de control profundo exigen pericia enorme. Lo hace con una **API en 4 niveles** sobre un mismo motor:

1. **Declarative** — fuentes y capas como objetos de configuración planos (basemaps, terrain, datos vectoriales, 3D Tiles). Mallas, efectos y luces también.
2. **Plugin** — bundles de funcionalidad lista: escena fotorrealista, modo paseo en primera persona, overlays DOM, UI de atribución. Cualquiera puede empaquetar y compartir el suyo.
3. **API** — estilar por atributo de feature (`FeatureEvaluator`), picking, muestreo de terrain, control de cámara y utilidades geodésicas/ECEF **usables sin el motor de mapa**.
4. **Shader** — acceso total al render engine: shaders y efectos propios contra su scene graph y pipeline.

Arquitectura clave: **núcleo GIS headless en Rust → WebAssembly** (parseo de datos, construcción de geometría, tile management, LOD, indexación espacial), con el dibujo delegado a Three.js — la capa de render es intercambiable a propósito.

## Cuándo usar

- Globo 3D completo en el navegador (no solo plano): imagery + terrain + 3D city models + vectores, todo apilable
- Basemap limpio para visualización de datos con estilo por atributo, o escena fotorrealista con atmósfera/sol/sombras — cambiando de nivel de API, no de librería
- Sustituto natural de CesiumJS en proyectos que quieren three.js: España Atlas, visores GTFS 3D, dashboards geoespaciales
- Utilidades geodésicas/ECEF sueltas sin arrancar el mapa

Para tiles 2D proyectados planos + extrusión GeoJSON sigue siendo más ligero `threejs-3d-maps`; para ciudades fotorrealistas con Google 3D Tiles vía Ion, `photorealistic-3d-tiles-threejs`. Navara es el término medio: motor GIS serio + render three.js + globo real.

## Instalación y ejemplo mínimo (verificado en docs oficiales)

```bash
npm install @navaramap/three @navaramap/three-default-plugin three postprocessing
```

```typescript
import ThreeView from "@navaramap/three";
import { DefaultPlugin } from "@navaramap/three-default-plugin";

const view = new ThreeView({ useNormal: true }); // useNormal: needed si no hay terrain/hillshade
const defaultPlugin = new DefaultPlugin();
view.addPlugin(defaultPlugin);   // registrar plugins ANTES de init()

await view.init();               // arranca el motor WASM + Web Workers — asíncrono, antes de capas

defaultPlugin.addDefaultPhotorealScene();       // cielo, estrellas, sol, atmósfera en una llamada
view.atmosphere.date = new Date("2026-07-16T01:00:00Z"); // SIEMPRE UTC string → misma escena en cualquier máquina
view.toneMappingExposure = 10;

const raster = view.addSource({           // fuente raster WMTS-compatible GoogleMaps
  type: "raster-tile",
  url: "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_NextGeneration/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg",
  maxZoom: 8,
});
view.addLayer({ type: "raster", source: raster, raster: {} });

view.attribution?.add([{ attributionHtml: "Imagery © NASA EOSDIS GIBS" }]);

// moverse: view.setCamera() salto instantáneo · view.flyTo() transición animada
```

`<body style="margin:0; width:100%; height:100%; overflow:hidden">` — Navara crea un canvas a viewport.

Docs: https://navara.world/docs/ · Ejemplos vivos (clouds, fog+light, elevation-heatmap, SSR sobre agua): https://navara.world/examples/

## Integración con proyectos de David

- **Tiles España**: las fuentes `raster-tile` aceptan plantillas `{z}/{y}/{x}` estilo WMTS GoogleMapsCompatible → los WMTS del IGN Base (epsg3857, `image/jpeg`, CC BY 4.0) encajan como fuente raster gratuita; **verificar antes de fiarse** (formato de URL WMTS del IGN vs plantilla). Atribución con `view.attribution.add()` — patrón IGN obligatorio.
- **Licencia**: Apache-2.0 OR MIT — sin coste, alineado con "herramientas SOLO gratuitas".
- **Estilo/escena**: `addDefaultPhotorealScene()` da atmósfera y sol para los renders espectaculares tipo España Atlas sin escribir shaders.
- **Skill oficial del propio repo**: `skills/navara-usage` (en `maplibre/navara/tree/main/skills/navara-usage`) — guía de buenas prácticas para agentes IA: orden de setup, errores comunes de API y escenas de ejemplo. Copiarla al proyecto cuando se trabaje con Navara.

## Contribuir / desarrollar desde el repo

```bash
# toolchain: Rust stable, Node LTS, pnpm
cargo install cargo-make && cargo install cargo-watch
cargo install wasm-bindgen-cli --version 0.2.126   # versión fijada
rustup component add rust-src                       # builds WASM de release (build-std)
cargo make prepare   # primera vez
cargo make dev       # hot-reload (el primer error del navegador es normal: WASM aún compila)
cargo make web       # alternativa: trabajo solo en el lado web
```

## Pitfalls

- **Orden estricto**: plugins → `await view.init()` → capas. Añadir capas antes de `init()` o registrar plugins después falla; `init()` levanta el WASM y los Web Workers.
- **`useNormal: true`** solo es necesario si la escena NO tiene terrain/hillshade (esas capas ya aportan sus normales).
- **Fecha del sol en UTC string** (`"...Z"`) — con hora local la escena cambia según la máquina que la abre.
- **Proyecto movido**: los enlaces viejos apuntan a `reearth/navara`; el repo vivo es `maplibre/navara` (el registry de MasterMind tenía una entrada skip del 09-01 con la org antigua y 155⭐ — no volver a scrapear la org vieja).
- **Pre-1.0 en rápida evolución** (260⭐, pushed diario): fijar versión de `@navaramap/*` en proyectos serios y esperar roturas de API entre minors.
- **Doc en línea, no en README**: la referencia de API por niveles está en navara.world/docs; el README solo da la visión — no asumir que "no existe" algo que no está en el README.

## Verificación

Globo mínimo: arrancar el ejemplo de arriba con `npm run dev` y comprobar (1) el canvas llena la ventana, (2) el disco de Blue Marble aparece con atmósfera y sol coherentes con la fecha fijada, (3) `flyTo(40.4168, -3.7038)` sitúa Madrid sin tiles rotos al hacer zoom (subdivisiones LOD del motor), (4) el bloque de atribución muestra el HTML pasado. Si la escena sale negra: verificar que `init()` fue awaited antes de `addLayer`.

## Referencias

- Repo: https://github.com/maplibre/navara (antes reearth/navara) — Apache-2.0 OR MIT, Rust+WASM+TypeScript
- Docs: https://navara.world/docs/ · Ejemplos: https://navara.world/examples/
- npm: scope `@navaramap` (`@navaramap/three`, `@navaramap/three-default-plugin`)
- Skill oficial para agentes: `skills/navara-usage` dentro del repo
- Skills hermanos: `threejs-3d-maps` (tiles 2D proyectados), `photorealistic-3d-tiles-threejs` (Google tiles + TSL), `cesium-3d-tiles-vector-data` (motor CesiumJS)

---

**Hecho con ❤️ por David Antizar**

## Comparativa de alternativas

- **[reearth/navara](https://github.com/reearth/navara)** — API por niveles (declarativo → bajo nivel) y escena fotorrealista con atmósfera/sol/sombras; la referencia de globo 3D sobre la que se apoya este skill (ver también `threejs-3d-maps`).

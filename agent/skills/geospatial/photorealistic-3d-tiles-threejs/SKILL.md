---
name: photorealistic-3d-tiles-threejs
version: "1.0.0"
description: "Use con ciudades 3D fotorrealistas three.js + 3D Tiles."
tags: [threejs, webgpu, tsl, 3d-tiles, cesium-ion, google-maps, geospatial, 3d-maps, webcodecs, gis]
related_skills: [threejs-3d-maps, cesium-3d-tiles-vector-data, fable5-webgpu-procedural, webgl-scene-wow]
---

# Tiles 3D Fotorrealistas en three.js (3DTilesRendererJS + TSL/WebGPU)

## Resumen

Patrones de ingeniería extraídos de **Makio64/dreamfold** (David Ronai, @makio64 — presentado en CesiumJS Dev Day 2026): una app three.js que sitúa la cámara en una calle real de los **tiles fotorrealistas 3D de Google** y pliega la ciudad sobre el espectador (efecto Inception) deformando vértices con **TSL en WebGPU**. El repo original tiene solo ~40⭐, pero su `AGENTS.md` (629 líneas) documenta más de una docena de decisiones con alternativas-plausibles-pero-incorrectas — oro para cualquiera que construya visores 3D de ciudades reales (España Atlas, gtfs-box-3d-viewer, map3d, sombras 3D…).

**Stack de referencia:** `three@0.185` + `3d-tiles-renderer@0.5.1` (NASA-AMMOS) + `mediabunny` (WebCodecs) + Vite, sin framework. Token gratuito de [Cesium Ion](https://ion.cesium.com/tokens) para servir los tiles de Google.

## Cuándo usar

- Visor 3D de ciudades REALES con malla + fotografía (no tiles 2D proyectados → para eso: `threejs-3d-maps`)
- Efectos sobre la propia geometría de la ciudad (plegar, ondear, desplazar vértices)
- Escenas WebGPU/TSL con streaming de 3D Tiles a escala planetaria
- Grabar vídeo determinista de una escena WebGL/WebGPU en el navegador
- Duda de motor: CesiumJS clásico → `cesium-3d-tiles-vector-data`; aquí el motor es three.js con el renderer de NASA

## Instalación

```bash
pnpm add three 3d-tiles-renderer mediabunny   # node >= 22.12
```

## Patrones clave (cada uno con su alternativa incorrecta plausible)

### 1. El ancla float32: todo al origen en frame local

Las coordenadas ECEF terrestre son ~6.4e6 y un vertex shader float32 tiene **~0.5 m de resolución** ahí. Solución: un `Frame` ECEF→local (East-Up-South) aplicado al grupo de tiles **en CPU con float64**; todo lo demás (uniformes, cámara) vive en metros locales. Sin esto, ningún efecto por vértices sobrevive. Ojo: el origen del frame NO se mueve al caminar (es el ancla de precisión); lo que sigue a la cámara es el centro del efecto.

### 2. Singularidades: evaluar el límite, no dividir

`sin(θ)/θ` y `(1−cosθ)/θ` son la forma correcta de escribir un arco de curvatura sin formar nunca el radio `1/k` (→ ~1e9 cuando θ→0). **Floor del ángulo, no del denominador**: dar floor solo abajo produce `sin(0)/1e-6 = 0` donde el límite es 1 → la ciudad colapsa sobre el eje (indistinguible de un fallo de carga). `1−cosθ` se escribe `2·sin²(θ/2)` por lo mismo. Para el pliegue completo: **cap** (techo) del ángulo, no clamp — un clamp acumula longitud de arco sobrante en el límite.

### 3. Refinamiento de tiles: cámara de carga separada

En un tileset planetario `displayActiveTiles=false` a propósito: conservar los tiles inactivos llenaría la escena de continentes de nivel raíz (en París estarías dentro de una malla marrón del tamaño de Francia). Se añade una **segunda cámara cenital** (loader camera) que solo refina — enmarca el disco de ciudad que el efecto puede alcanzar; una frustum que refina Y muestra es el error.

### 4. Geometría deformada → culling fuera

`autoDisableRendererCulling` debe quedarse ON: un vértice doblado deja su bounding sphere kilómetros atrás, así que todo frustum-test por objeto miente sobre esa geometría. Desactivarlo vacía el cielo justo cuando empieza el efecto.

### 5. TilesFadePlugin con NodeMaterials (WebGPU)

El plugin crossfadea LODs parcheando GLSL vía `onBeforeCompile` — que un `MeshBasicNodeMaterial` **nunca llama**; bajo WebGPU esa mitad falla en silencio. Fix: sustituir el `_fadeMaterialManager` privado del plugin por uno propio que lleve el stipple de Bayer **siempre en el shader** (sin el define `FEATURE_FADE`: cada flip de define bajo WebGPU es un recompile de pipeline, varios por segundo con tiles streaming). Acoplado a la forma interna del plugin en 0.5.1 → rompe ruidosamente al subir versión.

### 6. Ground probe: cuantil bajo de un abanico de rayos, no mediana

Sobre una ciudad, más de la mitad de un anillo de rayos hacia abajo cae en tejados → la mediana ES un tejado. Usar un cuantil bajo del repartido de varios rayos. El primer rayo da además el tejado bajo el origen → cámara encima del edificio en vez de dentro. Y **seguir sondeando hasta que el pipeline de tiles se calle**: el primer mesh bajo el origen es una cáscara continental; solo la última respuesta es la calle.

### 7. La calle se autoriza, no se infiere

Los impactos bajos no distinguen asfalto de parque, agua o el tablero bajo un viaducto. Las posiciones buenas llevan coordenada visualmente verificada (`streetCenter: true`); buscar "el punto más bajo más lejos" no es sustituto.

### 8. Tone mapping para mosaicos fotográficos: Khronos PBR Neutral, no AgX

La malla de Google YA es una fotografía con su curva de cámara impresa. Un tone-mapping escena-referida (AgX, película) "revela el negativo dos veces" → el yeso de París sale tiza. PBR Neutral es identidad por debajo de 0.8 y solo comprime arriba: las fotos salen fotografiadas y rueda hacia blanco solo lo autoría por encima de 1.0 (el disco solar). Consecuencia: `toneMappingExposure = 1`, no una fracción. Bloom umbral 1.0 y cadena HDR (RTTs half-float).

### 9. Presupuesto de frame: ratio 1.5 y pases que se reconstruyen

`setPixelRatio` capado a 1.5 (no 2 del dispositivo) — todo lo caro es por píxel. Los pases caros (raymarch de nubes, tilt-shift, glow) se **añaden/quitan de la cadena** con un checkbox, no se ponen a fuerza 0: un marching no se abarata por invisible. Cada rebuild debe disponer los render targets del anterior (RTTNode no libera en dispose).

### 10. Sistema de "shots" seekable = grabación determinista

Cada plano (8 movimientos tipo "escenas de entrenamiento de Inception") es un conjunto de canales que son **función pura de t** — nada integra estado. Por eso `seek(t)` es legal y la grabación fotograma a fotograma es idéntica al directo. Los canales de la animación escriben por los mismos setters que los sliders manuales (un movimiento inalcanzable a mano es inalcanzable para nadie). Cualquier control manual que toque un canal del shot debe DETENER el shot primero (wrapper `manual()`), si no el disparo lo sobreescribe en el mismo tick.

### 11. Grabación WebCodecs (mediabunny): reglas de oro

- **Nada puede await entre `renderFrame()` y leer el canvas**: un drawing buffer WebGPU solo es legible en la tarea que lo llenó (medido: leer antes = uniformemente cero).
- Las transiciones de tiles andan en el **reloj virtual** del shot (`1/fps` de tiempo autoral), nunca en `performance.now()` — un fotograma grabado tarda más en renderizarse que su duración real.
- Una ventana de tamaño 0 **invalida el swapchain permanentemente** (`setSize(0,0)` → error de validación en todos los renders posteriores, pantalla negra sin errores visibles). Resize rechaza 0, init lo pisa, y el tick reaplica el tamaño si difiere.

### 12. Verificación headless: rAF no existe en pestaña en segundo plano

`requestAnimationFrame` se pausa en pestaña oculta — y con él la `PriorityQueue` de descarga/parseo de tiles → parece un fallo de auth. Truco: sustituir `_schedulingCallback` de las colas por `setTimeout(…,0)` y buclear con un **MessageChannel** (no está throttled). Para congelar un fotograma de un shot: `seek` **sin** parar el loop — WebGPU solo presenta desde el animation loop; un loop parado = canvas congelado que parece escena negra.

### 13. Niebla/bruma en espacio doblado

La bruma es función del plano de suelo (distancia al eje del pliegue), NO de la distancia a cámara — el pliegue acerca el borde lejano a la lente y la niebla se desharía justo cuando hace falta. El cielo y la bruma son **la misma función muestreada dos veces** (una por el background a lo largo del rayo del píxel, otra por el material a lo largo del rayo al fragmento doblado): una copia afinada a mano siempre acaba en silueta en el borde.

## Esqueleto mínimo (3d-tiles-renderer + Ion)

```javascript
import { TilesRenderer, CesiumIonAuthPlugin, TilesFadePlugin } from '3d-tiles-renderer';
import { MeshBasicNodeMaterial } from 'three/tsl'; // tiles dibujados UNLIT:
                                                    // la malla ya viene fotografiada con sol

const tiles = new TilesRenderer();
tiles.registerPlugin(new CesiumIonAuthPlugin({ apiToken, assetId })); // Google Photorealistic vía Ion
tiles.registerPlugin(new TilesFadePlugin());
tiles.group.applyMatrix4(frame.toLocal);      // patrón 1: ECEF → metros locales
tiles.displayActiveTiles = false;             // patrón 3
// material de los tiles: NodeMaterial con el efecto en TSL, enganchado en 'load-model'
// para que un tile que llega a mitad de animación ya esté doblado en su primer frame
```

## Comparativa de alternativas

- **`threejs-3d-maps`** (geo-three/maptalks): tiles 2D proyectados + extrusión GeoJSON — más ligero, sin fotografía real. Usar este skill cuando hace falta malla 3D fotorrealista de ciudad.
- **`cesium-3d-tiles-vector-data`** / Reearth: motor CesiumJS completo (cualquier 3D Tiles, datos vectoriales) — usar cuando el requisito es GIS serio, no efecto visual three.js.
- **`fable5-webgpu-procedural`** / `webgl-scene-wow`: mundos procedurales TSL — el framework de shader es común, los datos no.

## Pitfalls

- El token de Cesium Ion debe **verificarse contra el servicio de tiles**, no solo de forma: un token bien formado y conocido por el endpoint puede recibir un root tileset que lo rechaza un momento después (`ok`/`slow`/`refused`: un timeout no es veredicto sobre la key).
- El renderer debe levantarse ANTES que la credencial (setup sobre el cielo, no sobre negro).
- Un corte (discard) de fragmentos al doblar se decide sobre el **par** coordenada-doblada vs coordenada-original: cortar solo sobre la doblada borra todo lo que hay detrás del espectador.
- Al grabar: nada puede detener el shot mientras `capturing` (un stop a mitad deja `_shot` null y el fichero sale con la segunda mitad congelada, con tamaño válido).
- 3d-tiles-renderer 0.5.x usa APIs internas (fade manager); fijar versión y auditar el upgrade.
- Los "recursos" de la escena (destinos, tiros de cámara) son datos curados a mano en tablas (`DESTINATIONS`, `SHOTS`) — el código solo los aplica.

## Verificación

Tras tocar el efecto: con `bend = 0` la ciudad debe quedar visualmente idéntica a un `MeshBasicNodeMaterial` pelado (un colapso sobre el eje se disfraza de "los tiles no cargaron"); el ground probe asienta en ±2 m de la altura conocida; nada `NaN` en la posición de cámara. Caminar hacia relieve (Hong Kong Central hacia The Peak es el banco de pruebas) y comprobar que el datum sigue el terreno — si se queda a 3 m mientras la cámara sube 400 m, es el bug del datum: el pliegue se curvará POR DEBAJO del espectador en vez de por encima.

## Referencias

- Repo: https://github.com/Makio64/dreamfold (demo: dreamfold.netlify.app — pide token Ion gratuito; `AGENTS.md` es el documento de decisiones completo)
- Hermano: https://github.com/Makio64/threejs-cinematic-world-zoom (comparte `geo.js`, `tilesAuth.js`, `mapLinks.js`)
- Renderer: https://github.com/NASA-AMMOS/3DTilesRendererJS
- Cesium Ion: https://ion.cesium.com/tokens · Photorealistic 3D Tiles © Google vía Ion

---

**Hecho con ❤️ por David Antizar**

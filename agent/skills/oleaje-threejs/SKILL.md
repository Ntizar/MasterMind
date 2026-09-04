---
name: oleaje-threejs
version: "1.0.0"
description: "Use al trabajar en Water3J: oleaje científico con Three.js."
tags: [threejs, oleaje, ocean, física, webgl, water3j]
---

# Simulación de oleaje con Three.js (Water3J)

Dominio para cualquier tarea del proyecto **Water3J** (`~/Projects/Water3J`, repo `Ntizar/Water3J`): visualizador científico de oleaje, refracción/difracción, sedimentos, e interacción con estructuras portuarias.

## Estado actual (agosto 2026): v1 + STUDIO PC + FASE 2D + SALIDAS PROFESIONALES

- **Biblia de tests 51/51 VERDE** (`npm test`): física en Node (T13 1D, T14 2D 8/8, T15 separaciones 4/4, T16 cliente Portus 5/5, **T17 convención EMODnet 7/7**) + verificaciones E2E puppeteer+SwiftShader headless (no dependen del PC del usuario). Los tests son LA BIBLIA del proyecto: primero se escribe el test del resultado final, luego código hasta que pase. Cada nueva capacidad = nuevo test en la biblia. Bugs cazados por la biblia: clave `F` de Goda, timestamp en comparación de JSON, huecos -99.9 del SIMAR, perpendicular del rayo, redondeo del invariante de rotura, **convención del signo EMODnet (T17: `Math.abs()` convertía tierra en "mar" → olas dentro de la tierra; correcto: negativo=agua, positivo=tierra→h=null)**.
- **App v1** en `src/app/`: estado puro serializable → campoOlas → shaders Gerstner GPU → main.js. UI móvil con sliders, escenas, guardar/cargar escenario JSON.
- **Datos reales Puertos del Estado** (`src/app/puertos.js` + `src/studio/portus.js`): API real descifrada de los widgets de Portus: `https://poem.puertos.es/portus/StationData?code=<CODIGO>&params=Hm0,Tp` → JSON con flag de calidad validada (excluir no validados). Parser SIMAR (CSV tab-separado; huecos = -99.9, filtrar con `<= -90`). T16 5/5. CORS: puede fallar en navegador → vía manual (pegar JSON) documentada. Nunca fingir datos si la red falla.
- **Water3J Studio** (`studio.html`, `src/studio/`): versión PC seria. Motor de transectos (`motor.js`, Node-testable, puro): shoaling Ks + refracción Snell Kr + límite rotura 0.78·h + cargas Goda + clapotis. Biblioteca de escenarios en IndexedDB. Panel de TRANSPARENCIA obligatorio: cada fórmula con qué test la avala + "ejemplo con tus números" comprobable a mano.
- **Fase 2D sobre mapa** (`motor2d.js`, `capa2d.js`, `batimetria-cliente.js`): rayos Snell 2D + flujo de energía con **b real medida entre rayos** (`calcularSeparaciones`) + rotura 0.78·h sobre **batimetría EMODnet real** (caché IndexedDB) sobre Leaflet (10 boyas geolocalizadas, transecto 2 clics haversine). Animación de frentes isócronos. **Resolución adaptable por zoom** (puertos: 15×15 en 1.2 km). Fuentes de batimetría: leer `references/fuentes-batimetria.md` ANTES de elegir fuente.
- **Salidas profesionales** (`src/studio/informe.js`): informe imprimible a PDF (window.open + Ctrl+P) con condiciones de partida + fuente de cada dato (boya con fecha GMT), física con su test avalador, y sección "Procedimiento de validación para el revisor" (URLs exactas de StationData y depth_sample para comprobar a mano). Export CSV del transecto (x,h,Hs,Ks,Kr,α,rotura). `descargar()` usa Blob+URL.createObjectURL.
- **README.md** actualizado con estado real: tabla de tandas de tests, bugs cazados, APIs, limitaciones honestas. Mantenerlo al día en cada fase (David lo pidió explícitamente: "el README con el estado real del proyecto").
- **Publicado**: landing https://ntizar.github.io/Water3J/ + demo.html (móvil) + studio.html (PC). Deploy multipage con vite base `/Water3J/` (añadir cada HTML nuevo a `vite.config.js` → input).

## Fuentes de verdad

1. **Docs del repo** — `docs/01-referencias.md` a `docs/09-biblia-tests.md`: investigación completa (teoría, fórmulas, arquitectura por fases 0-7) y la biblia de tests. Leer antes de implementar.
2. `references/repos-clave.md` — repos de referencia con qué copiar de cada uno.
3. `references/lecciones-implementacion.md` — lecciones y pitfalls de la implementación v1 (obligatorio antes de modificar src/).
4. `references/salidas-profesionales.md` — informe PDF, export CSV, flujo boya→2D y UX de estudio profesional (leer antes de tocar `informe.js`, `portus.js` del Studio o la UI de estudio).
5. `references/ranking-spots-surf.md` — app de "mejores olas": ranking de spots con datos reales, Open-Meteo Marine como respaldo de Puertos del Estado, rate-limit de EMODnet y PDF con puppeteer (leer antes de trabajar en ranking/informes de surf).
6. `references/ola-perfecta-zoom-playa.md` — fase "ola perfecta": zoom de playa con rayos 2D sobre rejilla fina EMODnet y puntos de rotura exactos con coordenadas (leer antes de hacer zoom de playa o mapas headless de rotura). Incluye la CONVENCIÓN T17 del signo de EMODnet (negativo=agua, positivo=tierra; NUNCA Math.abs — bug raíz de "olas dentro de la tierra"), coordenadas de playa por Nominatim (spots a mano desplazados ~3 km), y tooltips permanentes para screenshots headless.
7. `references/oleaje-clima-viento.md` — módulo oleaje-completo: desglose swell vs mar de viento, viento offshore/onshore por orientación de la playa, clima (lluvia/nubes) por hora; 2 endpoints Open-Meteo por spot (leer antes de tocar el ranking, el score de surf o informes con viento).

## Puntos clave (resumen operativo)

- **Olas visuales:** Gerstner espectral (componentes con dirección/steepness/wavelength, dispersión `c = sqrt(g/k)`). Shader de referencia limpio: Sean-Bradley/three.js rama `gerstner-waves`. Steepness sumado ≤ ~1.
- **Mar real:** espectros Pierson-Moskowitz / JONSWAP discretizados en bandas frecuencia+dirección con fases aleatorias.
- **Aguas someras / inundación:** solver SWE por **virtual pipes** (4 buffers: fondo, columna, flujo X, flujo Y) — mejor referencia `lisyarus/webgpu-shallow-water` (algoritmo portable a GLSL). En WebGL puro: `aeplay/WebFlood` (semi-lagrangiano).
- **Transformación costera:** shoaling (`H ∝ h^-1/4`), refracción (Snell `sin(α)/c = cte` con `c(h)` local), difracción (Mild-Slope Eq. / integrales de Fresnel tras diques), reflexión (Cr: muro vertical ~0.9, escollera ~0.3, playas ~0.1 → clapotis).
- **Sedimentos (fase 2):** τ de corte por oleaje → Shields/Meyer-Peter & Müller (bed load) → CERC (deriva litoral) → `∂z_b/∂t = -∇·Q/(1-p)` con feedback a la refracción. Base para port: `bshishov/UnityTerrainErosionGPU`.
- **Decisión de stack:** empezar 100% WebGL2 + GLSL (sin WebGPU/FFT/compute), como `achrefelouafi/WaterThreeJS` — corre en cualquier navegador, cero assets.

## Fases del proyecto

| Fase | Contenido | Estado |
|---|---|---|
| 0-1 | Setup + océano Gerstner espectral + material de agua | ✅ |
| 2 | Batimetría editable + shoaling/refracción | ✅ (Studio: presets; falta dibujar perfil a mano) |
| 3 | Estructuras (diques/muros) con reflexión | 🔶 muro vertical con Goda OK; dique/espigón con disipación real pendiente |
| 4 | SWE GPGPU (virtual pipes) | pendiente |
| 5 | Sedimentos/morfodinámica | pendiente |
| 6 | Interfaz científica (inspector, overlays Hs/τ/Kd) | 🔶 transparencia de fórmulas OK en Studio |
| 7 | Batimetría real (GeoTIFF) | pendiente |

**Siguientes pasos acordados con David**: dique/espigón con disipación real, dibujar perfil batimétrico a mano (edición gráfica, hoy JSON en textarea), difracción tras diques, isócronas de alcance, comparación A/B de escenarios, y convertir el ranking de spots en app con cron diario a Telegram. Hecho ya: informe PDF + export CSV + boya→simulador + animación de frentes + b real + resolución adaptable por zoom para puertos + README con estado real + **test real de Somo** (batimetría EMODnet + 14 días de oleaje horario real → ranking de días de surf, zona de rotura, cambio de costa vía transporte CERC Q∝Hs^5) + **ranking de 8 spots del Cantábrico con PDF** (ver `references/ranking-spots-surf.md`) + **test multi-zona Mediterráneo** (mismo motor en otra costa, scores menores correctos por régimen) + **mapa de puntos críticos** (Leaflet headless → PNG incrustado en el informe PDF v2) + **"ola perfecta" en 3 playas** (Somo, Suances/Los Locos, Liencres/Madero): zoom de playa con roturas exactas por coordenada, cada una con huella batimétrica distinta (barra recta / cabo convergente / ría con canal) + **T17 tras el feedback de David ("¿cómo vamos a tener olas dentro de la tierra?")**: convención del signo EMODnet corregida de raíz, máscara de costa, mapas regenerados y verificados 100% sobre el agua + **módulo oleaje-completo**: desglose swell vs mar de viento, viento offshore/onshore por hora y clima 7d (ver `references/oleaje-clima-viento.md`); pendiente integrar la nota de viento en el score del ranking y en el PDF. El pipeline de zoom es genérico: nueva playa = posición OSM por Nominatim + 2 coordenadas + 1 comando (~1 min; ver `references/ola-perfecta-zoom-playa.md`). El Pages es el escaparate ("venderlo"); el programa debe ser top con datos en local (IndexedDB), PC-first con más capacidades y móvil como demo ligera. Ritmo de trabajo del usuario: "dale duro" — planear pocas llamadas decisivas (≤5), batchear, y entregar fases completas verificadas, no planes. David valida con TESTS REALES ("¿de verdad o no sirve para nada?"): ante un avance, demostrar valor con un caso real ejecutado (playa concreta, datos reales, resultado cuantificado), no con tests unitarios solos.

## Hero Three.js interactivo para landings (patrón GlamourSurf, 31/08/2026)

Receta probada en https://ntizar.github.io/glamoursurf/ (repo Ntizar/glamoursurf, index.html autocontenido, sin build):

- **Imagen de marca como textura viva**: `PlaneGeometry(24,12,220,120)` + ShaderMaterial con 3 Gerstner sumadas (direcciones/steepness/wavelength distintos), textura fluyendo con `vUv + vec2(0, vHeight*0.02)`, foam por `smoothstep` en la cresta. Import ESM: `https://unpkg.com/three@0.160.0/build/three.module.js`; textura con `TextureLoader` + `colorSpace = SRGBColorSpace`.
- **Móvil = scroll rompe la ola**: uniform `uBreak` (0→1 con `scrollY/innerHeight`); al crecer, suben amplitudes, la cresta se adelanta (`pos.x += barrel·sin(π·uv.y)`) y aparece espuma.
- **PC = ratón surfea**: uniforms `uMouse` normalizado + `uMouseV` (delta por frame): hundir la superficie bajo el cursor con gaussiana `exp(-md²·k)`, estela proporcional a velocidad y brillo dorado en el fragment. Detección táctil: `matchMedia('(pointer: coarse)')`.
- Hero `position:fixed` + `main { margin-top:100vh }` encima: el contenido sube sobre la ola; titular se desvanece con el scroll.
- Verificación sintáctica sin navegador: extraer el `<script type="module">` y compilarlo con `new vm.Script()` en Node.
- El CTA de una landing promocional SIEMPRE apunta al canal social que David indique (aquí corrigió a mitad de sesión: botón degradado Instagram → instagram.com/glamour.surf).

## Convenciones

- Todo en castellano, atribución "Hecho con ❤️ por David Antizar".
- Preferencia visual de David aplica: fondo blanco/sombras sutiles en UI, nada de dark/liquid-glass.
- Diseño espectacular pero cada fase usable por sí misma; física correcta antes que realismo fotográfico.

## Comparativa de alternativas

- **[Token-Gremlin/natural-disasters](https://github.com/Token-Gremlin/natural-disasters)** — océano y clima extremo procedural en three.js r169 (WebGL2/GLSL3) con CI; referencia de oleaje de alta energía/clima extremo.
- **[gdfa-ugr/marinetools](https://github.com/gdfa-ugr/marinetools)** — caracterización estadística de proceso vectorial para generar oleaje estocástico; útil para alimentar el oleaje con datos reales.

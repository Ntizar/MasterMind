# Repos clave para oleaje con Three.js (investigación 2026-08-30)

Qué copiar de cada referencia. Detalle completo de teoría y fórmulas en `docs/02-teoria.md` y `docs/03-transformaciones.md` del repo Water3J.

| Repo | Stars | Qué tomar | Qué NO |
|---|---|---|---|
| **achrefelouafi/WaterThreeJS** | — | Pipeline HDR completo: pase refracción + DepthTexture, Gerstner espectral con dispersión, caústicas procedurales, espuma de orilla por columna de agua, flotabilidad ligera, underwater volumétrico, ACES. Todo GLSL/WebGL2, cero assets | — |
| **Sean-Bradley/three.js** (rama `gerstner-waves`) | — | Función `GerstnerWave` GLSL didáctica y limpia (4 componentes, `c = sqrt(9.8/k)`) — punto de partida directo del shader | Solo 3 olas fijas, sin espectro |
| **lisyarus/webgpu-shallow-water** | 102 | Algoritmo virtual pipes: 4 buffers (fondo RG32F, columna, flujo X, flujo Y), pasos del solver, fronteras tipo muro/fuente/olas. Portable a GLSL | Es C++ nativo, no Three.js |
| **aeplay/WebFlood** | 57 | SWE semi-lagrangiano 100% WebGL (sin WebGPU), validado con Fraccarollo & Toro 1995. PDF de tesis con implementación | Código antiguo (GLOW.js) |
| **jeantimex/threejs-water** | 185 | Caústicas raytraced, reflejos/refracciones en geometría con shader dedicado (proyección de caústicas sobre superficies redondeadas) | Escenario piscina, no océano |
| **Mohido/Ocean** | — | Port JS del clásico "Effective Water Simulation" (GPU Gems 1 cap. 1) | — |
| **bshishov/UnityTerrainErosionGPU** | 154 | Matemática de erosión: capacidad de transporte, deposición, actualización de altura. Base del módulo sedimentos | Es Unity/compute shaders |
| **pyReef-model/wavesed** | — | Modelo científico de sedimentos por oleaje (Airy + Huygens + CERC) — referencia conceptual | Python, no portable directo |
| **Three.js Water Pro / Tidewater** | comerciales | Qué espera el mercado: FFT+Gerstner combinados, espuma multicapa, wake field, presets. Lección Tidewater: "no es CFD y eso es bueno" | Código cerrado, no copiar |

## Teoría (no-repo)

- **Coastal Wiki** (coastalwiki.org/wiki/Shallow-water_wave_theory): fuente principal de fórmulas — refracción, shoaling, difracción, reflexión, radiación de tensiones.
- **satbastola CivilEngineering Cap. 5**: fórmulas condensadas de MSE (`∇·(C·Cg·∇η) + k²·C·Cg·η = 0`), difracción por Fresnel tras dique semi-infinito.
- **GMD Ocean wave tracing v.1 (2023)**: ray tracing de olas sobre batimetría y corrientes variables.
- **MDPI 2673-3951/5/2/25**: pipeline integrado Mild-Slope → RANS → sedimentos (aspiración científica).
- **wavespectra (Python)**: validar espectros generados.

## Lección transversal

El estándar de la industria visual es **Gerstner (swell) + espectro (viento/chop)**, no CFD. Para puertos lo importante es refracción+reflectión+difracción (modelos de fase tipo MSE), no Navier-Stokes completo.

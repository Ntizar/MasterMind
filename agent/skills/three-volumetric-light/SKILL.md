---
name: three-volumetric-light
description: Three.js Volumetric Light — haz de luz volumétrica (god rays) con raymarching analítico de cono, shadow map, bloom pyramid low-res y partículas de polvo. Upgrade leído del código real (2026-09-02).
version: "2.0.0"
tags: [threejs, glsl, shaders, post-processing, god-rays, volumetric, creative]
---

# Three.js Volumetric Light — Haz de luz volumétrico real (código destilado)

Repo: `github.com/cullenwebber/three-volumetric-light` (~41⭐, JS, MIT-less, activo jul-2026).
Escena demo: mano GLB animada bajo un foco con haz volumétrico, polvo flotante, bloom y gradiente ASCII.
**Esta v2 reemplaza la v1 inventada del maratón 2026-06-18/19** (bullets genéricos sin leer el código).

## Cuándo usar este patrón

- Necesitas **un god-ray convincente en three.js sin post-processing chain pesada** (UnrealBloomPass, etc.)
- Quieres luz volumétrica que **reacciona a oclusores** (shadow map) — no un simple cone degradado
- Landing 3D "espectáculo visual" (prefs de David: espectáculo primero) con polvo/halo/flicker
- Referencia para animación esquelética procedural sobre GLB descargado

## Arquitectura real del repo (leída del árbol src/)

```
src/
├── core/Three.js, WebGLContext.js      # bootstrap renderer + loop
├── scenes/Scene.js                     # composición: luces, objetos, compositor, LightProbe
├── objects/VolumetricBeam.js           # CONO con ShaderMaterial (el corazón)
├── objects/BeamParticles.js            # 2 capas de puntos de polvo dentro del haz
├── objects/LightGradient.js            # gradiente de fondo detrás del haz
├── objects/Arm.js                      # GLB mano + bones procedurales
├── postfx/BeamCompositor.js            # pipeline render a baja res + bloom pyramid
├── materials/AsciiMaterial.js          # shader ASCII (glitch aesthetic)
├── materials/BentNormalShading.js + baking/BentNormalBaker.js  # (descatalogado, ver pitfalls)
├── utils/CameraRig.js                  # parallax de ratón con maath easing
└── shaders/*.glsl                      # beam, particles, bloomDown/Upsample, screen, ascii, background
```

Stack: three ^0.182, three-mesh-bvh ^0.9, maath, vite 7 + vite-plugin-glsl (importa .glsl directo), tailwind 4.

## Patrón 1 — Haz volumétrico: raymarching analítico de cono (VolumetricBeam + beam.frag.glsl)

Mesh = superficie del cono (`BackSide`, `AdditiveBlending`, `depthWrite:false, depthTest:false`) construida desde un `THREE.SpotLight`:
- `direction = normalize(target.position − light.position)`; base `right = cross(dir, up)`, `up = cross(right, dir)`
- Conos internos/externos desde el propio spot: `inner = angle·(1−penumbra)` → uniforms `uCosInner`, `uCosOuter`
- El fragment hace **intersectBox ray-box** (slab method, `t0/t1 = (bmin−ro)/rd`) contra AABB de la escena y **marcha STEPS=16 samples** solo dentro del haz

Densidad acumulada por sample (niebla/humo):
- **value noise 2D con hash PCG3D entero** (`uvec2 v*1664525u+1013904223u`, sin `fract(sin(dot))` — barato y sin banding)
- rampa `uSmokeRamp`, escala `uSmokeScale`, atenuación inversa al cuadrado con `uAttenuation`/`uFalloff`
- **God rays por shadow map**: `uniform sampler2DShadow uShadowMap` + `uShadowMatrix` (¡`light.shadow.matrix`! no `light.matrixWorldInverse`); coords fuera de [0,1] → visible; bias `sc.z − 0.002`
- Colores: core + gradiente top/bottom (`uColorCore`, `uColorTop`, `uColorBottom`) + halo exterior `uCosHalo = cos(min(angle·2.4, 1.25))`
- Depth de la escena (`sampler2D uSceneDepth` + `uCameraNear/Far`) para que el haz se corte con geometría

## Patrón 2 — Compositor low-res (BeamCompositor.js): el truco de rendimiento

- **RESOLUTION_SCALE = 0.25**: haz + bloom se renderizan a ¼ de resolución en RTs `HalfFloatType` → barato y el blur lo disfraza
- `BLOOM_MIP_COUNT = 6`: pyramid downsample→upsample (shaders `bloomDownsample/bloomUpsample.frag.glsl` estilo Kawase), `bloomStrength 2.5`
- RT de escena a resolución completa con `samples: 2` (MSAA) + `depthTexture` para el beam
- **Escena de oclusores separada** (`occluderScene`): se re-renderizan solo los objetos que deben bloquear luz al RT de profundidad → no pagas la escena completa 2 veces
- Grain final (`grainStrength 0.04`), threshold 0.075, knee 0, contraste 1.2, compuesto con `screen.frag.glsl`
- **primeGI**: render + update dobles en el frame 0 para que bloom/shadow no salgan negros el primer fotograma

## Patrón 3 — Polvo en el haz (BeamParticles.js)

Dos capas: gruesa (15 pts, size 4, `focusDistance 16, focusRange 0.5`) y fina (50 pts, size 1, focusRange 16) — depth-of-field fake sobre sprites; posiciones restringidas al volumen del cono (usan la geometría del beam como guía).

## Patrón 4 — GLB animado sin Timeline (Arm.js)

- Carga con GLTFLoader envuelto en Promise (`ImportGltf`), escala normalizada: `root.scale = 3.2/size.y` y centrado con `Box3`
- **Huesos por regex de nombre**: `/^(thumb|index|middle|ring|pinky)\.?(\d+)?$/` → array `{bone, baseX, finger, segment}`
- Onda procedural: `rotation.x = baseX + lerp(min,max, sin(t·2 + finger·1.25 + segment·0.15)·0.5+0.5)·0.75` con rangos distintos por falange — mano "respirando" sin keyframes

## Patrón 5 — Escena y presentación

- SpotLight: `angle 0.225, penumbra 0.35, decay 2.6, intensity 600`, background `0x010204` casi negro → el haz es el protagonista
- `LightProbeGenerator` (three/addons) para IBL ambiental derivada del propio entorno; fondo = plano con gradiente shader
- `CameraRig` con límites x/y/z y `smoothTime 0.4` (maath damping) + `distanceScale = clamp(1.7/aspect, 1, 1.5)` → responsive móvil sin layout aparte
- Deploy a GitHub Pages vía `.github/workflows/deploy.yml`
- `window.three = three` en DEV → depurar escena desde la consola

## Pitfalls (verificados en el código)

- **BentNormalShading/baking fue DESACTIVADO** por crashes (`// Removed bent normals due to crashing` en Scene.js) — no lo reintegres sin aislar
- El shader requiere GLSL ES 3 (usa `sampler2DShadow`, hashes `uvec3`) → no compila en WebGL1; three moderno OK
- `depthTest:false` en el beam: se compone SIEMPRE encima; el corte con geometría lo da el depth RT del compositor, no el Z-buffer — si quitas el compositor, el haz atraviesa todo
- shadow.matrix ≠ matrixWorldInverse — copiar el uniform de un tutorial viejo da sombras desplazadas
- Los RT HalfFloat a ¼ res pueden bandear en GPUs viejas si falta `renderer.outputColorSpace` correcto
- repo sin README: sin docs de uso; es plantilla de estudio, no librería publicable — extraer los patrones, no el paquete

## Integración Mastermind

- Fuente de patrones para landings 3D (scroll-world-3d-landing, webgl-scene-wow, fable5-webgpu-procedural) cuando se pida "un foco dramático"
- El compositor low-res es el patrón reutilizable para CUALQUIER postfx en móvil: render efecto a escala 0.25 + pyramid blur
- WebGL headless: para verificar estas escenas sin GPU ver skill `devops/webgl-headless-verification`

## Verificación

Al portar el efecto: (1) el haz debe atenuarse con la distancia y cortarse con objetos opacos (probar metiendo una caja entre foco y fondo), (2) primer frame sin negro (primeGI), (3) `__THREE_RENDERER__`/`window.three` en DEV para inspeccionar uniforms, (4) FPS estable en móvil gracias a la escala 0.25.

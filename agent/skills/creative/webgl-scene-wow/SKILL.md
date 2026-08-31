---
name: webgl-scene-wow
description: "Use al crear escenas Three.js hiperrealistas con boids."
version: 1.0.0
tags: [threejs, webgl, shaders, boids, agua, caustics, hiperrealismo]
---

# Escenas "wow" con Three.js — estándar hiperrealista interactivo

Referencia mental: el estanque koi visto desde arriba donde lanzas pan y los peces nadan a comerlo. Ese nivel se logra con 6 técnicas combinadas, no con un truco único.

## Las 6 técnicas (receta completa)

1. **Agua = render target + shader de superficie**
   - Textura de normales animada (2 capas desplazándose en direcciones distintas) o simulación de ripples en ping-pong FBO (`height[i] = (promedio vecinos)*2 - prev` — propagación de ondas real, no seno).
   - Caústicas: patrón de Voronoi animado multiplicado sobre el fondo, o shader con `pow(voronoi, 8.0)`. Referencia: threejs.org/examples `shader/ocean`; blog de Maxime Heckel (blog.maximeheckel.com) para caústicas.
2. **Boids para criaturas** (peces, pájaros, enjambres)
   - 3 fuerzas: separación, alineación, cohesión + atractor (la comida) + repulsor (toque = susto).
   - En GPU: FBO simulation (posición/velocidad en texturas float; referencia threejs `community/gpgpu-birds`). En CPU: <100 criaturas va sobrado.
   - Detalle que lo vende: los peces NO van rectos al atractor — `steer = normalize(desired - velocity) * maxForce`, y los más rápidos llegan primero (competencia realista).
3. **Interacción física plausible**
   - Click = soltar comida (partícula que flota y hunde lento, con drift). Los peces compiten por ella; al comerla desaparece con puf de burbujas.
   - Ripples donde tocas: perturbar el FBO de altura, no un efecto cosmético encima.
4. **Profundidad y luz**
   - Fog exponencial con color del agua; sombras suaves PCF; env map para reflejos (`PMREMGenerator`).
   - Fondo del estanque: rocas con textura + normal map + oclusión; profundidad = más oscuro/azul.
5. **Postprocesado** (lo que separa "demo" de "hiperrealista")
   - UnrealBloomPass sutil, vignette, grano. En móvil: desactivar bloom en GPUs flojas.
6. **Vida ambiental**
   - Partículas: burbujas, motas en suspensión, hojas (opacidad 0.1-0.3, pocas).
   - Sonido opcional solo tras interacción del usuario (autoplay bloqueado).

## Recetas por escena

| Escena | Combina |
|---|---|
| Estanque koi (vista cenital) | ripples FBO + caústicas voronoi + boids CPU + comida que se hunde |
| Océano desde playa | threejs Water shader + cielo Sky + Gerstner (ver skill oleaje-threejs) |
| Enjambre/escuela 3D | GPGPU boids + instanced mesh + trail fade |
| Terrario/jardín zen | caústicas + partículas polen + viento en shaders de vegetación |

## Pitfalls

- **Móvil primero**: FBO float requiere `EXT_color_buffer_float` en WebGL2 — fallback (mitad de boids, sin bloom).
- Ping-pong FBO: 2 render targets y SWAPEAR, no recrear (fuga de memoria).
- Caústicas voronoi falsas si no se modulan por profundidad — multiplicar por `smoothstep` de profundidad.
- Boids con dt variable explotan (NaN) — clamp dt a 1/30 máx.
- En vertex shader: solo WebGL2, `texture` (no texture2D), `texelFetch` para grid.

## Verificación

- Headless puppeteer + SwiftShader (patrón biblia Water3J): screenshot no negro.
- FPS con `performance.now()` en 20 frames — <16ms promedio en desktop.
- Interacción: lanzar comida → un boid debe acercarse (log distancia mínima < radio).

## Referencias

- threejs.org/examples: `shader/ocean`, `community/gpgpu-birds`, `postprocessing/*`
- Maxime Heckel — caústicas y shaders: blog.maximeheckel.com
- m4ym4y/mayas-aquarium-3d — acuario react-three-fiber con feed fish
- kucdinteractive koiPond — UX: tap corto=ripples, mantener=atraer peces
- Skill hermano: `oleaje-threejs` (física de oleaje real, Water3J)

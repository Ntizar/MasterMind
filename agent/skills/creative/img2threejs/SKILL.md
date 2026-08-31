---
name: img2threejs
description: Use al convertir una imagen en modelo 3D Three.js.
version: 1.0.0
tags: [threejs, 3d, procedural, image-to-3d, generative, webgl]
---

# img2threejs — imagen → modelo Three.js procedural

Reconstruye el objeto de una imagen de referencia como modelo Three.js **solo con código** (paramétrico/procedural), listo para animar. Repo: https://github.com/img2threejs/img2threejs (14k+ ⭐, Apache-2.0, Python 3.10+ stdlib en `forge/`, TypeScript para el output).

## Cuándo usarlo
- Necesitas un 3D "bonito y liviano" de un objeto conocido (vehículo, edificio, mueble) sin descargar assets ni mallas.
- El output debe ser animable y editable por código (ideal para dashboards, demos, World3D).

## Flujo
1. Clonar el repo y ejecutar el forge CLI con la imagen de referencia: `python forge/` (ver README para flags exactos).
2. El forge genera un módulo TypeScript que construye la escena con primitivas/paramétricas (sin mallas descargadas).
3. Iterar contra los **quality gates** automáticos (silueta, proporciones, colores): el pipeline re-chequea el render contra la imagen y rechaza versiones fuera de tolerancia.
4. Integrar el módulo generado en tu escena Three.js; el modelo es code-only → diff-able y versionable en git.

## Patrones clave
- **Reconstrucción-por-código** vs fotogrametría: sin pesos, sin assets binarios, token-efficient para agentes.
- **Quality gates iterativos**: comparación render↔referencia como bucle de verificación (aplicable a cualquier pipeline generativo visual).
- **Output paramétrico**: árbol de primitivas con parámetros expuestos → animable por código.

## Pitfalls
- No sirve para objetos orgánicos complejos (caras, esculturas): mejor fotogrametría/modelos ML.
- El forge es Python stdlib: no necesita pip, pero requiere Python 3.10+.
- Los quality gates pueden iterar varias veces: presupuesta llamadas de render.

## Verificación
- Renderizar el módulo generado en una página Three.js mínima y comprobar silueta vs la imagen original.
- Confirmar que no hay assets binarios en el output (solo TS/JS).

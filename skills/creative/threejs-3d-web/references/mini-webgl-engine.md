# Mini WebGL Engine — Patrón para entornos sin scripts externos

## Cuándo usar

- **Hermes browser tool:** NO ejecuta `<script src>` externos, importmap, ni ES modules
- **Three.js inline 600KB+:** Timeout en el browser de Hermes al ejecutar scripts enormes
- **Canvas 2D no es suficiente:** Se necesita WebGL real (sombras, iluminación Phong, shaders, perspectiva 3D)
- **Archivo autocontenido obligatorio:** Sin dependencias externas

## Patrón: Motor WebGL mínimo (~33KB)

Escribir un mini motor WebGL con solo las clases necesarias:
- 4 programas de shaders (esferas, líneas, estrellas, anillos)
- Geometría de esfera (32x24 segmentos)
- Geometría de anillo (64 segmentos)
- Geometría de estrellas (puntos)
- Matemáticas de matrices (perspectiva, lookAt, multiply, translate, scale, rotY, rotX)
- Loop de renderizado con cámara esférica

## Shaders esenciales

### Esfera con iluminación Phong
```glsl
// Vertex: posición, normal, matriz MVP, matriz normal, color, dirección de luz, posición del ojo
// Fragment: diff + spec + ambient + rim light + emisividad
```

### Líneas (órbitas)
```glsl
// Vertex: posición + MVP
// Fragment: color + alpha
```

### Estrellas (puntos)
```glsl
// Vertex: posición + tamaño + brillo + MVP
// Fragment: círculo suave con alpha según distancia al centro
```

### Anillos (disco con textura)
```glsl
// Vertex: posición + UV + MVP + modelo
// Fragment: textura + iluminación + alpha según UV
```

## Matemáticas de matrices (sin librería)

```javascript
function mat4Perspective(fov, aspect, near, far) { ... }
function mat4LookAt(eye, center, up) { ... }
function mat4Multiply(a, b) { ... }
function mat4Translate(x,y,z) { ... }
function mat4Scale(s) { ... }
function mat4RotY(a) { ... }
function mat4RotX(a) { ... }
function mat3FromMat4(m) { ... }
```

## Estructura del render loop

```javascript
function render(time) {
    requestAnimationFrame(render);
    camDist += (targetDist - camDist) * 0.05;
    const view = mat4LookAt(eye, center, up);
    const proj = mat4Perspective(fov, aspect, near, far);
    const vp = mat4Multiply(proj, view);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    // 4. Estrellas → 5. Órbitas → 6. Sol → 7. Planetas → 8. Anillos
}
```

## Cámara esférica

```javascript
const eyeX = camDist * Math.sin(camPhi) * Math.cos(camTheta);
const eyeY = camDist * Math.cos(camPhi);
const eyeZ = camDist * Math.sin(camPhi) * Math.sin(camTheta);
```

Interacción:
- **Arrastrar:** modificar `camTheta` y `camPhi`
- **Scroll:** modificar `camDist`
- **Click en planeta:** `targetCamDist = radio * 8`, `targetCamTheta = atan2(x,z)`, `targetCamPhi = PI/3`

## Pitfalls

- **Buffer de índices:** `gl.ELEMENT_ARRAY_BUFFER` es global, no por objeto.
- **depthMask(false)** para estrellas — si no, pueden tapar objetos detrás.
- **gl.useProgram()** cambia todos los uniforms. Resetear todo antes de cada draw call.
- **Normal matrix** necesario para iluminación correcta con escala no uniforme.
- **Viewport con devicePixelRatio** para pantallas retina.
- **Clear color oscuro** para espacio negro profundo.
- **Saturno:** anillos después del planeta con `blendFunc` para alpha.

## Comparativa

| | Canvas 2D | Mini WebGL | Three.js |
|---|---|---|---|
| Tamaño | ~30KB | ~33KB | ~600KB |
| 3D real | No | Sí (esferas, iluminación) | Sí completo |
| Carga | Instantánea | Instantánea | Depende de CDN |
| Entornos | Todos | Todos | Scripts externos |

## Ejemplo completo

Ver `/root/workspace/sistema-solar/index.html` — ~33KB autocontenido con:
- Sol emisivo con pulso
- 9 planetas con iluminación Phong y rim light
- Saturno con anillos texturizados (División de Cassini)
- 3000 estrellas con point sprites
- Órbitas elípticas keplerianas
- Click en planeta = cámara vuela suavemente
- Arrastrar para rotar, scroll para zoom
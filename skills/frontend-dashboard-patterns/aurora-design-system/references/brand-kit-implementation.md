# Brand Kit Implementation — Técnica de Generación

**Fecha:** 2026-07-09
**Proyecto:** Ntizar-Aurora commit `4bc05f9`

## Resumen

Proceso completo para generar un kit de marca programáticamente: logos SVG geométricos, conversión a PNG, favicon multi-resolución, y página de marca viva con Three.js. Todo sin herramientas de diseño — solo código.

## 1. Logos SVG geométricos

### Diseño del símbolo "A"

Símbolo: letra "A" geométrica (de Antizar) con dos trazos de color divididos.

- **ViewBox:** 100×100
- **Apex:** `(50, 12)` — punta superior de la A
- **Trazo izquierdo:** azul `#2563eb` — `M50,12 L14,88 L38,88 L50,42 Z`
- **Trazo derecho:** naranja `#f97316` — `M50,12 L86,88 L62,88 L50,42 Z`
- **Barra horizontal:** negro `#0a0a0a` — `M34,55 L66,55 L66,62 L34,62 Z`

### Variantes generadas

5 símbolos + 5 logotipos (símbolo + wordmark "aurora"):

| Variante | Fondo | Trazo izq | Trazo der | Crossbar |
|---|---|---|---|---|
| Color | transparente | azul | naranja | negro |
| Blanco | transparente | blanco | blanco | blanco |
| Negro | transparente | negro | negro | negro |
| Azul | transparente | azul | azul | azul |
| Naranja | transparente | naranja | naranja | naranja |

### Logotipo completo

Símbolo a la izquierda + texto "aurora" en lowercase, font-weight 700, letter-spacing -0.02em. El texto usa el color del fondo de destino (blanco sobre oscuro, negro sobre claro).

### Técnica de generación

Generar SVGs con Python `write_file` — cada SVG es texto plano con paths hardcodeados. No se necesita ninguna librería de generación SVG.

```python
# Estructura base de cada SVG
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path d="M50,12 L14,88 L38,88 L50,42 Z" fill="{left_color}"/>
  <path d="M50,12 L86,88 L62,88 L50,42 Z" fill="{right_color}"/>
  <path d="M34,55 L66,55 L66,62 L34,62 Z" fill="{crossbar_color}"/>
</svg>'''
```

## 2. Conversión SVG → PNG

### Herramienta: cairosvg

```bash
pip install cairosvg --break-system-packages
```

### Generación de PNGs

```python
import cairosvg

# Símbolo 200px
cairosvg.svg2png(url='simbolo-color.svg', write_to='simbolo-color-200.png',
                 output_width=200, output_height=200)

# Logotipo 340px de ancho (mantiene aspect ratio)
cairosvg.svg2png(url='logo-negativo.svg', write_to='logo-negativo-340.png',
                 output_width=340)

# Favicon multi-resolución
for size in [32, 180, 512]:
    cairosvg.svg2png(url='favicon.svg', write_to=f'favicon-{size}.png',
                     output_width=size, output_height=size)
```

### Favicon ICO

Para el `.ico` se puede usar Pillow:

```python
from PIL import Image
img = Image.open('favicon-32.png')
img.save('favicon.ico', format='ICO', sizes=[(16,16),(32,32),(48,48)])
```

## 3. Página brand.html con Three.js

### Arquitectura

- **Importmap:** `https://cdn.jsdelivr.net/npm/three@0.164/build/three.module.js`
- **Dogfooding:** usa clases Aurora (`nz-btn`, `nz-badge`, `nz-eyebrow`, `nz-bento`, etc.)
- **CSS:** ntizar.css + ntizar.nucleo.css + ntizar.ui.css + ntizar.data.css + ntizar.motion.css

### Hero 3D — La "A" extruded

```javascript
// Geometría de la A en 2D (Shape)
const shape = new THREE.Shape();
shape.moveTo(50, 12);   // apex
shape.lineTo(14, 88);   // base izquierda
shape.lineTo(38, 88);   // pata izquierda interior
shape.lineTo(50, 42);   // cruce izquierdo
shape.lineTo(62, 88);   // pata derecha interior
shape.lineTo(86, 88);   // base derecha
shape.lineTo(50, 12);   // cerrar

// Extrude con profundidad
const geometry = new THREE.ExtrudeGeometry(shape, {
  depth: 12, bevelEnabled: true, bevelThickness: 2, bevelSize: 2
});

// Dos materiales: izquierdo azul, derecho naranja
// (usar groups en ExtrudeGeometry o dos meshes separados)
```

### Partículas con glow

```javascript
const particles = new THREE.Points(particleGeometry, new THREE.PointsMaterial({
  size: 0.5,
  color: 0x2563eb,  // azul
  transparent: true,
  opacity: 0.8,
  blending: THREE.AdditiveBlending,  // glow effect
  depthWrite: false
}));
```

### Anillos orbitales

3 anillos (azul, naranja, blanco) con `THREE.TorusGeometry`, rotación continua en ejes diferentes.

### Mouse parallax

```javascript
document.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 0.3;
  const y = (e.clientY / window.innerHeight - 0.5) * 0.3;
  camera.position.x += (x - camera.position.x) * 0.05;
  camera.position.y += (-y - camera.position.y) * 0.05;
});
```

### Secciones de la página

1. **Hero 3D** — canvas Three.js a pantalla completa + título overlay
2. **Logo** — showcase de las 5 variantes del símbolo + 5 del logotipo
3. **Color** — paleta con hex + oklch, bloques de color sólido
4. **Tipografía** — muestra de font stacks
5. **Forma** — `data-nz-shape` variants
6. **Componentes** — dogfooding de nz-btn, nz-badge, nz-card
7. **Voz** — tono do/don't, antetítulo `›`
8. **Descargas** — links a SVGs, PNGs, brandbook.md

## 4. Estructura de archivos del kit

```
Ntizar-Aurora/
├── assets/
│   ├── simbolo/
│   │   ├── simbolo-color.svg
│   │   ├── simbolo-blanco.svg
│   │   ├── simbolo-negro.svg
│   │   ├── simbolo-azul.svg
│   │   ├── simbolo-naranja.svg
│   │   ├── simbolo-color-200.png
│   │   ├── simbolo-blanco-200.png
│   │   └── simbolo-negro-200.png
│   ├── logo/
│   │   ├── logo-negativo.svg
│   │   ├── logo-positivo.svg
│   │   ├── logo-blanco.svg
│   │   ├── logo-negro.svg
│   │   ├── logo-azul.svg
│   │   ├── logo-negativo-340.png
│   │   ├── logo-positivo-340.png
│   │   ├── logo-blanco-340.png
│   │   └── logo-negro-340.png
│   └── favicon/
│       ├── favicon.svg
│       ├── favicon.ico
│       ├── favicon-32.png
│       ├── favicon-180.png
│       └── favicon-512.png
├── BRAND.md
├── brandbook.md
├── AGENTS.md
├── brand.html
├── DESIGN.md (parcheado: +accent_budget, +brand_voice)
└── ntizar.css (parcheado: +.nz-eyebrow)
```

## 5. Pitfalls

1. **cairosvg requiere `--break-system-packages`** en MicroVM sin venv — `pip install cairosvg --break-system-packages`
2. **ExtrudeGeometry con 2 colores** — no soporta multi-material por cara directamente. Solución: crear 2 shapes separados (mitad izq + mitad der) o usar vertex colors
3. **AdditiveBlending en partículas** — `depthWrite: false` obligatorio, si no las partículas tapan la geometría
4. **Importmap debe ir antes que el module script** — si no, Three.js no se resuelve
5. **Modelo sin visión** — no se pueden verificar logos visualmente. La geometría SVG debe ser correcta matemáticamente (coordenadas hardcodeadas, no generadas por IA)

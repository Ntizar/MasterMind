# Caso ARENA — Chorrada viral con Three.js

## Resumen
Proyecto web: reloj de arena 3D donde cada € = 1 grano de arena. La última gota del Mundial 2026 gana el 50% del bote. Cada usuario elige un país y su grano se colorea con la bandera.

## Flujo ejecutado (sesión junio 2026)

### 1. Ideación (iterativa)
- Primera propuesta: 10 ideas "de negocio" → David: "no estás siendo suficiente disruptivo"
- Segunda propuesta: 5 chorradas virales → David: "me encanta el reloj de arena"
- refinamiento: añadir banderas de países, giro de 100€, fecha límite Mundial

### 2. Construcción (una sesión)
- `index.html` — Layout: horaglass a la izquierda, info + pago a la derecha
- `css/style.css` — Estilo mármol griego: serif (Cormorant Garamond), dorado, crema
- `js/arena.js` — Three.js hourglass 3D + partículas + oscilación + spin
- `js/countries.js` — 47 selecciones con banderas y colores
- `server.js` — Express + SQLite + WebSocket + hashes SHA-256
- `Dockerfile` — Para NaN (node:20-alpine, usuario no-root, puerto 3000)

### 3. Despliegue
- GitHub Pages: repo público → API POST /pages → live en ~1 min
- URL: `https://ntizar.github.io/arena/`
- NaN: pendiente (requiere crear espacio en dashboard manualmente)

## Lecciones técnicas

### Three.js r128
- `MeshPhysicalMaterial` NO soporta `thickness` → quitar esa propiedad
- CanvasTexture para mármol procedural: radialGradients + lineas + flecks dorados
- Oscilación: `Math.sin(elapsed * speed) * range` en rotation.z
- Partículas: esferas tiny (0.03 radius) con color por país
- Spin: ease-out-cubic en rotation.z, 4s duración, 8 vueltas

### GitHub Pages
- API: `POST /repos/{owner}/{repo}/pages` con `source: {branch: "main", path: "/"}`
- Build time: ~30-60 segundos
- Solo sirve archivos estáticos (HTML/CSS/JS)
- Three.js CDN funciona perfecto
- No necesita build step (no Vite, no webpack)

### Patrón de diseño visual
- Fuente serif (Cormorant Garamond) + dorado (#c9a84c) = elegancia clásica
- Fondo crema (#f5f0eb) con gradientes radiales sutiles
- Cards con sombras suaves + bordes dorados al hover
- Countdown en header sticky
- Responsive: grid 2 col → 1 col en móvil

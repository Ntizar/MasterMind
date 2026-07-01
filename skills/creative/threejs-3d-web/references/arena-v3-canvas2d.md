# ARENA v3 — Referencia de implementación Canvas 2D

## Estructura del proyecto

```
arena/
├── Dockerfile          # node:20-alpine, PORT=7070, usuario no-root
├── package.json        # express, better-sqlite3, ws
├── server.js           # API REST + WebSocket + SQLite
├── index.html          # Sin Three.js, sin CDN externo
├── css/
│   ├── style.css       # Tema mármol + hash toast + spin card
│   └── arena-v2.css    # Grain detail, search, live feed
├── js/
│   ├── countries.js    # Lista de países con códigos y banderas
│   └── arena-v2.js     # Canvas 2D hourglass + física + UI
└── public/
    └── qr-paypal.jpg   # QR de pago
```

## Canvas 2D Hourglass — implementación clave

### Dimensiones
- Canvas: 320×520px (escala CSS mantiene aspect ratio)
- Bulbo: elipse de radio 110px
- Cuello: 20px de ancho

### Dibujo del reloj
```javascript
function drawHourglass() {
  // 1. Bulbo superior: ctx.ellipse(0, -R*1.1, R, R*1.1, 0, Math.PI, 0)
  // 2. Bulbo inferior: ctx.ellipse(0, R*1.1, R, R*1.1, 0, 0, Math.PI)
  // 3. Cuello: ctx.rect(-neck/2, -R*0.15, neck, R*0.3)
  // 4. Anillos dorados: ctx.ellipse con strokeStyle='#c9a84c'
  // 5. Granos: ctx.arc() por cada partícula
}
```

### Rotación 3D simulada
- No hay cámara 3D real
- Se acumula `rotationY` con drag del ratón
- En spin: `ctx.rotate(spinProgress * Math.PI * 2 * ROTATIONS)`
- Las partículas se dibujan en coordenadas del canvas, no del mundo 3D

### Física de partículas
```javascript
// Por frame (requestAnimationFrame):
g.vy += GRAVITY * dt;     // 0.0003
g.y += g.vy * dt;
g.x += g.vx * dt;
g.vy *= FRICTION;          // 0.998
g.vx *= FRICTION;

// Colisión con pared del bulbo:
// Calcular radio máximo en esa Y (elipse)
// Si |x| > maxR, clamp y rebotar
```

### Fases
- **accumulation**: gravedad desactivada, granos estáticos en fondo
- **competition**: gravedad activa, granos caen lentamente
- **closed**: todo congelado

## API endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /api/state | Estado actual del bote + fase |
| GET | /api/grains | Lista paginada de granos |
| GET | /api/grains/search?q= | Buscar por ID o nombre |
| GET | /api/grains/:id | Detalle de un grano |
| POST | /api/payment | Registrar pago (devuelve hash) |
| POST | /api/spin | Giro de 10€ (solo competición) |
| POST | /api/start-competition | Admin: iniciar competición |
| POST | /api/close | Cerrar bote (solo tras deadline) |
| GET | /api/winner | Info del ganador |
| GET | /api/events | Feed de eventos |

## WebSocket events

| Evento | Dirección | Datos |
|--------|-----------|-------|
| state | server→client | total, grainCount, phase, closed |
| grain:added | server→client | grainId, countryCode, amount, hash, posY, settled |
| grain:settled | server→client | grainId, posX, posY, posZ |
| spin | server→client | ownerName, grainsAffected |
| competition:start | server→client | grainsAffected |
| closed | server→client | winnerGrainId, winnerHash, totalGrains |

## Hash chain

```
GENESIS → hash(grano#1) → hash(grano#2) → ... → hash(grano#N)
                                                      ↓
                                        hash(último + timestamp)
                                                      ↓
                                        winnerOffset = hash % totalGrains
                                                      ↓
                                        winnerGrainId = totalGrains - winnerOffset
```

## Deploy en NaN.builders

- Dockerfile: `FROM node:20-alpine`, `ENV PORT=7070`, `EXPOSE 7070`
- Container port en dashboard: **7070** (debe coincidir)
- Auto-deploy: On push to main
- SQLite persiste entre deploys (volumen NaN)
- Para reset: borrar `arena.db` y redeploy
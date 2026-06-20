---
name: webapp-viral-rapida
version: "1.0.0"
description: Construir webapps virales y gamificadas de forma rápida — concepto absurdamente simple, visual impactante (Three.js), pagos integrados, deploy rápido. Patrón extraído de ARENA (reloj de arena Mundial 2026).
tags: [viral, gamificacion, pagos, prototype, rapida, canvas2d]
triggers: [webapp viral, app gamificada, proyecto viral, prototype rapido, app de pagos, promocion participativa, sorteo hash]
---

# Webapp Viral Rápida

Patrón para construir webapps con potencial viral: concepto de 2 segundos, visual impactante, mecánica de competencia/participación, pagos integrados, deploy en <1 día.

## Filosofía

La viralidad viene de 3 ingredientes:
1. **Concepto absurdo pero entendible** — "un pixel a 1$", "un grano de arena a 1€"
2. **Visual compartible** — la gente comparte capturas, no links
3. **Mecánica social** — competencia, progreso colectivo, FOMO

## Regla de oro: el usuario decide el stack visual

**PREGUNTAR siempre antes de asumir Three.js.** El usuario puede preferir:
- **Canvas 2D nativo** — más ligero, sin dependencias, mejor rendimiento en móvil
- **Three.js** — para 3D real, iluminación compleja, efectos de cámara
- **p5.js** — para arte generativo, shaders, interactividad creativa
- **CSS puro** — para animaciones 2D simples, sin canvas

**Señales de que el usuario NO quiere Three.js:**
- "no me convence el sistema de three.js"
- "es demasiado pesado"
- "en móvil va lento"
- "prefiero algo más simple"

En ese caso, **Canvas 2D nativo** es la alternativa correcta. Ofrece:
- Sin dependencias externas (ni CDN, ni build)
- Física de partículas igual de buena
- Rotación 3D simulada con transformaciones matriciales
- Mejor rendimiento en dispositivos low-end
- Código más mantenible y autocontenido

## Flujo de construcción

### FASE 1: Concepto (30 min)
- Definir la mecánica viral en 1 frase
- Verificar: ¿se entiende en 2 segundos? ¿da risa o genera curiosidad?
- Definir el "ganador" / recompensa / progreso
- **NO pensar en monetización aún** — primero que sea compartible

### FASE 2: Visual core (1-2 horas)
- Construir LO VISUAL PRIMERO — el hourglass, el muro, el mapa, lo que sea
- Three.js si necesita 3D, Canvas 2D si es 2D
- Estilo visual coherente (mármol, neón, pixel art, lo que encaje)
- Que se vea bien en captura de pantalla (750px width)

### FASE 3: Mecánica + pago (1-2 horas)
- Conectar la mecánica al visual (cada pago = acción visual)
- PayPal Checkout SDK para pagos rápidos
- WebSocket para tiempo real
- Base de datos SQLite para empezar

### FASE 4: Deploy (30 min)
- Dockerfile para NaN.builders
- Puerto no-root (3000+), HEALTHCHECK, usuario no-root
- Push a GitHub → NaN auto-deploy por polling

## Stack estándar

```
Frontend:  HTML vanilla + Canvas 2D (o Three.js si el usuario lo pide) + CSS
Backend:   Node.js + Express + better-sqlite3
Pagos:     PayPal Checkout SDK (o QR + webhook manual)
Real-time: WebSocket (ws)
Hash:      SHA-256 encadenado para transparencia
Deploy:    NaN.builders (Dockerfile, puerto >1024, usuario no-root)
```

## Patrón de reloj de arena (ARENA)

### Opción A: Canvas 2D nativo (recomendado para móvil)

```javascript
const CONFIG = {
  BULB_RADIUS: 110,       // px
  NECK_WIDTH: 20,         // px
  CANVAS_W: 320,
  CANVAS_H: 520,
  GRAVITY: 0.0003,        // por frame
  FRICTION: 0.998,
};

// Dibujar bulbo superior e inferior con ctx.ellipse()
// Cuello con rectángulo estrecho
// Anillos dorados con ctx.ellipse() + strokeStyle

// Partículas: array de {x, y, vx, vy, countryCode, settled, id}
// Cada grano se dibuja con ctx.arc() en su posición

// Rotación 3D simulada: acumular rotationY con drag del ratón
// Spin: animar spinProgress con requestAnimationFrame y easing cúbico
//   ctx.rotate(spinProgress * Math.PI * 2 * ROTATIONS)

// Física simplificada:
//   g.vy += GRAVITY * dt
//   g.y += g.vy * dt
//   g.x += g.vx * dt
//   g.vy *= FRICTION
//   Colisión con paredes del bulbo (elipse)
```

**Ventajas sobre Three.js:**
- 0 dependencias externas
- ~2KB de código vs ~150KB de Three.js
- Funciona en cualquier navegador sin CDN
- Más fácil de debuggear (inspeccionar canvas)
- Sin problemas de WebGL en dispositivos low-end

### Opción B: Three.js (para 3D real)

Usar solo si el usuario lo pide explícitamente o si necesita:
- Iluminación compleja (sombras, reflejos)
- Efectos de cámara (zoom, depth of field)
- Geometrías 3D reales (cilindros, esferas, toros)

### Mecánica de fases (ARENA)

```
FASE ACUMULACIÓN (hasta fecha X):
  - Granos caen al fondo y se quedan estáticos (settled=true)
  - Cada pago genera un hash SHA-256 único
  - El hash se muestra al usuario en un toast
  - Sin demo, sin granos falsos

FASE COMPETICIÓN (desde fecha X hasta fecha Y):
  - Giro violento: todos los granos vuelan arriba
  - Granos empiezan a caer lentamente uno a uno
  - Pagar 10€ empuja los granos del usuario hacia arriba
  - El último grano en caer gana

FASE CIERRE (desde fecha Y):
  - Se genera hash de cierre SHA-256
  - El hash determina el grano ganador (determinístico)
  - 50% del bote para el ganador
```

### Hash SHA-256 encadenado

```javascript
// Generación de hash por grano
function generateHash(prevHash, countryCode, ownerName) {
  return crypto.createHash('sha256')
    .update(`${prevHash}:${countryCode}:${ownerName}:${Date.now()}:${Math.random()}`)
    .digest('hex');
}

// Hash de cierre (determina ganador)
const winnerHash = crypto.createHash('sha256')
  .update(`${lastGrain.hash}:${closingTimestamp}`)
  .digest('hex');
const winnerOffset = parseInt(winnerHash.substring(0, 8), 16) % totalGrains;
const winnerGrainId = totalGrains - winnerOffset;
```

### Toast de confirmación con hash

Cuando un usuario compra, mostrar un toast con:
- ✅ "¡Grano registrado!"
- El hash SHA-256 completo (seleccionable, copiable)
- El número de grano (#ID)
- Botón "Copiar hash"
- Auto-cierre a los 15 segundos

Esto es **crítico para la confianza** — el usuario necesita una prueba tangible de su compra.

## Layout estándar

```
┌──────────────────────────────────────────┐
│  HEADER: Logo + Countdown                │
├──────────────────┬───────────────────────┤
│                  │  Cómo funciona (pasos) │
│  [VISUAL]        │  Estadísticas/Bote    │
│  (canvas 2D      │  Selector de país     │
│   o three.js)    │  Botones de pago      │
│                  │  [Giro] (solo comp.)  │
│  Buscador de     │  QR PayPal            │
│  granos/pixels   │                       │
├──────────────────┴───────────────────────┤
│  Feed de actividad en vivo               │
├──────────────────────────────────────────┤
│  Normas · Patrocinadores · Legal · FAQ   │
├──────────────────────────────────────────┤
│  FOOTER: Atribución                      │
└──────────────────────────────────────────┘
```

### Toast de hash (flotante sobre todo)
```
┌──────────────────────────────┐
│ ✅ ¡Grano registrado!    [✕] │
│ Tu código único:             │
│ ┌────────────────────────┐   │
│ │ a3f8c2d1... (SHA-256)  │   │
│ └────────────────────────┘   │
│ Guarda este código.          │
│ [📋 Copiar hash]             │
└──────────────────────────────┘
```

## Legal (sweepstakes, NO gambling)

- El pago es "donación con participación", no apuesta
- Términos y condiciones claros en la web
- Geo-restricción UE/EEE si hay premio real
- Ganador determinado por mecanismo verificable (hash SHA-256)
- Empresa/autónomo detrás para declarar ingresos

## Referencias

- `references/arena-v3-canvas2d.md` — Implementación completa de ARENA v3 con Canvas 2D: estructura, API, WebSocket, física, hash chain, deploy

## Pitfalls

- **NO empezar por el backend** — El visual es lo que se comparte. Primero que se vea bien.
- **NO pensar en escalabilidad antes de validar** — SQLite + 1 servidor aguanta miles de usuarios. No necesitas PostgreSQL para un prototype.
- **NO asumir Three.js** — Preguntar al usuario. Si dice "no me convence", usar Canvas 2D nativo.
- **NO poner demo automático** — Los granos falsos rompen la confianza. Solo granos reales de pagos reales.
- **NO mostrar el botón de giro en acumulación** — Solo visible durante la fase de competición.
- **PayPal Checkout SDK requiere `PAYPAL_CLIENT_ID` en env** — No hardcodear. Usar `.env.example` en repo + env vars en NaN dashboard.
- **NaN: Puerto >1024, usuario no-root, HEALTHCHECK en puerto configurado** — Si el contenedor crashea silenciosamente, revisar estos 3 puntos.
- **NaN: Container port en dashboard debe coincidir con EXPOSE y PORT env** — Si no coinciden, 502 Bad Gateway.
- **El concepto tiene que ser COMPARTIBLE en 1 frase** — Si necesitas explicarlo en 2 párrafos, es demasiado complejo. Simplificar.
- **David quiere DISRUPTIVO, no "negocio serio"** — Cuando pide ideas, pensar en chorradas virales (pixel wall, countdowns, confesiones), no en SaaS B2B.
- **Mostrar el visual en <5 min de inicio** — Si pasas 20 min en el backend sin mostrar nada visual, estás haciendo algo mal. Primero el wow, luego la lógica.
- **El hash es la prueba del usuario** — Sin hash visible, el usuario no tiene forma de demostrar que compró. Mostrarlo en un toast con botón de copiar.
- **La DB SQLite persiste entre deploys en NaN** — No borrar `arena.db` en producción. El volumen persiste aunque el contenedor se reconstruya.

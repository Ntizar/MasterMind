# Game/Simulation Project Architecture

Modular architecture for interactive 3D web applications: games, simulators, and visual experiences using Three.js + Vite.

## When to use

- Building a game, simulator, or interactive3D experience
- Project needs gamepad/keyboard input, physics, HUD overlay
- Three.js as the rendering engine
- Web-first with optional Electron desktop wrapper

## Architecture pattern

```
src/
├── engine/          # Core systems (no game logic)
│   ├── Renderer.js      # Three.js scene, camera, postprocessing
│   ├── InputManager.js  # Gamepad API + keyboard fallback
│   └── AudioManager.js  # Web Audio API, spatial sound
├── [domain]/        # Game-specific entities (drone/, ship/, character/)
│   ├── [Entity].js      # Model + physics + state
│   └── ...
├── track/           # Environment/level generation
│   ├── TrackBuilder.js  # Procedural or designed levels
│   ├── Checkpoint.js    # Progress markers
│   └── Obstacle.js      # Collision objects
├── game/            # Game logic (no rendering)
│   ├── GameManager.js   # State machine, scoring, difficulty
│   └── PowerUpManager.js
├── hud/             # 2D overlay on top of3D
│   └── HUD.js           # Speed, health, score display
├── ui/              # Menus, settings screens
│   ├── Menu.js
│   └── Settings.js
└── utils/           # Pure functions, constants
```

**Key principle:** Engine layer knows nothing about the game. Game layer knows nothing about rendering. HUD is a DOM overlay, not3D.

## Gamepad API pattern

```javascript
// Detection
window.addEventListener('gamepadconnected', (e) => {
  console.log(`Controller: ${e.gamepad.id}`);
  this.gamepadIndex = e.gamepad.index;
});

// Reading (call every frame)
const gamepads = navigator.getGamepads();
const pad = gamepads[this.gamepadIndex];
if (pad) {
  const leftStick = {
    x: applyDeadzone(pad.axes[0]),  // Yaw
    y: applyDeadzone(pad.axes[1])   // Throttle
  };
  const rightStick = {
    x: applyDeadzone(pad.axes[2]),  // Roll
    y: applyDeadzone(pad.axes[3])   // Pitch
  };
  const boost = pad.buttons[7]?.value || 0; // RT analog
}

// Deadzone
function applyDeadzone(value, deadzone = 0.15) {
  if (Math.abs(value) < deadzone) return 0;
  const sign = value > 0 ? 1 : -1;
  return sign * ((Math.abs(value) - deadzone) / (1 - deadzone));
}
```

**Pitfalls:**
- `navigator.getGamepads()` returns null if no gamepad — always check
- Deadzone must rescale output to 0-1 range, not just clamp to 0
- Some controllers have different axis mappings — detect by `gamepad.id`
- Keyboard fallback essential for testing without controller

## Three.js + Vite setup

```javascript
// vite.config.js
import { defineConfig } from 'vite'
export default defineConfig({
  build: {
    rollupOptions: {
      output: { manualChunks: { three: ['three'] } }
    }
  }
})

// Dynamic import in game init
const THREE = await import('three');
window.THREE = THREE;
```

**Pitfalls:**
- Three.js is ~600KB — always chunk separately
- Use `type="module"` in HTML for dynamic imports
- `window.THREE` pattern needed for shared access across modules
- Canvas must be created before Three.js renderer
- **GitHub Pages legacy mode (no workflow) does NOT serve ES6 modules.** If `type="module"` scripts silently fail, embed CSS+JS inline in a single HTML file. See `github-pages-modern-deploy` skill for details.
- **CRITICAL: `Object.assign(threeJsObject, {position: vec3})` CRASHES silently** — Three.js objects have read-only property getters (position, rotation, scale). Always use `.position.set(x,y,z)` or `.position.copy(vec)` instead. This bug produces NO console error message — just an empty `exception` with blank `message`. The page goes black with no visible error. See "Silent crash debugging" below.

## Three.js Pitfalls — Read-Only Properties

Three.js objects (Mesh, Light, Camera, Group) expose `position`, `rotation`, `scale` as **read-only getter properties** backed by internal Vector3/Euler objects. You CANNOT reassign them:

```javascript
// ❌ CRASHES — silent, no error message
Object.assign(light, { position: new THREE.Vector3(0, 10, 0) });
light.position = new THREE.Vector3(0, 10, 0);

// ✅ CORRECT — mutate the existing object
light.position.set(0, 10, 0);
light.position.copy(myVec3);
light.position.x = 0;
```

This applies to: `.position`, `.rotation`, `.scale`, `.quaternion` on any Three.js Object3D subclass.

**Also dangerous with Object.assign:**
```javascript
// ❌ May lose internal Three.js state
Object.assign(mesh, { position: vec, rotation: euler });

// ✅ Always use setters
mesh.position.copy(vec);
mesh.rotation.copy(euler);
```

## Silent Crash Debugging (Three.js)

When Three.js init crashes silently (page shows black/blank, no error in console):

1. **Check if elements exist:** `document.getElementById('mainMenu')` — if all return `null`, body is empty
2. **Check `document.body.innerHTML`** — if empty string, the JS crashed before DOM interaction
3. **Manually call init()** from console: `try { init(); } catch(e) { e.message + e.stack; }`
4. **The real error appears** — usually a TypeError with a blank message (Three.js internal errors often have empty `.message`)
5. **Check the stack trace** — it points to the exact line in setupLights/createDrone/etc.

**Pattern:** Empty `exception` in console with blank `message` field almost always means a Three.js read-only property assignment or missing dependency.

## Cyberpunk aesthetic palette

```css
--bg-dark: #0a0a1a;
--neon-green: #00ffaa;    /* Primary accent, checkpoints, trails */
--neon-blue: #00aaff;     /* Secondary, LEDs, UI elements */
--neon-pink: #ff3366;     /* Danger, warnings, back LEDs */
--neon-orange: #ff6600;   /* Track borders, obstacles */
--neon-yellow: #ffcc00;   /* Power-ups, combo indicator */
```

**Postprocessing stack (Three.js EffectComposer):**
1. Bloom — neon glow effect
2. Motion blur — speed sensation
3. Vignette — immersion
4. God rays — from light sources

**Neon material pattern:**
```javascript
const neonMaterial = new THREE.MeshStandardMaterial({
  color: 0x00ffaa,
  emissive: 0x00ffaa,
  emissiveIntensity: 1.0
});
```

## Procedural track generation

```javascript
// CatmullRomCurve3 for smooth paths
const curve = new THREE.CatmullRomCurve3([
  new THREE.Vector3(0, 0, 0),
  new THREE.Vector3(50, 0, 0),
  new THREE.Vector3(80, 0, 30),
  // ...
], true, 'catmullrom', 0.5);

// Get points along track
const position = curve.getPoint(t); // t = 0 to 1

// ExtrudeGeometry for track surface
const trackGeometry = new THREE.ExtrudeGeometry(trackShape, {
  steps: 200,
  extrudePath: curve
});
```

## HUD overlay pattern

DOM overlay on top of3D canvas — not3D text (which is unreadable at distance).

```html
<canvas id="gameCanvas"></canvas>
<div id="hud" class="hidden">
  <div class="hud-top">...</div>
  <div class="hud-bottom">...</div>
</div>
```

```css
#hud {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none; /* Click through to canvas */
  z-index: 50;
}
```

**Pitfalls:**
- `pointer-events: none` on HUD container, `pointer-events: auto` on interactive elements
- Use `font-variant-numeric: tabular-nums` for numbers that change
- Update HUD every frame but batch DOM reads/writes
- Sticks visualization: `transform: translate()` not `left/top` (GPU accelerated)

## Physics approach (semi-realistic)

### Simplified aerodynamics (arcade-lite)

Not a real physics engine — simplified aerodinamica:

```javascript
// Thrust based on pitch angle
const forwardForce = -Math.sin(pitchAngle) * thrust;
velocity.z += forwardForce * deltaTime;

// Gravity always applies
velocity.y += gravity * deltaTime;

// Drag (multiplicative per frame)
velocity.multiplyScalar(Math.pow(dragCoefficient, deltaTime * 60));

// Ground collision
if (position.y < groundHeight && velocity.y < 0) {
  position.y = groundHeight;
  velocity.y = 0;
}
```

### Realistic racing quad physics (recommended for simulators)

Full 6-DOF quad-motor model with aerodynamic thrust, inertia tensor, and two control modes:

```javascript
const DRONE = {
  mass: 1.2,                        // kg (5" racing quad)
  Ixx: 0.0082, Iyy: 0.0082,        // kg·m² roll/pitch inertia
  Izz: 0.0149,                      // kg·m² yaw inertia (higher — elongated)
  armLength: 0.1125,                // m (225mm frame / 2)
  rotorRadius: 0.0635,              // m (5" prop)
  airDensity: 1.225,                // kg/m³
  CT: 0.0105,                       // thrust coefficient
  CQ: 0.00045,                      // torque coefficient
  CD_body: 0.6,                     // body drag coefficient
  motorTimeConstant: 0.018,         // s (18ms spin-up)
  motorMinRPM: 2000, motorMaxRPM: 50000,
  maxThrustPerMotor: 28,            // N (112N total, TWR ~9.5:1)
  maxRollRate: 800 * DEG,           // rad/s (800°/s — pro racing)
  maxPitchRate: 800 * DEG,
  maxYawRate: 450 * DEG,
  groundEffectHeight: 0.127,        // 1 prop diameter
  groundEffectGain: 0.35,           // +35% lift near ground
};
```

**Motor mixing (X-config, 45° arms):**
```javascript
function motorMix(throttle, roll, pitch, yaw) {
  return [
    throttle + roll*0.25 - pitch*0.25 + yaw*0.12,  // FL (CW)
    throttle - roll*0.25 - pitch*0.25 - yaw*0.12,  // FR (CCW)
    throttle + roll*0.25 + pitch*0.25 - yaw*0.12,  // RL (CCW)
    throttle - roll*0.25 + pitch*0.25 + yaw*0.12,  // RR (CW)
  ].map(v => Math.max(0, Math.min(1, v)));
}
```

**Thrust model (per rotor, not simplified):**
```javascript
// F = CT × ρ × A × (Ω × R)² — real aerodynamic formula
const omegaRad = rpm * TAU / 60;
const F = CT * airDensity * rotorArea * Math.pow(omegaRad * rotorRadius, 2);
// Ground effect: extra lift when height < 1 prop diameter
if (pos.y < groundEffectHeight * 2) {
  F *= 1 + (1 - pos.y / (groundEffectHeight * 2)) * groundEffectGain;
}
```

**Quaternion-based rotation (not Euler) — CRITICAL for Three.js r128:**
```javascript
// Integrate quaternion: dq/dt = 0.5 × q × ω_quat
const omegaQuat = new THREE.Quaternion(angVelWorld.x, angVelWorld.y, angVelWorld.z, 0);
const qOmega = quat.clone().multiply(omegaQuat); // multiply() is VOID in r128!
// ❌ BROKEN: quat.clone().multiply(omegaQuat).multiplyScalar(0.5)
//    → multiplyScalar doesn't exist on Quaternion in r128
// ✅ CORRECT: multiply component-wise manually
const dq = new THREE.Quaternion(qOmega.x * 0.5, qOmega.y * 0.5, qOmega.z * 0.5, qOmega.w * 0.5);
quat.x += dq.x * dt; quat.y += dq.y * dt;
quat.z += dq.z * dt; quat.w += dq.w * dt;
quat.normalize();
```

**⚠️ Three.js r128 Quaternion API traps:**
- `Quaternion.multiply(q)` is **VOID** — does NOT return `this` for chaining. `q.copy(a).multiply(b)` returns `undefined` after `.multiply()`
- `Quaternion.multiplyScalar(s)` **DOES NOT EXIST** — must multiply components manually: `q.x *= s; q.y *= s; q.z *= s; q.w *= s;`
- These are version-specific: r125 and earlier may have different behavior. Always verify with `typeof quat.multiply` before chaining

**Gyroscopic coupling (Euler's rotation equation):**
```javascript
// τ = I × α + ω × (I × ω)
const gyroCoupling = new THREE.Vector3(
  angVel.y * angVel.z * (Iyy - Izz) / Ixx,
  angVel.x * angVel.z * (Izz - Ixx) / Iyy,
  angVel.x * angVel.y * (Ixx - Iyy) / Izz
);
```

**Two control modes:**
- **Rate mode** (acrobatic): sticks command angular velocity directly
- **Angle mode** (stable): sticks command target angle, P+D controller achieves it
- Toggle via button/key

**Key properties of realistic quad physics:**
- Motor response time (18ms) creates perceptible input lag
- Quaternion integration avoids gimbal lock
- Gyroscopic coupling: rolling affects pitch and vice versa
- Ground effect: +35% lift when <1 prop diameter from ground
- Drag scales with v² AND increases with tilt angle
- Camera shake from velocity AND acceleration
- Dynamic FOV widens with speed

**Pitfalls:**
- Without motor response time, the drone feels instant/unrealistic
- Quaternion integration must normalize every frame or drift accumulates
- `Object.assign` with Vector3/Euler on Three.js objects CRASHES — see pitfalls above
- Euler angles have gimbal lock at ±90° — use quaternions for integration
- **Three.js r128: Quaternion.multiply() is void, multiplyScalar() doesn't exist** — see r128 traps above
- **Auto-hover for flight games**: when no throttle input and altitude < threshold, apply counter-thrust equal to `mass * gravity / maxThrust` to simulate flight controller. Without this, drone falls to ground when player releases controls

## GitHub Pages CDN Caching Pitfall

When deploying to GitHub Pages legacy mode, the CDN can serve stale versions even after push:

**Symptoms:** `curl` shows new code, but browser runs old code. `resetPhys.toString()` shows old function body.

**Diagnosis:**
```javascript
// In browser console — check what code is actually loaded
const s = document.querySelector('script:last-of-type').textContent;
s.includes('yourNewFeature'); // true = new code loaded, false = stale
```

**Fix (browser console):**
```javascript
// Clear all caches and force reload
if ('caches' in window) {
  caches.keys().then(names => names.forEach(name => caches.delete(name)));
}
location.reload(true); // true = bypass cache, fetch from server
```

**Prevention:** Add cache-busting query strings to HTML: `<script src="app.js?v=TIMESTAMP">`

## Browser Automation Keyboard for Game Testing

Browser automation tools (browser_press) send keydown+keyup too fast for game loops — the key is pressed and released before the next animation frame reads it.

**Fix:** Mutate key state directly in browser console:
```javascript
// Instead of browser_press(key='w'), do:
keys['KeyW'] = true;
keys['ShiftLeft'] = true;
setTimeout(() => {
  keys['KeyW'] = false;
  keys['ShiftLeft'] = false;
}, 3000); // hold for 3 seconds
```

**Verification:**
```javascript
JSON.stringify({
  keys_pressed: Object.keys(keys).filter(k => keys[k]),
  speed: (phys.speed * 3.6).toFixed(1) + ' km/h',
  pos: {x: phys.pos.x.toFixed(1), y: phys.pos.y.toFixed(1), z: phys.pos.z.toFixed(1)},
})
```

## Rewrite vs Patch Decision Pattern

**When to rewrite from scratch instead of patching:**

| Signal | Action |
|--------|--------|
| File > 50K chars with 10+ patches | Consider rewrite |
| "It worked before but now it's broken" after multiple fixes | Rewrite |
| Each fix introduces new bugs | Rewrite |
| Can't reason about all interactions in the file | Rewrite |
| Patches contradict each other | Rewrite |

**How to rewrite safely:**
1. Keep old file as `index-old.html` (don't delete)
2. Write new clean version from scratch
3. Verify syntax: `node -e "new Function(scriptContent)"`
4. Test in browser before committing
5. Commit new version, delete old after verification

**Anti-pattern:** "Let me just fix this one more thing" × 10 → 84K char monolith with 1000+ errors/frame

## Desktop wrapper (Electron, optional)

```json
// package.json scripts
"electron:dev": "concurrently \"vite\" \"electron .\"",
"electron:build": "vite build && electron-builder"
```

**Pitfalls:**
- Electron adds ~150MB — only use if USB native access or offline needed
- `preload.js` bridges renderer ↔ main process for USB
- Web version works for 90% of users — Electron is optional enhancement

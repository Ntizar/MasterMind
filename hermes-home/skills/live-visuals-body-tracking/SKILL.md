---
name: live-visuals-body-tracking
description: "Patrón para construir procesadores VJ / visuales en vivo en el navegador — detección de cuerpo con MediaPipe Pose (33 landmarks), efectos Canvas 2D, reactividad audio con Web Audio API, arquitectura HTML autocontenido sin servidor. Para artistas, DJs, instalaciones."
version: "1.0.0"
category: creative
tags: [mediapipe, pose, body-tracking, vj, live-visuals, canvas, web-audio, creative-coding, cyberpunk, effects]
---

# Live Visuals with Body Tracking

## When to use

- Artist/DJ wants live visuals that react to their body movement via webcam
- Need real-time body tracking (not just bounding boxes) for visual effects
- Browser-based solution (no server, no install, just open HTML)
- Audio-reactive visuals for concerts, installations, VJ sets
- Cyberpunk/generative aesthetics driven by human motion

## When NOT to use

- Static generative art (use `p5js` instead)
- TouchDesigner pipelines (use `touchdesigner-mcp`)
- Object detection / counting (use `onnx-webgpu-inference`)
- Server-rendered visuals or GPU clusters needed

## Core Architecture

```
Webcam/Video → MediaPipe Pose (33 landmarks) → Effect Engine → Canvas 2D
                                        ↓
              Web Audio API (FFT) → beat/volume/freq data → effect parameters
```

**Key decision: MediaPipe Pose over YOLO**
- YOLO: bounding box only ("person here") — not enough for motion-driven effects
- MediaPipe Pose: 33 body landmarks + visibility — hands, elbows, shoulders, head, hips, knees, ankles
- 30+ FPS in browser, ~12MB model, no server needed
- CDN: `@mediapipe/pose` + `@mediapipe/camera_utils`

## Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Detection | MediaPipe Pose | 33 body landmarks in real-time |
| Audio | Web Audio API | FFT analysis, beat detection, BPM estimation |
| Rendering | Canvas 2D | Effect rendering with trail persistence |
| UI | Vanilla JS + CSS | Control panels, effect selector, audio visualizer |
| Deployment | GitHub Pages | Static hosting, HTTPS for camera access |

## MediaPipe Pose Setup

```html
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js" crossorigin="anonymous"></script>
```

```javascript
const pose = new Pose({
  locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
});

pose.setOptions({
  modelComplexity: 1,
  smoothLandmarks: true,
  enableSegmentation: false,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5,
});

pose.onResults((results) => {
  // results.poseLandmarks = Array of 33 landmarks
  // Each: { x: 0-1, y: 0-1, z: depth, visibility: 0-1 }
});

const camera = new Camera(videoElement, {
  onFrame: async () => { await pose.send({ image: videoElement }); },
  width: 640, height: 480,
});
await camera.start();
```

### Key Landmarks (33 points)

```
Head/Face:    0 (nose), 1-4 (eyes), 5-8 (ears), 9-10 (mouth)
Torso:        11-12 (shoulders), 23-24 (hips)
Left arm:     11→13→15→17→19→21 (shoulder→elbow→wrist→fingers)
Right arm:    12→14→16→18→20→22
Left leg:     23→25→27→29→31 (hip→knee→ankle→heel→foot)
Right leg:    24→26→28→30→32
```

### Data Extraction from Landmarks

```javascript
// Center of body (average of shoulders + hips + nose)
const keyIndices = [11, 12, 23, 24, 0];
const center = average(lm.filter((_, i) => keyIndices.includes(i)));

// Velocity (delta between frames)
const velocity = { x: (center.x - prevCenter.x) / dt, y: ... };

// Hands position
const leftHand = lm[19];  // Left wrist
const rightHand = lm[20]; // Right wrist

// Body contour (for outline effects)
const contourIndices = [11,13,15,17,19,21,19,17,15,13,11,12,14,16,18,20,22,...];
const contour = contourIndices.map(i => ({ x: lm[i].x, y: lm[i].y }));

// Aperture (distance between hands)
const aperture = distance(lm[19], lm[20]);

// Height (head to feet)
const height = Math.abs(lm[32].y - lm[0].y);
```

## Effect Engine Pattern

```javascript
class Effect {
  constructor(name, category, emoji, colors) { ... }
  init(canvas, ctx) {}
  onActivate() {}
  update(bodyData, audioData, dt) {}
  render(ctx, bodyData, audioData, w, h) {}
}

class EffectEngine {
  register(effect) { ... }
  setEffect(index) { ... }
  render(bodyData, audioData, dt) {
    // Trail persistence (fade previous frame)
    this.trailCtx.fillStyle = 'rgba(10,10,18,0.15)';
    this.trailCtx.fillRect(0, 0, w, h);
    // Active effect renders onto trail canvas
    this.active.render(this.trailCtx, bodyData, audioData, w, h);
    // Composite to main canvas
    ctx.drawImage(this.trailCanvas, 0, 0);
  }
}
```

### Trail Canvas for Persistent Effects

Key technique: use an offscreen canvas that fades each frame, so effects leave visual trails:

```javascript
// Each frame:
trailCtx.fillStyle = 'rgba(10,10,18,0.15)'; // Slow fade = long trails
trailCtx.fillRect(0, 0, w, h);
activeEffect.render(trailCtx, body, audio, w, h);
ctx.clearRect(0, 0, w, h);
ctx.drawImage(trailCanvas, 0, 0);
```

## Audio Reactivity

```javascript
class AudioAnalyzer {
  async init() {
    this.ctx = new AudioContext();
    this.analyser = this.ctx.createAnalyser();
    this.analyser.fftSize = 2048;
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.source = this.ctx.createMediaStreamSource(stream);
    this.source.connect(this.analyser);
  }

  update() {
    this.analyser.getByteFrequencyData(this.dataArray);
    // Split into bands:
    const bass = avg(dataArray[0..bassEnd]) / 255;    // 20-250 Hz
    const mid = avg(dataArray[bassEnd..midEnd]) / 255;  // 250-2000 Hz
    const treble = avg(dataArray[midEnd..end]) / 255;   // 2000+ Hz
    const volume = rms(dataArray) / 255;

    // Beat detection
    const energy = bass * 2 + mid + treble * 0.5;
    const avgEnergy = avg(energyHistory);
    this.beat = energy > avgEnergy * 1.4 && (now - lastBeat) > 250;
    // BPM from beat intervals...
  }
}
```

### Reactivity Modes

| Mode | Description |
|------|-------------|
| `hybrid` | Combines audio + movement (default) |
| `audio` | Only reacts to sound |
| `motion` | Only reacts to body movement |
| `manual` | Fixed parameters, no reactivity |

## Effect Categories (Cyberpunk Theme)

| Category | Effects | Visual Style |
|----------|---------|-------------|
| Ciberespacio | Grid Distortion, Matrix Rain, Circuit Board, Data Stream | Rejillas, código, datos |
| Luz Neón | Neon Tracer, Light Streaks, Glow Pulse, Neon Outline | Líneas brillantes, siluetas |
| Partículas | Constellation, Particle Burst, Star Field, Dust Storm | Puntos, explosiones, campo estelar |
| Onda/Energía | Shockwave, Energy Field, Sound Waves, Pulse Ring | Ondas, campos, pulsos |
| Espacio/VR | Portal Vortex, Warp Speed, Galaxy Spiral, Wormhole | Vórtices, galaxias, warp |
| Glitch/Retro | Glitch Body, VHS Static, Synthwave Sunset, Pixel Sort | Errors, retro, synthwave |

## GitHub Pages Deployment

```yaml
# .github/workflows/pages.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: { path: '.' }
      - uses: actions/deploy-pages@v4
        id: deployment
```

**Enable Pages via API:**
```bash
curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/pages \
  -d '{"build_type":"workflow","source":{"branch":"main","path":"/"}}'
```

## Pitfalls

- **HTTPS mandatory** — camera and microphone require secure context. GitHub Pages enforces HTTPS automatically.
- **Chrome/Edge recommended** — MediaPipe works best in Chromium browsers. Firefox has lower FPS.
- **MediaPipe WASM files** — first load downloads ~12MB of WASM. Show loading indicator.
- **Canvas resolution vs CSS size** — set canvas.width/height to fixed values (1280x720), let CSS scale. Don't use `window.innerWidth` directly or it pixelates on resize.
- **AudioContext suspended** — browsers block audio until user interaction. Call `audioCtx.resume()` on first click/keypress.
- **Landmark visibility** — always check `lm[i].visibility > 0.4` before using a landmark. Hidden landmarks produce erratic positions.
- **Trail canvas memory** — use `fillRect` with alpha for fading, never `clearRect` (kills trails). Fade factor 0.15 = medium trails, 0.05 = long trails, 0.3 = short trails.
- **Camera access blocks loading indefinitely** — if webcam is denied, unavailable, or MediaPipe init fails, `camera.start()` can hang forever. ALWAYS wrap MediaPipe init in try/catch + `Promise.race` with timeout (10-15s). The app must degrade gracefully: show message "Webcam no disponible — sube un vídeo o foto" and let the user continue with video/image backgrounds. See `references/defensive-loading-fallback.md`.
- **Loading overlay blocks browser permission dialog** — a `loadingOverlay` with `z-index: 1000` and solid background (`background: var(--bg)`) covers the entire viewport and **prevents the user from seeing/accepting the browser's `getUserMedia` permission prompt**. Fix: hide the loading overlay BEFORE calling `getUserMedia` (so the permission dialog is visible), then show it again only for the MediaPipe WASM download (~3-5s). Also use `rgba()` with transparency + `backdrop-filter: blur()` instead of solid `background` so the dialog is always partially visible.
- **`camera.start()` never rejects on some browsers** — MediaPipe's `Camera.start()` internally calls `getUserMedia`, but on some browsers it can stay in `pending` state forever (neither resolves nor rejects) if the user denies or the webcam is unavailable. Wrap in `Promise.race([camera.start(), timeoutPromise(12000)])` to guarantee progress.

## Performance Targets

| Metric | Target |
|--------|--------|
| FPS | 30+ minimum, 60 ideal |
| MediaPipe latency | < 50ms per frame |
| Particle count | 300-500 at 60fps (Canvas 2D) |
| Initial load | < 5 seconds (including WASM) |
| Memory | < 500MB |

## Project Structure

```
project/
  index.html          # Single self-contained file (HTML + CSS + JS)
  README.md           # Usage instructions
  .github/workflows/
    pages.yml         # GitHub Pages deployment
```

All code inline in index.html. No build step, no npm, no bundler. CDN for MediaPipe only.

## Related Skills

- `p5js` — Generative art with p5.js (different: static/animated art, not live body tracking)
- `touchdesigner-mcp` — Real-time visuals via TouchDesigner (requires TD installation)
- `onnx-webgpu-inference` — YOLO object detection (bounding boxes, not body landmarks)
- `creative--threejs-3d-web` — 3D WebGL scenes (different rendering approach)

## References

- `references/defensive-loading-fallback.md` — Patrón de fallback defensivo para MediaPipe/cámara: try/catch + timeout de 15s para evitar spinner infinito

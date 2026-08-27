# Real-time Body Detection + Visual Effects in Browser

## Overview
Pattern for building browser-based VJ processors, visual instruments, and body-tracking art tools. Single HTML file, zero server, webcam input → body landmarks → generative visuals.

**Proven in:** `blonde-vj-processor` (Ntizar/blonde-vj-processor) — 10 cyberpunk effects, MediaPipe Pose, Web Audio API.

## Architecture

```
Webcam / Video → MediaPipe Pose (33 landmarks) → Effect Engine → Canvas 2D/WebGL
                                         ↑
                        Web Audio API (FFT) → beat/mid/bass/treble
```

## Stack

| Component | Library | CDN |
|-----------|---------|-----|
| Body detection | MediaPipe Pose | `@mediapipe/pose` |
| Camera utils | MediaPipe Camera | `@mediapipe/camera_utils` |
| Rendering | Canvas 2D (or WebGL) | Native |
| Audio analysis | Web Audio API | Native |

## MediaPipe Pose Integration

### CDN Scripts
```html
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js" crossorigin="anonymous"></script>
```

### Initialization
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
  if (results.poseLandmarks) processBody(results.poseLandmarks);
});
const camera = new Camera(videoElement, {
  onFrame: async () => await pose.send({ image: videoElement }),
  width: 640, height: 480,
});
await camera.start();
```

### Key Landmarks (33 points)

| Index | Body part | Use in effects |
|-------|-----------|----------------|
| 0 | Nose | Head position, center anchor |
| 11-12 | Shoulders | Body width, torso reference |
| 13-14 | Elbows | Arm bend angles |
| 15-16 | Wrists | Hand positions, ray origins |
| 17-23 | Fingers | Detailed hand tracking |
| 23-24 | Hips | Body center, stance |
| 25-30 | Knees/Ankles | Lower body tracking |

### Derived Data (compute each frame)
```javascript
const center = avg(lm[0], lm[11], lm[12], lm[23], lm[24]);
const velocity = { x: (center.x - prevCenter.x) / dt, y: ... };
const height = Math.abs(lm[0].y - lm[32].y);
const leftHand = lm[19], rightHand = lm[20];
const aperture = dist(leftHand, rightHand);
const contourIndices = [11,13,15,17,19,21,19,17,15,13,11,12,14,16,18,20,22,20,18,16,14,12,24,26,28,30,32,30,28,26,24,23,25,27,29,31,29,27,25,23,11];
const contour = contourIndices.map(i => ({ x: lm[i].x, y: lm[i].y }));
```

## Web Audio API Integration

### Setup
```javascript
const audioCtx = new AudioContext();
const analyser = audioCtx.createAnalyser();
analyser.fftSize = 2048;
analyser.smoothingTimeConstant = 0.8;
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
audioCtx.createMediaStreamSource(stream).connect(analyser);
```

### Frequency Bands
```javascript
const dataArray = new Uint8Array(analyser.frequencyBinCount);
analyser.getByteFrequencyData(dataArray);
const binSize = audioCtx.sampleRate / analyser.fftSize;
const bass = avg(dataArray.slice(0, Math.floor(250/binSize))) / 255;
const mid = avg(dataArray.slice(Math.floor(250/binSize), Math.floor(2000/binSize))) / 255;
const treble = avg(dataArray.slice(Math.floor(2000/binSize))) / 255;
```

### Beat Detection
```javascript
const energy = bass * 2 + mid + treble * 0.5;
const isBeat = energy > avgEnergy * 1.4 && (now - lastBeatTime) > 250;
```

## Effect Patterns

### Trail (persistent rendering)
```javascript
trailCtx.fillStyle = 'rgba(10,10,18,0.15)';
trailCtx.fillRect(0, 0, w, h);
activeEffect.render(trailCtx, bodyData, audioData, w, h);
ctx.clearRect(0, 0, w, h);
ctx.drawImage(trailCanvas, 0, 0);
```

### Neon Glow
```javascript
ctx.shadowColor = neonColor; ctx.shadowBlur = 20 * audioMult;
ctx.stroke(); ctx.shadowBlur = 0;
```

### Particles (object pool, max 500)
```javascript
function spawn(x, y, audioMult) {
  if (particles.length >= 500) return;
  particles.push({ x, y, vx, vy, life: 1, size: 2+Math.random()*4 });
}
```

### Grid Body Distortion
```javascript
const d = Math.sqrt((x-cx)**2 + (y-cy)**2);
if (d < bodyRadius*2) {
  const force = (1 - d/(bodyRadius*2)) * 40;
  x += Math.cos(angle) * force * Math.sin(t*3);
}
```

## Pitfalls

1. **HTTPS required** — Camera/mic need secure context
2. **MediaPipe WASM** — First load downloads ~12MB. Show loading indicator
3. **`pose.send()` is async** — Let Camera handle frame timing
4. **Trail canvas** — Use `fillRect` alpha fade, NOT `clearRect`
5. **Shadow blur perf** — Reset `shadowBlur = 0` after each stroke
6. **Video mirroring** — `ctx.translate(w,0); ctx.scale(-1,1)` for correct L/R
7. **Beat threshold** — 1.4x avg energy works generally; lower to 1.2x for bass-heavy music
8. **Particle GC** — `splice()` in loops causes pauses. Mark dead, recycle

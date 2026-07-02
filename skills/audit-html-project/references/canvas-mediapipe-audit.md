# Canvas + MediaPipe + Web Audio — Patrones de Auditoría y Mejora

Patrones extraídos de la auditoría y mejora de `blonde-vj-processor` (single-file HTML, Canvas 2D + MediaPipe Pose + Web Audio API, 15 efectos visuales, 2.913 líneas).

## Arquitectura de clases de efecto

```javascript
class Effect {
  constructor(ctx, canvas) {
    this.ctx = ctx;
    this.canvas = canvas;
    this.colors = ['#00ffff', '#ff00ff'];
    this._dt = 0.016; // default delta time
  }

  update(poseData, dt) {
    this._dt = dt || 0.016; // ALMACENAR para que render() tenga acceso
    // ... update logic
  }

  render() {
    // Usar this._dt, NO dt como parámetro
    this.angle += this._dt * 0.5;
    // ... render logic
  }

  getContour(poseData) {
    // Método compartido — mover a base si 3+ subclases lo duplican
    // ... contour extraction from pose landmarks
  }
}
```

**Regla:** `update()` recibe `dt` del game loop. `render()` NO recibe parámetros. Solución: almacenar `this._dt` en `update()`.

## MediaPipe CDN version pinning

```html
<!-- MAL: sin versión, puede romper en cualquier update del CDN -->
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js"></script>

<!-- BIEN: versión fijada -->
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils@0.3.1675466862/camera_utils.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/pose.js"></script>
```

**Detección:** `grep -oP '@mediapipe/[a-z_]+@\K[0-9.]+' index.html` — si no hay output, no hay version pinning.

## Stream cleanup al cambiar fuente

```javascript
async function startCamera() {
  // PARAR streams anteriores antes de getUserMedia
  if (video.srcObject) {
    video.srcObject.getTracks().forEach(t => t.stop());
  }

  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;
}
```

Sin esto, cada cambio de fuente acumula un stream activo → webcam bloqueada + CPU innecesaria.

## MediaRecorder con mimeType fallback

```javascript
function toggleRecording() {
  if (!mediaRecorder || mediaRecorder.state === 'inactive') {
    const stream = canvas.captureStream(30); // 30 FPS

    // Cadena de fallback: VP9 → VP8 → WebM genérico
    const mimeTypes = [
      'video/webm;codecs=vp9',
      'video/webm;codecs=vp8',
      'video/webm'
    ];
    const mimeType = mimeTypes.find(t => MediaRecorder.isTypeSupported(t)) || '';

    mediaRecorder = new MediaRecorder(stream, {
      mimeType,
      videoBitsPerSecond: 5000000 // 5 Mbps
    });

    const chunks = [];
    mediaRecorder.ondataavailable = e => { if (e.data.size > 0) chunks.push(e.data); };
    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `vj-session-${Date.now()}.webm`;
      a.click();
      URL.revokeObjectURL(url);
    };

    mediaRecorder.start();
  } else {
    mediaRecorder.stop();
  }
}
```

## Canvas snapshot (PNG)

```javascript
function takeSnapshot() {
  const dataUrl = canvas.toDataURL('image/png');
  const a = document.createElement('a');
  a.href = dataUrl;
  a.download = `vj-snapshot-${Date.now()}.png`;
  a.click();
}
```

## localStorage persistence con auto-save

```javascript
class VJProcessor {
  constructor() {
    this.loadConfig();        // Cargar antes de buildUI
    this.buildUI();
    this.applyLoadedConfig(); // Aplicar después de construir UI

    // Auto-save cada 5 segundos
    setInterval(() => this.saveConfig(), 5000);
  }

  saveConfig() {
    const config = {
      activeEffect: this.activeEffectIndex,
      colors: this.colors,
      // ... otros parámetros
    };
    localStorage.setItem('vj-config', JSON.stringify(config));
  }

  loadConfig() {
    try {
      const saved = localStorage.getItem('vj-config');
      if (saved) this._loadedConfig = JSON.parse(saved);
    } catch (e) { /* ignore corrupt JSON */ }
  }

  applyLoadedConfig() {
    if (!this._loadedConfig) return;
    if (this._loadedConfig.colors) this.colors = this._loadedConfig.colors;
    if (this._loadedConfig.activeEffect != null) {
      this.transitionToEffect(this._loadedConfig.activeEffect);
    }
  }
}
```

**Orden crítico:** `loadConfig()` → `buildUI()` → `applyLoadedConfig()`. Si se aplica antes de construir la UI, los elementos no existen y falla silenciosamente.

## CSS bloom post-processing

```css
#canvas {
  filter: drop-shadow(0 0 8px rgba(0, 255, 255, 0.3))
          drop-shadow(0 0 16px rgba(255, 0, 255, 0.2))
          saturate(1.3);
}
```

Más ligero que post-processing WebGL. No es tan configurable pero funciona sin shaders ni framebuffer overhead.

## Transition overlay entre efectos

```html
<div id="transition-overlay"></div>
```

```css
#transition-overlay {
  position: fixed;
  inset: 0;
  background: #000;
  opacity: 0;
  pointer-events: none;
  transition: opacity 250ms ease;
  z-index: 1000;
}
#transition-overlay.active { opacity: 1; }
```

```javascript
transitionToEffect(index) {
  const overlay = document.getElementById('transition-overlay');
  overlay.classList.add('active');

  setTimeout(() => {
    this.activeEffectIndex = index;
    this.effects[index].reset?.();
    overlay.classList.remove('active');
  }, 250);
}
```

## HSL→hex para colores neón coherentes

```javascript
// MAL: RGB aleatorio → colores deslavados, sin coherencia visual
function addColorRandom() {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`;
}

// BIEN: HSL con saturación y luminosidad fijas → neón coherente
function addColorNeon() {
  const hue = Math.random() * 360;
  const s = 0.9;  // 90% saturación
  const l = 0.55; // 55% luminosidad
  return hslToHex(hue, s, l);
}

function hslToHex(h, s, l) {
  l /= 100;
  const a = s * Math.min(l, 1 - l);
  const f = n => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');
  };
  return `#${f(0)}${f(8)}${f(4)}`;
}
```

## Verificación post-modificación

Tras añadir features a un single-file HTML con Canvas:

```bash
# 1. JS syntax check (extraer <script> inline a archivo temporal)
node --check /tmp/extracted.js

# 2. Balance de tags
python3 -c "
content = open('index.html').read()
print(f'Divs: {content.count(\"<div\")}/{content.count(\"</div>\")}')
print(f'Braces: {content.count(\"{\")}/{content.count(\"}\")}')
print(f'Parens: {content.count(\"(\")}/{content.count(\")\")}')"

# 3. Funciones onclick definidas
python3 -c "
import re
content = open('index.html').read()
onclick_fns = set(re.findall(r'onclick=\"([a-zA-Z_]+)\(', content))
defined_fns = set(re.findall(r'function\s+([a-zA-Z_]+)\s*\(', content))
missing = onclick_fns - defined_fns
print(f'Missing: {missing}' if missing else 'All onclick functions defined')"
```

## Detección de bugs comunes en Canvas + MediaPipe

| Bug | Síntoma | Detección |
|-----|---------|-----------|
| `dt` undefined en `render()` | Efecto no anima o salta (NaN propagation) | `grep -n 'render(dt)' index.html` — si render recibe dt como param pero el caller no lo pasa |
| MediaPipe sin pinning | App deja de funcionar tras update CDN | `grep -oP '@mediapipe/[a-z_]+@\K[0-9.]+'` — sin output = sin pinning |
| Streams acumulados | Webcam bloqueada tras cambiar fuente | Buscar `getUserMedia` sin `getTracks().forEach(t => t.stop())` antes |
| onclick a ID incorrecto | Botón no hace nada al click | Comparar IDs en `onclick="X.click()"` con IDs reales en HTML |
| Método duplicado en subclases | Código repetido, difícil de mantener | Contar definiciones del mismo método por clase |

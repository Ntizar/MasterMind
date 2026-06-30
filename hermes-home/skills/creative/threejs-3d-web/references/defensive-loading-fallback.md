# Defensive Loading Fallback para MediaPipe/Webcam

## El problema

`camera.start()` de MediaPipe puede colgarse indefinidamente si:
- No hay webcam disponible
- El usuario niega permisos de cámara
- La red es lenta y los WASM tardan en cargar
- HTTPS no funciona (HTTP puro bloquea getUserMedia)

**Síntoma:** spinner de carga permanente, app inaccesible.

## Patrón de solución (4 capas)

### 1. Ocultar overlay ANTES de pedir permisos

El `loadingOverlay` con `z-index: 1000` y fondo sólido tapa el dialog de permisos del navegador. El usuario no puede ver ni aceptar el prompt de `getUserMedia`.

```javascript
async startWebcam() {
  try {
    // 1) Ocultar overlay ANTES de getUserMedia
    const loading = document.getElementById('loadingOverlay');
    if (loading) loading.classList.add('hidden');

    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' }
    });

    // 2) Mostrar overlay de nuevo mientras carga MediaPipe WASM
    if (loading) loading.classList.remove('hidden');

    // 3) Iniciar MediaPipe
    await this.detector.init(onResults);
  } catch (e) {
    if (loading) loading.classList.add('hidden');
    // fallback UI...
  }
}
```

### 2. Overlay semitransparente como fallback

Si por alguna razón el overlay no se oculta a tiempo, hazlo semitransparente:

```css
.loading-overlay {
  background: rgba(10,10,18,0.85); /* NO var(--bg) sólido */
  backdrop-filter: blur(4px);       /* permite ver lo de detrás */
  z-index: 1000;
}
```

### 3. Promise.race en camera.start()

`camera.start()` puede quedarse en pending eterno en algunos navegadores:

```javascript
try {
  await Promise.race([
    this.camera.start(),
    new Promise((_, reject) => setTimeout(() => reject(new Error('camera timeout')), 12000))
  ]);
  // OK
} catch (e) {
  // timeout o error → degradar
}
```

### 4. Timeout de seguridad en el constructor

```javascript
async init(onResults) {
  this.pose = new Pose({ locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}` });
  this.pose.setOptions({ modelComplexity: 1, smoothLandmarks: true, ... });
  this.pose.onResults((results) => { ... });

  this.camera = new Camera(this.video, {
    onFrame: async () => { if (this.pose && !CONFIG.paused) await this.pose.send({ image: this.video }); },
    width: 640, height: 480,
  });

  try {
    await this.camera.start();
    this.ready = true;
    document.getElementById('loadingOverlay').classList.add('hidden');
  } catch (e) {
    console.warn('MediaPipe init failed:', e);
    document.getElementById('loadingOverlay').classList.add('hidden');
  }
}
```

### 2. Timeout de seguridad en el constructor

```javascript
// En VJProcessor constructor:
this._loadTimeout = setTimeout(() => {
  console.warn('MediaPipe load timeout — degrading gracefully');
  if (this.detector && this.detector.startFallback) {
    this.detector.startFallback();
  }
}, 15000); // 15 segundos máximo
```

### 3. Método fallback que limpia el loading

```javascript
async startFallback() {
  document.getElementById('loadingOverlay').classList.add('hidden');
  document.getElementById('noDetection').classList.remove('hidden');
  document.getElementById('noDetection').querySelector('.text').textContent =
    'Webcam no disponible — sube un vídeo o foto';
}
```

### 4. Limpiar timeout si MediaPipe carga OK

```javascript
// Al final del try en init():
if (window._vjApp && window._vjApp._loadTimeout) {
  clearTimeout(window._vjApp._loadTimeout);
  window._vjApp._loadTimeout = null;
}
```

## Decisiones

| Timeout | Por qué |
|---------|---------|
| 10s | Demasiado agresivo para redes lentas |
| **15s** | Buen equilibrio — MediaPipe normal carga en 3-5s, conexiones malas en ~12s |
| 20s+ | Demasiado tiempo esperando |

## Variables de contexto

- **GitHub Pages:** HTTPS automático, pero puede servir caché viejo. El hash URL (`?t=`) fuerza refresh.
- **CDN jsDelivr:** Generalmente rápido, pero puede fallar en regiones con mala conectividad a China/Rusia.
- **Webcam permission:** Si niega, `getUserMedia` rechaza inmediatamente → el try/catch lo atrapa.
- **MediaPipe WASM:** Son los que más tardan (~12MB). Si fallan, la app sigue sin cámara pero los efectos funcionan.

## Comprobación post-deploy

```bash
# Verificar que el fallback está en el HTML servido
curl -s https://user.github.io/repo/ | grep -c 'startFallback'
# Debe devolver 1+

# Verificar timeout
curl -s https://user.github.io/repo/ | grep -c '_loadTimeout'
# Debe devolver 1+
```

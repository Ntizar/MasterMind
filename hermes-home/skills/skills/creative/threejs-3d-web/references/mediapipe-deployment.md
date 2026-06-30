# MediaPipe Pose Integration & Deployment Notes

## MediaPipe CDN URLs (as of June 2026)

```
https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js
https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js
```

WASM files auto-loaded from: `https://cdn.jsdelivr.net/npm/@mediapipe/pose/`

## Camera Setup Pattern

```javascript
const camera = new Camera(videoElement, {
  onFrame: async () => {
    await pose.send({ image: videoElement });
  },
  width: 640,
  height: 480,
});
await camera.start();
```

**Critical**: `Camera` from `@mediapipe/camera_utils` wraps `getUserMedia` and sends frames to MediaPipe. Don't call `getUserMedia` separately.

## Video Input (file/URL) Alternative

When using uploaded video instead of webcam:
1. Set `video.src = URL.createObjectURL(file)` (not srcObject)
2. Call `video.play()` 
3. In the `onFrame` callback, send the video element to MediaPipe
4. MediaPipe processes each frame as it arrives

```javascript
// File input handler
function loadVideo(event) {
  const file = event.target.files[0];
  const video = document.getElementById('webcamVideo');
  video.srcObject = null;
  video.src = URL.createObjectURL(file);
  video.loop = true;
  video.play();
}
```

## Webcam Mirroring

For selfie-style presentation, mirror the canvas horizontally:
```javascript
if (CONFIG.mirrored) {
  ctx.translate(canvas.width, 0);
  ctx.scale(-1, 1);
}
ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
```

**Important**: Landmarks from MediaPipe are already in video coordinates. If you mirror the canvas for display, the landmarks will appear correct (following the mirrored video). Don't mirror the landmarks themselves.

## Visibility Threshold

Always filter landmarks by visibility before using them:
- `visibility > 0.5` — reliable, use for main effects
- `visibility > 0.3` — usable but may jitter
- `visibility < 0.3` — unreliable, skip

Lower visibility means the model is less confident about that landmark position (e.g., occluded body parts).

## GitHub Pages Deployment

### API Call to Enable Pages

```bash
# Create Pages site with workflow build
curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/pages \
  -d '{"build_type":"workflow","source":{"branch":"main","path":"/"}}'
```

### Response

```json
{
  "html_url": "https://OWNER.github.io/REPO/",
  "status": null,
  "build_type": "workflow",
  "source": {"branch": "main", "path": "/"},
  "public": true,
  "https_enforced": true
}
```

### Workflow File

Uses `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`.
The artifact uploads the repo root (`path: '.'`), so `index.html` is served at the root URL.

### Timing

- Workflow triggers on push to main
- Typically completes in 20-40 seconds
- Pages URL becomes available immediately after workflow success
- First visit may take 5-10 seconds (cold start)

## AudioContext Resume

Browsers block AudioContext until user gesture. Resume on first interaction:

```javascript
document.addEventListener('click', () => {
  if (audioCtx.state === 'suspended') audioCtx.resume();
}, { once: true });
```

Or resume inside the `init()` method after `getUserMedia` succeeds (the permission prompt counts as user gesture).

## Performance: Frame Skipping

On slow hardware, skip MediaPipe inference on some frames:

```javascript
let frameSkip = 0;
onFrame: async () => {
  frameSkip++;
  if (frameSkip % 2 === 0) return; // Skip every other frame
  await pose.send({ image: videoElement });
}
```

Or detect hardware and adjust:
```javascript
const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
const gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
// Classify: 'M1'/'RTX' = high, 'UHD'/'Intel' = medium, else = low
```

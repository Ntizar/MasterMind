---
name: webgpu-onnx-detection
version: "1.0.0"
category: computer-vision
description: Ejecutar modelos de visión por computador (YOLO, etc.) en el navegador con WebGPU/ONNX sin servidor GPU. Basado en YoloConteo.
tags: [computer-vision, WebGPU, ONNX, YOLO]

---

# WebGPU + ONNX — Detección de Objetos en Navegador

## Resumen

Patrón para ejecutar modelos de visión por computador (YOLO, etc.) directamente en el navegador usando WebGPU, sin servidor GPU ni backend. Basado en el proyecto YoloConteo de Ntizar.

## Cuándo Usar

- Necesitas detección de objetos en tiempo real sin servidor
- Quieres que la IA corra en el dispositivo del usuario
- Necesitas privacidad (datos nunca salen del dispositivo)
- Quieres deploy estático (GitHub Pages, Vercel, Netlify)

## Pasos

### 1. Preparar el Modelo ONNX

```bash
pip install ultralytics onnx
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt').export(format='onnx')"
# Modelo resultante: yolov8n.onnx (~12 MB)
```

### 2. Backend Python (Opcional — para deploy Vercel)

```python
# detector.py — YOLOv8 + ByteTrack
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.confidence = 0.25
    
    def track_frame(self, frame):
        results = self.model.track(
            frame, persist=True, tracker='bytetrack.yaml',
            conf=self.confidence, verbose=False
        )
        return detections
```

### 3. Frontend WebGPU (ONNX Runtime Web)

```html
<script src="https://cdn.jsdelivr.net/npm/onnxruntime-web/ort.webgpu.min.js"></script>
<script type="module">
  const session = await ort.InferenceSession.create(
    'yolov8n.onnx',
    { executionProviders: ['webgpu'] }
  );
  
  async function detect(frame) {
    const tensor = preprocess(frame);
    const feeds = { images: tensor };
    const results = await session.run(feeds);
    return postprocess(results);
  }
</script>
```

### 4. Conteo Bidireccional con Línea Virtual

```javascript
class Counter {
  constructor(lineY) {
    this.lineY = lineY;
    this.counts = { up: 0, down: 0 };
    this.trackedPositions = new Map();
  }
  
  update(detections) {
    for (const det of detections) {
      const prevY = this.trackedPositions.get(det.track_id);
      if (prevY !== undefined) {
        if (prevY > this.lineY && det.centro.y < this.lineY) this.counts.up++;
        else if (prevY < this.lineY && det.centro.y > this.lineY) this.counts.down++;
      }
      this.trackedPositions.set(det.track_id, det.centro.y);
    }
  }
}
```

## Despliegue

La carpeta del proyecto es completamente autocontenida (HTML + JS + CSS + modelo ONNX). Sirve como sitio estatico en cualquier hosting:

- **Vercel** — conecta el repo, directorio de publicacion, sin build command
- **Netlify** — mismo proceso que Vercel
- **GitHub Pages** — `git subtree push --prefix web origin gh-pages`

> HTTPS es obligatorio en produccion para que funcionen la camara y el GPS.

## Pipeline Completo

```
Camara -> YOLOv8n (ONNX/WebGPU) -> Tracker IoU -> Contador bidireccional -> Resultados en pantalla
```

## Objetos Detectados (COCO)

| Objeto | Emoji |
|--------|-------|
| Personas | 👤 |
| Bicicletas | 🚲 |
| Coches | 🚗 |
| Motos | 🏍️ |
| Autobuses | 🚌 |
| Camiones | 🚛 |

## Rendimiento Esperado

| Backend | FPS | Requisito |
|---------|-----|-----------|
| WebGPU | 20-40+ | Chrome/Edge 113+ |
| WASM | 5-15 | Cualquier navegador moderno |

En movil se optimiza automaticamente saltando frames de inferencia para mantener fluidez.

## Pitfalls

- WebGPU solo funciona en HTTPS o localhost
- Móvil: optimizar saltando frames de inferencia para mantener fluidez
- Tamaño modelo: YOLOv8n (~12 MB) se cachea tras primera carga
- Siempre implementar WASM como fallback para WebGPU
- ByteTrack: preferir tracker built-in de Ultralytics sobre DeepSort
- **HTTPS obligatorio** — la camara y GPS requieren contexto seguro
- **Modelo grande** — yolov8n.onnx ~12 MB, descargar una vez y cachear
- **Licencia AGPL-3.0** — YOLOv8 de Ultralytics usa AGPL-3.0

## Archivos de Referencia

- YoloConteo: https://github.com/Ntizar/YoloConteo
- Deploy: https://yolo-conteov2.vercel.app
- Licencia: AGPL-3.0

## Variables Clave

```python
YOLO_MODEL_PATH = "yolov8n.onnx"
CONFIDENCE_THRESHOLD = 0.25
TRACKER = "bytetrack.yaml"
COCO_CLASSES = ["person", "bicycle", "car", "motorcycle", "bus", "truck"]
```

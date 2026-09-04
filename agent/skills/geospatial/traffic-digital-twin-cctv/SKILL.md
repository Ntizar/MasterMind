---
name: traffic-digital-twin-cctv
version: "1.0.0"
description: "Digital twin de tráfico desde footage CCTV — detecta, cuenta y rastrea vehículos usando solo video mp4 de cámaras. Inspirado en duy-phamduc68/TrafficLab-3D (⭐315)."
tags: [traffic, digital-twin, cctv, computer-vision, yolo, tracking, 3d]
---

# Digital Twin de Tráfico desde CCTV

## Resumen

Crea un digital twin de tráfico usando solo footage de cámaras CCTV (mp4). Detecta vehículos con YOLO, rastrea con DeepSORT, y reconstruye posiciones 3D en un mapa. Sin sensores adicionales.

## Cuándo usar

- Análisis de tráfico urbano desde cámaras existentes
- Digital twin de intersección o tramo de carretera
- Conteo y clasificación de vehículos sin hardware adicional
- Visualización 3D de flujo de tráfico

## Arquitectura

```
Video CCTV (mp4)
  ↓ Frame extraction (cv2)
  ↓ YOLO detection (coches, camiones, motos, buses)
  ↓ DeepSORT tracking (ID por vehículo)
  ↓ Homography: pixel → coordenadas reales
  ↓
Digital Twin 3D
  ├── Mapa 3D de la zona
  ├── Vehículos como meshes animados
  ├── Trayectorias históricas
  └── Métricas: conteo, velocidad, densidad
```

## Patrón de uso

```python
import cv2
from ultralytics import YOLO
from deep_sort_realtime import DeepSort

# 1. Cargar modelo YOLO
model = YOLO('yolov8n.pt')
tracker = DeepSort(max_age=30)

# 2. Procesar video CCTV
cap = cv2.VideoCapture('cctv_footage.mp4')
detections_log = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # Detectar vehículos
    results = model(frame, classes=[2, 3, 5, 7])  # car, motorcycle, bus, truck
    
    # Formatear para DeepSORT
    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = box.conf[0].item()
        detections.append(([x1, y1, x2-x1, y2-y1], conf, int(box.cls)))
    
    # Tracking
    tracks = tracker.update_tracks(detections, frame=frame)
    
    for track in tracks:
        if not track.is_confirmed(): continue
        track_id = track.track_id
        bbox = track.to_tlbr()
        
        # Homography: pixel → coordenadas reales
        real_pos = pixel_to_world(bbox_center(bbox), homography_matrix)
        detections_log.append({
            'id': track_id,
            'position': real_pos,
            'class': track.get_det_class(),
            'frame': frame_count
        })

# 3. Exportar para visualización 3D
import json
json.dump(detections_log, open('traffic_data.json', 'w'))
```

```javascript
// Visualización 3D del digital twin
const trafficData = await loadJSON('traffic_data.json');

// Agrupar por vehículo
const vehicles = groupByID(trafficData);

vehicles.forEach(v => {
  // Crear mesh para cada vehículo
  const mesh = new THREE.Mesh(vehicleGeometry, vehicleMaterial);
  scene.add(mesh);
  
  // Animar trayectoria
  v.positions.forEach((pos, i) => {
    setTimeout(() => {
      mesh.position.set(pos.x, 0, pos.z);
    }, i * 33); // 30fps
  });
});
```

## Pitfalls

- **Homography:** Necesita calibración: 4+ puntos conocidos en la imagen → coordenadas reales.
- **Oclusiones:** YOLO falla con oclusiones. DeepSORT ayuda a mantener ID durante oclusiones cortas.
- **Perspective:** Cámaras con ángulo muy pronunciado dificultan la detección. Mejor ángulo cenital.
- **Night mode:** YOLO falla con poca luz. Usar modelo entrenado para night o IR.
- **Frame rate:** Procesar a 10-15fps es suficiente para tráfico. 30fps = más datos pero más costoso.

## Referencias

- TrafficLab-3D: https://github.com/duy-phamduc68/TrafficLab-3D
- YOLO: https://github.com/ultralytics/ultralytics
- DeepSORT: https://github.com/levanons/deep-sort-pytorch

---

**Hecho con ❤️ por David Antizar**

## Comparativa de alternativas

- **[Barath19/Boxer3D](https://github.com/Barath19/Boxer3D)** — eleva la detección 2D a cajas 3D orientadas (OBB) con BoxerNet para digital twin; el paso de 2D→3D que este skill necesita para el gemelo digital.

---
name: cctv-yolo
description: Detección de objetos YOLO para cámaras CCTV — tráfico, vehículos, personas en tiempo real.
version: "1.0.0"
tags: [YOLO, CCTV, detection, traffic, vehicles, real-time, CV]
---

# CCTV YOLO — Detección para Cámaras de Seguridad

## Resumen

Detección de objetos YOLO para cámaras CCTV — tráfico, vehículos, personas en tiempo real. 624⭐.

## Repo de referencia

- **GitHub:** `github.com/SanshruthR/CCTV_YOLO`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install ultralytics opencv-python numpy
# O clonar
git clone https://github.com/SanshruthR/CCTV_YOLO.git
cd CCTV_YOLO && pip install -r requirements.txt
```

## Uso Básico

```python
import cv2
from ultralytics import YOLO

# Cargar modelo YOLO
model = YOLO("yolov8n.pt")

# Detectar en video de CCTV
cap = cv2.VideoCapture("cctv_feed.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Inferencia
    results = model(frame, conf=0.25)
    
    # Dibujar resultados
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = model.names[int(box.cls)]
            conf = box.conf[0]
            pts = box.xyxy[0].int().tolist()
            cv2.rectangle(frame, (pts[0], pts[1]), (pts[2], pts[3]), 
                         (0, 255, 0), 2)
            cv2.putText(frame, f"{cls} {conf:.2f}", 
                       (pts[0], pts[1]-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imshow("CCTV YOLO", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
```

## Clases Detectables

1. **Personas** — count de personas en zona
2. **Vehículos** — coches, motos, camiones
3. **Tráfico** — densidad vehicular
4. **Objetos abandonados** — detección de objetos estáticos

## Integración con Mastermind

- Complementa `computer-vision` pipelines para vigilancia
- Útil para `traffic-digital-twin` — datos de cámaras reales
- Reemplaza detección manual con YOLO pre-entrenado
- Ideal para `satellite-traffic-detection` — misma lógica, otra fuente

## Pitfalls

- **Cámara fija:** Modelos entrenados con cámara fija pueden no generalizar
- **Iluminación:** Noche/lluvia afectan precisión
- **Resolución:** CCTV de baja resolución reduce accuracy
- **Performance:** YOLO completo es pesado — usar nano/small para tiempo real

## Referencias

- [GitHub: SanshruthR/CCTV_YOLO](https://github.com/SanshruthR/CCTV_YOLO)

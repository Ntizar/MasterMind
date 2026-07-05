---
name: streetview-3d-cities-dataset
version: "1.0.0"
description: "Dataset de Street View Image, Pose y 3D Cities para computer vision. Inspirado en amir32002/3D_Street_View (⭐509). Datos para 3D reconstruction, pose estimation y city understanding."
tags: [streetview, 3d, dataset, computer-vision, city, pose-estimation]
---

# Dataset 3D Street View

## Resumen

Dataset de imágenes Street View con pose (posición + orientación) y modelos 3D de ciudades. Usado para "Generic 3D Representation via Pose-Conditioned Joint Image-Text Learning". Permite 3D reconstruction, pose estimation y city understanding.

## Cuándo usar

- 3D reconstruction de escenas urbanas
- Pose estimation de cámara desde imagen
- Entrenamiento de modelos de city understanding
- Visualización 3D de calles con datos reales

## Estructura del dataset

```
3D_Street_View/
├── images/          # Imágenes Street View (panorámicas)
├── poses/           # Pose de cámara (x, y, z, qx, qy, qz, qw)
├── depth/           # Mapas de profundidad
├── text/            # Descripciones de texto de la escena
├── 3d_models/       # Modelos 3D de ciudades (mesh, point cloud)
└── metadata.json    # Metadata: ciudad, GPS, timestamp
```

## Patrón de uso

```python
import json
import numpy as np
from PIL import Image

# Cargar dataset
metadata = json.load(open('3D_Street_View/metadata.json'))

# Pose estimation: predecir pose desde imagen
def load_sample(idx):
    entry = metadata[idx]
    image = Image.open(f"images/{entry['image_id']}.jpg")
    pose = np.array(entry['pose'])  # [x, y, z, qx, qy, qz, qw]
    depth = np.load(f"depth/{entry['image_id']}.npy")
    return image, pose, depth

# 3D reconstruction desde múltiples vistas
def reconstruct_3d(samples):
    points = []
    for img, pose, depth in samples:
        # Back-project depth to 3D
        h, w = depth.shape
        fx = fy = 500  # focal length
        cx, cy = w/2, h/2
        
        for y in range(0, h, 10):
            for x in range(0, w, 10):
                z = depth[y, x]
                if z <= 0: continue
                x3d = (x - cx) * z / fx
                y3d = (y - cy) * z / fy
                # Transform to world coordinates using pose
                point = np.array([x3d, y3d, z])
                point = apply_pose(point, pose)
                points.append(point)
    
    return np.array(points)
```

## Pitfalls

- **Pose format:** Quaternion (qx, qy, qz, qw) o Euler angles. Verificar formato del dataset.
- **Depth units:** Verificar si depth está en metros o normalizado.
- **Panoramic images:** Las imágenes panorámicas necesitan equirectangular projection handling.
- **Scale:** Los modelos 3D pueden estar en diferentes escalas. Normalizar.
- **License:** Verificar licencia del dataset antes de usar en producción.

## Referencias

- 3D_Street_View: https://github.com/amir32002/3D_Street_View
- Paper: "Generic 3D Representation via Pose-Conditioned Joint Image-Text Learning"

---

**Hecho con ❤️ por David Antizar**

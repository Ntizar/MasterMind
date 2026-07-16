---
name: r3-reconstruction
description: R^3 — reconstrucción 3D vía regresión relativa. Implementación oficial del paper de CVPR.
---

# R^3 — 3D Reconstruction via Relative Regression

## Qué hace

[R^3](https://github.com/KevinXu02/R3) es la implementación oficial del paper "3D Reconstruction via Relative Regression" (CVPR). Permite reconstruir escenas 3D a partir de imágenes 2D usando regresión relativa de profundidades, más eficiente que métodos SfM tradicionales para certain use cases.

## Instalación

```bash
git clone https://github.com/KevinXu02/R3.git
cd R3
pip install -r requirements.txt

# Descargar pre-trained models
bash download_models.sh
```

## Uso básico

```python
from r3 import SceneReconstructor

# Reconstruir escena desde imágenes
reconstructor = SceneReconstructor(
    model_path='pretrained/r3.pth',
    device='cuda'
)

# Entrada: lista de imágenes con poses conocidas o estimadas
images = ['img1.jpg', 'img2.jpg', 'img3.jpg']
poses = [...]  # Camera poses (optional, R^3 puede inferirlas)

# Ejecutar reconstrucción
result = reconstructor.reconstruct(images, poses)

# Guardar result
result.save_mesh('output.ply')
result.save_depth('depth_map.png')
```

```bash
# CLI
r3 reconstruct --images ./scene/ --output output.ply \
  --model pretrained/r3.pth --device cuda
```

## Integración con pipelines 3D

```python
# R^3 → Three.js/WebGL para visualización web
import trimesh

# R^3 output →PLY
mesh = trimesh.load('output.ply')

# Convertir a glTF para WebGL
mesh.export('scene.gltf')
# Luego cargar en Three.js con GLTFLoader
```

## Pitfalls

- Requiere GPU CUDA para rendimiento práctico
- Los resultados dependen de la calidad y cobertura de las imágenes de entrada
- No es un reemplazo completo de SfM tradicional — mejor para escenas con superposición significativa
- El modelo pre-entrenado está optimizado para escenas urbanas/exteriores

## Referencias

- Paper: "3D Reconstruction via Relative Regression" (CVPR)
- Repo: https://github.com/KevinXu02/R3
- Relacionado: `depth-anything-3`, `colmap-view`, `threejs-3d-maps`, `monolith-terrain`
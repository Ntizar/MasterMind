---
name: depth-anything-3
description: Depth Anything V3 — estimación de profundidad de estado del arte, zero-shot, para cualquier imagen/video.
category: computer-vision
---

# Depth Anything V3 — Estimación de Profundidad SOTA

## Qué es

Depth Anything V3 de ByteDance es un modelo de estimación de profundidad que ofrece:
- **Zero-shot** — funciona en cualquier imagen sin fine-tuning
- **SOTA accuracy** — estado del arte en estimación de profundidad
- **Multi-escala** — predice profundidad a diferentes resoluciones
- **Rápido** — inference en tiempo real con GPU

## Instalación

```bash
git clone https://github.com/ByteDance-Seed/Depth-Anything-3.git
cd Depth-Anything-3
pip install -e .

# Descargar checkpoint
# https://huggingface.co/depth-anything/Depth-Anything-V3
```

## Uso básico

```python
from depth_anything_v3.dpt import DepthAnythingV3

# Cargar modelo
model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
    'vitb': {'encoder': 'vitb', 'features': 128, 'out_channels': [96, 192, 384, 768]},
    'vitl': {'encoder': 'vitl', 'features': 256, 'out_channels': [256, 512, 1024, 1024]},
}

encoder = 'vitl'  # vits, vitb, or vitl
model = DepthAnythingV3(**model_configs[encoder])
model.load_state_dict(torch.load(f'depth_anything_v3_{encoder}.pth'))
model.eval()

# Predecir profundidad
depth = model.predict(image)
```

## Casos de uso para David

- **Mapas 3D** — generar altura/depth para visualizaciones geoespaciales
- **Satélite** — estimar profundidad de terreno desde imágenes
- **Three.js** — texturas de profundidad para escenas 3D
- **Autoguardrails** — validación de profundidad para navegación

## Pitfalls

- Modelo grande (~2GB para vitl)
- Requiere GPU para inference rápida
- Las imágenes de satélite pueden tener artefactos
- No es modelo geométrico — la profundidad es relativa, no métrica

## Referencias

- Repo: `github.com/ByteDance-Seed/Depth-Anything-3` (5K⭐)
- HuggingFace: `https://huggingface.co/depth-anything`

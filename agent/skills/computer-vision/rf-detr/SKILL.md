---
name: rf-detr
version: "1.0.0"
description: "RF-DETR — Real-Time SOTA object detection, instance segmentation y keypoint detection de Roboflow. Backbone DINOv2, 7 modelos (N→2XL). SOTA en COCO y RF100-VL con latencia <7ms para detección en T4. Apache 2.0."
tags: [computer-vision, object-detection, instance-segmentation, keypoint-detection, transformer, det, dino, real-time, roboflow, sota]
---

# RF-DETR — Real-Time SOTA Object Detection

## Resumen

RF-DETR es un architecture transformer en tiempo real para **detección de objetos, segmentación de instancias y detección de keypoints** de Roboflow. Usa DINOv2 (Vision Transformer) como backbone y ofrece SOTA en COCO y RF100-VL con latencias increíbles (<7ms en T4).

## Modelos disponibles

| Tamaño | COCO AP<sub>50</sub> | Latencia (ms) | Parámetros | Resolución | Licencia |
|--------|---------------------|---------------|------------|------------|----------|
| RF-DETR-N | 67.6 | 2.3 | 30.5M | 384×384 | Apache 2.0 |
| RF-DETR-S | 72.1 | 3.5 | 32.1M | 512×512 | Apache 2.0 |
| RF-DETR-M | 73.6 | 4.4 | 33.7M | 576×576 | Apache 2.0 |
| RF-DETR-L | 75.1 | 6.8 | 33.9M | 704×704 | Apache 2.0 |
| RF-DETR-XL | 77.4 | 11.5 | 126.4M | 700×700 | PML 1.0 |
| RF-DETR-2XL | 78.5 | 17.2 | 126.9M | 880×880 | PML 1.0 |

Modelos de segmentación (RF-DETR-Seg-N a 2XL): COCO AP<sub>50:95</sub> 40.3–49.9, de 3.4ms a 21.8ms.
Keypoints (preview): COCO AP<sub>50:95</sub> 71.8 a 9.7ms — supera a YOLO26-pose-X (71.0).

## Instalación

```bash
pip install rfdetr
```

Dependencias: PyTorch >=2.2, torchvision >=0.17, transformers >=5.1, supervision >=0.29, numpy, pydantic.

## Uso básico — Detección

```python
import supervision as sv
from rfdetr import RFDETRMedium

model = RFDETRMedium()
detections = model.predict("image.jpg", threshold=0.5)

# Visualización con supervision
from rfdetr.assets.coco_classes import COCO_CLASSES
labels = [COCO_CLASSES[cid] for cid in detections.class_id]

annotated = sv.BoxAnnotator().annotate(sv.Image(image), detections)
annotated = sv.LabelAnnotator().annotate(annotated, detections, labels)
```

Modelos: `RFDETRNano`, `RFDETRSmall`, `RFDETRMedium`, `RFDETRLarge`, `RFDETRXLarge`.

## Finetuning

```python
# LoRA fine-tuning (opcional, requiere pip install rfdetr[lora])
# PyTorch Lightning training (requiere pip install rfdetr[train])
```

Soporta LoRA en backbone, Albumentations para augmentations, export a ONNX/TensorRT/TFLite.

## Comparativa clave vs YOLO

RF-DETR-L supera a YOLO26-X en detección (56.5 vs 56.9 AP50:95) con similar latencia (6.8 vs 9.6ms) pero solo 33.9M params vs 56.9M. En segmentación la diferencia es mayor: RF-DETR-Seg-L 47.1 AP50:95 vs YOLO26-X-Seg 46.8.

## Integración con Mastermind

- Visor de imágenes con detección de objetos en tiempo real
- Pipeline de CV para proyectos geoespaciales (NAIP, Sentinel)
- Detección de objetos en drone/Satellite imagery
- Combinar con `vision/clip-multimodal` o `vision/onnx-webgpu-inference`
- Para export a navegador: ONNX → WebGPU via `vision/onnx-webgpu-inference`

## Referencias

- Repo: `roboflow/rf-detr`
- Docs: https://github.com/roboflow/rf-detr
- Paper: arXiv 2511.09554
- HuggingFace Space: SkalskiP/RF-DETR
- Complemento: `roboflow/supervision` para visualización y post-procesamiento

---
name: fast-alpr
version: "1.0.0"
description: "FastALPR — framework rápido de reconocimiento de matrículas (ALPR/ANPR) con ONNX y OCR"
---

# FastALPR — Automatic License Plate Recognition

## Descripción

Sistema de reconocimiento automático de matrículas (ALPR/ANPR) de alto rendimiento y personalizable. Modelos ONNX rápidos por defecto, con fast-plate-ocr para OCR y open-image-models para detección de placas.

## Por qué importa para David

- **ALPR/ANPR**: Útil para análisis de tráfico y movilidad en proyectos de transporte
- **ONNX runtime**: Modelo ligero, rápido y portable
- **Customizable**: Se pueden swapear los modelos por propios
- **Real-time**: Procesamiento en tiempo real de streams de video

## Arquitectura

```
Video Stream (CCTV, dashcam, etc.)
    ↓
Plate Detection (open-image-models)
    ↓
OCR (fast-plate-ocr)
    ↓
License Plate Recognition
    ↓
Structured output (JSON)
```

Stack: Python, ONNX Runtime, PyTorch, OpenCV

## Instalación

```bash
pip install fast-alpr
# o
pip install fast-plate-ocr  # para OCR standalone
```

## Uso básico

```python
from fast_alpr import ALPR

alpr = ALPR()
results = alpr.process_image("image.jpg")
# results = [{'plate': 'ABC1234', 'confidence': 0.95, 'bbox': [...]}, ...]
```

## Integración con proyectos de David

- **Traffic monitoring**: Integrar en proyectos de monitorización de tráfico
- **Movement analysis**: Combinar con datos de movilidad y transporte
- **NAP DGT**: Patrón de análisis de imágenes de tráfico

## Pitfalls

- Requiere GPU para performance en tiempo real (ONNX puede ir en CPU pero más lento)
- Precisión depende de calidad de imagen y condiciones de iluminación
- Modelo entrenado principalmente con placas europeas/españolas
- No es un producto enterprise → puede necesitar tuning para casos edge

## Referencias

- GitHub: https://github.com/ankandrew/fast-alpr
- Docs: https://ankandrew.github.io/fast-alpr/
- Hugging Face Space: https://huggingface.co/spaces/ankandrew/fast-alpr
- OCR: https://github.com/ankandrew/fast-plate-ocr

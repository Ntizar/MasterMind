---
name: fast-alpr
description: "Usa a reconocer matrículas con FastALPR (ONNX)."
version: "2.0.0"
tags: [alpr, matricula, onnx, opencv, reconocimiento, vehiculos, python]
related_skills: [fast-alpr, cctv-yolo, roboflow-supervision]
---

# FastALPR — reconocimiento rápido de matrículas

> ⚠️ Corrección 2026-09-05 (auditoría): el método es `predict(...)` (no `process_image`), y `pip install fast-alpr` sin el extra no instala el runtime ONNX.

**Repo:** `https://github.com/ebitbooster/fast-alpr` (Python, ~1.6K⭐).

## When to Use

- Cuando pidas **reconocer matrículas** (ALPR) de forma rápida y en local usando ONNX + OpenCV.

## Uso (API real)

```bash
pip install fast-alpr            # + extra para runtime ONNX (ver README)
```

```python
import fast_alpr
result = fast_alpr.predict(image_path_or_array)   # método predict (no process_image)
```

## Pitfalls

- Método: **`predict`**, no `process_image`.
- El paquete base puede no traer el runtime ONNX — instalar el extra documentado en el README.

## Verificación

- `fast_alpr.predict(img)` y comprobar que devuelve la placa del vehículo.

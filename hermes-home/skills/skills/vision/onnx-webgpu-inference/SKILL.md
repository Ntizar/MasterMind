---
name: onnx-webgpu-inference
description: Ejecutar modelos YOLO ONNX en el navegador con WebGPU (20-40+ fps) o WASM fallback (5-15 fps). Deteccion de personas y vehiculos en tiempo real desde camara web. Derivado de YoloConteo.
version: "1.0.0"
tags: [onnx, webgpu, yolo, deteccion, navegador]
---

# ONNX WebGPU Inference - Patron de Deteccion en Navegador

## Descripcion

Patron para ejecutar modelos de deteccion de objetos YOLO ONNX directamente en el navegador usando WebGPU (GPU local) o WASM como fallback. Sin servidor, sin instalacion.

## Origen

Derivado del repositorio [YoloConteo](https://github.com/Ntizar/YoloConteo).

## Pipeline

```
Camara -> YOLOv8n (ONNX/WebGPU) -> Tracker IoU -> Contador bidireccional -> Resultados en pantalla
```

## Rendimiento

| Backend | FPS esperados | Requisito |
|---------|--------------|-----------|
| **WebGPU** | 20-40+ fps | Chrome/Edge 113+ |
| **WASM** (fallback) | 5-15 fps | Cualquier navegador moderno |

En movil se optimiza automaticamente saltando frames de inferencia para mantener fluidez.

## Estructura del Proyecto

```
YoloConteo/
  web/                    # App web — despliega esta carpeta
    index.html            # Interfaz (Ntizar Design System)
    detector.js           # YOLOv8n inferencia ONNX (WebGPU/WASM)
    tracker.js            # Tracking por IoU
    counter.js            # Conteo bidireccional por cruce de linea
    app.js                # Orquestacion: camara, UI, GPS, mapa, CSV
    ntizar.css            # Estilos
    yolov8n.onnx          # Modelo YOLOv8n (~12 MB)
    serve.py              # Servidor local de desarrollo
  export_model.py         # Exporta yolov8n.pt -> web/yolov8n.onnx
```

## Objetos Detectados

| Objeto | Emoji |
|--------|-------|
| Personas | 👤 |
| Bicicletas | 🚲 |
| Coches | 🚗 |
| Motos | 🏍️ |
| Autobuses | 🚌 |
| Camiones | 🚛 |

## Despliegue

La carpeta `web/` es completamente autocontenida (HTML + JS + CSS + modelo ONNX). Sirve como sitio estatico en cualquier hosting:

- **Vercel** — conecta el repo, directorio de publicacion `web/`, sin build command
- **Netlify** — mismo proceso que Vercel
- **GitHub Pages** — `git subtree push --prefix web origin gh-pages`

> HTTPS es obligatorio en produccion para que funcionen la camara y el GPS.

## Conteo Bidireccional

- Se define una linea virtual en la imagen
- Cada objeto detectado se trackea por IoU (Intersection over Union)
- Se cuenta cada cruce en ambas direcciones
- Se pueden exportar los datos a CSV y geolocalizar con GPS

## Implementacion en Hermes

Para replicar este patron:

1. Exportar modelo YOLO a ONNX (`export_model.py`)
2. Cargar modelo ONNX con ONNX Runtime Web
3. Detectar WebGPU, fallback a WASM
4. Implementar tracker por IoU para seguimiento de objetos
5. Definir linea de conteo interactiva
6. Optimizar saltando frames en movil

## Pitfalls

- **HTTPS obligatorio** — la camara y GPS requieren contexto seguro
- **WebGPU solo Chrome/Edge 113+** — WASM como fallback universal
- **Modelo grande** — yolov8n.onnx ~12 MB, descargar una vez y cachear
- **Rendimiento movil** — saltar frames de inferencia automaticamente
- **Licencia AGPL-3.0** — YOLOv8 de Ultralytics usa AGPL-3.0

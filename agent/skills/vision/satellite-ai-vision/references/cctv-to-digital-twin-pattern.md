# Patrón CCTV → Digital Twin

## Concepto
Convertir vídeo CCTV existente en un digital twin 3D funcional sin necesidad de sensores IoT, GPS en vehículos ni infraestructura costosa.

## Pipeline
1. **Entrada:** Vídeo CCTV mp4 + coordenadas GPS de la cámara (Google Maps)
2. **Detección:** YOLO detecta y trackea vehículos en 2D (bounding boxes)
3. **Calibración:** Camera intrinsics + extrinsics + homografía para mapeo planar
4. **Proyección:** Mapeo de los 2D bounding boxes al espacio 3D georreferenciado
5. **Visualización:** Integración sobre imagen satelital + GUI 3D (PyQt5)

## Hardware requerido
- **Cámaras CCTV existentes** (las que ya hay instaladas)
- **Computadora** para procesamiento (no necesita GPU dedicada para prototipos)
- **Sin sensores IoT**, sin GPS en vehículos, sin cámaras especiales

## Aplicaciones GeoAsset
- **Flotas municipales:** cámaras de tráfico → datos en tiempo real de vehículos
- **Monitorización:** conteo de vehículos, velocidad estimada, direcciones
- **Digital Twin:** visualizar el tráfico de la ciudad sobre el modelo 3D
- **Simulación:** plataforma de predicción basada en datos reales

## Referencia
- **Repo:** duy-phamduc68/TrafficLab-3D (311⭐)
- **Autor:** Yuk (yuk068)
- **URL:** https://github.com/duy-phamduc68/TrafficLab-3D
- **Estado:** PoC experimental, monolítico, refactorización en curso

---
name: airsim-simulation
description: Simulador 3D open-source de Microsoft para drones y robots — simulación urbana, visión por computador, navegación autónoma.
version: "1.0.0"
tags: [simulation, 3D, drone, robot, Microsoft, urban, CV]
---

# AirSim — Simulador 3D de Drones y Robots

## Resumen

Simulador 3D open-source de Microsoft para drones y robots — simulación urbana, visión por computador, navegación autónoma. 18k⭐.

## Repo de referencia

- **GitHub:** `github.com/microsoft/AirSim`
- **Lenguaje:** C++/Python
- **Licencia:** Apache 2.0
- **Motor:** Unreal Engine

## Instalación

```bash
# Descargar desde GitHub
git clone https://github.com/microsoft/AirSim.git
cd AirSim
./setup.sh  # Linux
# o descargar binarios pre-compilados
```

## Uso Básico

```python
import airsim

# Conectar al simulador
client = airsim.MultirotorClient()
client.confirmConnection()

# Volar drone
client.enableApiControl(True)
client.armDisarm(True)

# Movimiento
client.moveByVelocityAsync(1, 0, -1, 2).join()  # 1m/s adelante, 1m/s arriba, 2s

# Capturar imágenes
images = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.Scene),
    airsim.ImageRequest("1", airsim.ImageType.DepthVis)
])[0]

# Guardar imagen
with open("frame.png", "wb") as f:
    f.write(images.image_data_uint8)
```

## Patrones Clave

1. **Simulación urbana:** Entornos de ciudad realistas para probar algoritmos
2. **Visión por computador:** Cámaras simuladas para training de CV models
3. **Lidar simulado:** Sensores LiDAR virtuales para SLAM
4. **Multi-robot:** Simular múltiples drones/robots simultáneamente
5. **Python API:** Control completo desde Python

## Integración con Mastermind

- Útil para simulación de tráfico y transporte
- Complementa `microsoft/AirSim` para datos de entrenamiento de CV
- Ideal para testing de algoritmos de navegación antes de deploy real
- Puede generar datos sintéticos para `geodeep` training

## Pitfalls

- **Unreal Engine:** Requiere UE4/UE5 instalado (pesado)
- **Hardware:** Necesita GPU decente para renderizado en tiempo real
- **Complejidad:** Curva de aprendizaje alta para configurar entornos
- **Plataforma:** Principalmente Windows/Linux, no macOS nativo

## Referencias

- [GitHub: microsoft/AirSim](https://github.com/microsoft/AirSim)
- [Docs](https://microsoft.github.io/AirSim)

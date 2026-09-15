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

## Comparativa de alternativas: CARLA (UE5)

CARLA (`carla-simulator/carla`, ~14.400 ⭐, MIT + assets CC-BY, consultado 2026-09-15) es el simulador de conducción autónoma de referencia frente a AirSim (Microsoft, UE4, drones/robots, sin desarrollo activo).

- Rama por defecto **`ue5-dev`** (Unreal Engine 5.5); existe `ue4-dev` (UE 4.26) con diferencias significativas.
- Sistemas soportados: **Ubuntu 22.04/24.04 o Windows 11** (no arranca en Ubuntu 20.04 ni Windows 10 o inferior).
- Hardware recomendado: i7/i9 gen 9-11 o Ryzen 7/9, **+32 GB RAM** y RTX 3070/3080/3090/4090 con 16 GB+ de VRAM → **inviable en portátil**, dato clave antes de plantear despliegue local.
- Build: `./CarlaSetup.sh --interactive` (Linux; `--python-root=PATH`, modo desatendido con `GIT_LOCAL_CREDENTIALS`) o `CarlaSetup.bat` (Windows). Requiere vincular la cuenta de GitHub a Epic Games para el fork privado de UE 5.5.
- Reconstrucción: `cmake -G Ninja -S . -B Build --toolchain=$PWD/CMake/Toolchain.cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_ROS2=ON` → `cmake --build Build` → `carla-python-api-install` / `launch`.
- Ecosistema: `scenario_runner`, `ros-bridge`, `driving-benchmarks` y el leaderboard `leaderboard.carla.org`.

**Cuándo usar cada uno:** AirSim para drones/robots y setups ligeros; CARLA UE5 para conducción urbana, ROS2 y assets abiertos (con el coste de hardware descrito).

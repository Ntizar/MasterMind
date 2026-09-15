---
name: inertial-navigation-inslib
description: "Navegación inercial en C: fusión IMU+GNSS con QA DO-178."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [imu, gnss, kalman, navegacion, embedded, ferrocarril, qa, do-178]
    related_skills: [simsat, rail-lidar-qa-mvp, pk-rail-geocoding]
---

# INSLIB — navegación inercial en C

Librería C11 **sin dependencias ni heap** para fusionar IMU + GNSS + barómetro + magnetómetro con filtros de Kalman de raíz cuadrada, más herramientas Python de post-proceso con GUI. Pensada para embedded/bare-metal.

## When to Use (cuándo usarlo)

- Trayectorias con **GNSS degradado o mudo** (túneles, ferrocarril, interior): navegación inercial con aiding.
- Post-proceso de un dataset IMU/GNSS a KML o PDF de gráficas.
- **Patrón de QA certificable** reutilizable (cobertura MC/DC, trazabilidad de requisitos) para MVPs ferroviarios.

## Núcleo técnico

- Filtros **UDU/Bierman-Thornton** (raíz cuadrada, numéricamente robustos), compensación y **estimación del retardo GNSS** (100-200 ms típicos de receptor).
- **World Magnetic Model embebido** para declinación; modo `AHRS_MODE_ARS` de 5 estados **sin magnetómetro**.
- Formato de datos simple: un CSV por sensor con `t_us` (microsegundos) como primera columna — IMU: `gyr_frd_x/y/z` (rad/s) y `acc_frd_x/y/z` (m/s²) — más un `config.yaml` por dataset (modo de aiding, ruido de sensores, lever arms, canales activos). Ejemplos: `config_basic.yaml`, `config_local_inertial.yaml`.

## Uso verificado

```bash
sh python/setup_venv.sh          # crea venv y hace 'make pylib'
. env.sh                          # activa el entorno
python3 python/inspostgui.py datasets/fog          # GUI de post-proceso

python3 python/replay.py datasets/fog --plot --plot-out /tmp/plots.pdf
python3 python/replay.py datasets/fog --kml salida.kml
python3 python/replay.py <dataset> --estimate-gnss-delay   # mide el lag real por correlación cruzada
```

Tiempo real: `make insrcv` escucha paquetes UDP en el **puerto 29800** (protocolo en `tools/inslib_protocol.md`) y reemite a **PlotJuggler** (JSON UDP `:9870`) y opcionalmente MAVLink (`./build/insrcv --mavlink`, UDP `:14550`).

## Patrón de QA (lo más valioso para proyectos certificables)

- >90 % de cobertura incluyendo **MC/DC**, orientado a **DO-178 DAL-A / ISO 26262 ASIL-D**.
- Trazabilidad de requisitos machine-checkable con `make reqs`; análisis estático con UBSan/ASan.

## Pitfalls

- Los datasets de ejemplo son logs de vuelo (`datasets/fog`): sus escalas de ruido no valen tal cual para ferrocarril — recalibrar `config.yaml`.
- El magnetómetro es opcional pero su ausencia degrada el rumbo: usar `AHRS_MODE_ARS` a conciencia.
- Sin heap ⇒ buffers de tamaño fijo: revisar límites antes de subir frecuencias de muestreo.

## Referencia

- Repo: `jnz/INSLIB` (~482 ⭐, C, consultado 2026-09-15).

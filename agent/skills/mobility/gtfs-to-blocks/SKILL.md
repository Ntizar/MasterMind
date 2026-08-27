---
name: gtfs-to-blocks
description: Convertir GTFS a bloques de transporte — planificación de rutas, frecuencias y turnos.
version: "1.0.0"
tags: [GTFS, transport, planning, blocks, scheduling, mobility]
---

# GTFS to Blocks

## Resumen

Convierte feeds GTFS a bloques de transporte — planificación de rutas y frecuencias. 6⭐.

## Repo de referencia

- **GitHub:** `github.com/BlinkTagInc/gtfs-to-blocks`
- **Lenguaje:** Python
- **Licencia:** MIT
- **Mantenedor:** BlinkTag Inc (empresa de software de transporte)

## Instalación

```bash
git clone https://github.com/BlinkTagInc/gtfs-to-blocks.git
cd gtfs-to-blocks && pip install -r requirements.txt
```

## Uso Básico

```python
from gtfs_to_blocks import GTFSBlocks

# Procesar feed GTFS
blocks = GTFSBlocks("feed_gtfs.zip")

# Generar bloques (turnos de conductores)
result = blocks.generate(
    start_time="05:00:00",
    end_time="01:00:00",
    max_trip_duration=480,  # 8 horas máx
    break_duration=30,  # 30 min de descanso
)

# Visualizar bloques
result.plot("bloques.png")

# Exportar
result.export_csv("bloques_plan.csv")
```

## Funcionalidades

1. **Block generation:** Generar bloques de trabajo a partir de horarios
2. **Constraints:** Duración máxima, descansos, turnos
3. **Optimization:** Minimizar número de bloques
4. **Visualization:** Gráficos de bloques en el tiempo
5. **Export:** CSV, Excel para planificación

## Integración con Mastermind

- Complementa `gtfs-manager` — planificación vs creación
- Útil para `opentripplanner-otp` — datos de operación
- Ideal para `transit-data-pipelines` — pipelines de datos
- Reemplaza planificación manual de turnos

## Pitfalls

- **Proyecto pequeño:** Pocos stars, puede estar abandonado
- **Dependencias:** Requiere Python 3.8+ con pandas
- **Validación:** Los bloques generados pueden no ser realistas
- **Documentación:** Docs limitados

## Referencias

- [GitHub: BlinkTagInc/gtfs-to-blocks](https://github.com/BlinkTagInc/gtfs-to-blocks)

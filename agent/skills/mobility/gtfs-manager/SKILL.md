---
name: gtfs-manager
description: Gestor estático de feeds GTFS — crear, editar y validar feeds de transporte público.
version: "1.0.0"
tags: [GTFS, transport, editor, validator, mobility]
---

# GTFS Manager — Gestor de Feeds GTFS

## Resumen

Gestor estático de feeds GTFS para crear, editar y validar feeds de transporte público. 159⭐.

## Repo de referencia

- **GitHub:** `github.com/WRI-Cities/static-GTFS-manager`
- **Lenguaje:** Python/JavaScript
- **Licencia:** Apache 2.0
- **Mantenedor:** World Resources Institute (WRI)

## Instalación

```bash
git clone https://github.com/WRI-Cities/static-GTFS-manager.git
cd static-GTFS-manager && pip install -r requirements.txt
```

## Uso Básico

```python
# Crear feed GTFS desde cero
from gtfs_manager import GTFSManager

manager = GTFSManager()

# Añadir rutas
manager.add_route(
    route_id="R1",
    agency_id="AG1",
    route_short_name="1",
    route_long_name="Centro → Universidad",
    route_type=3,  # Bus
)

# Añadir paradas
manager.add_stop(
    stop_id="S1",
    stop_name="Plaza Mayor",
    stop_lat=40.4154,
    stop_lon=-3.7074,
)

# Añadir frecuencias
manager.add_frequency(
    route_id="R1",
    start_time="06:00:00",
    end_time="22:00:00",
    headway_secs=300,  # cada 5 minutos
)

# Exportar
manager.export("mi_feed_gtfs.zip")
```

## Funcionalidades

1. **Crear:** Generar feeds GTFS desde cero o templates
2. **Editar:** Modificar rutas, paradas, horarios existentes
3. **Validar:** Verificar compliance con especificación GTFS
4. **Converter:** GTFS ↔ CSV, GTFS ↔ GeoJSON
5. **Visualizar:** Mapa de rutas y paradas

## Integración con Mastermind

- Complementa `gtfs-tidy` — creación vs limpieza
- Útil para `gtfs-to-blocks` — generar feeds para planificación
- Fuente para `opentripplanner-otp` — feeds custom
- Reemplaza edición manual de CSVs de GTFS

## Pitfalls

- **Especificación:** GTFS tiene muchas reglas — validar siempre
- **Zona horaria:** Los horarios usan zona horaria del feed
- **Calidad:** Los feeds generados pueden no ser realistas
- **Mantenimiento:** Proyecto pequeño, actualizar con cuidado

## Referencias

- [GitHub: WRI-Cities/static-GTFS-manager](https://github.com/WRI-Cities/static-GTFS-manager)

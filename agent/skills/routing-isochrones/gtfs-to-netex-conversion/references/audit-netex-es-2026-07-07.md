# Casos reales de auditoría de proyectos NeTEx-ES

## Auditoría GTFS-Converter (2026-07-07)

### Contexto
Proyecto NeTEx-ES: convertidor GTFS→NeTEx para España. 2.832 líneas, 101 KB, cero dependencias, 39 tests definidos.

### Bugs críticos descubiertos
1. `_get_publisher_code()` en `netex_writer.py` usa `stop_id` como publisher code → IDs como `ES:StopPlace:ATOH:ATOH` (repetido)
2. `test_netex_writer.py` falta `import pytest` → 0 tests pasan
3. `total_time` en `cli.py` usa variable del bloque anterior → tiempo total siempre es solo el de escritura

### Hallazgos clave
- **Cero dependencias ≠ cero bugs**: Un proyecto que solo usa stdlib puede tener bugs lógicos graves
- **LineGeometries huérfanas**: Se generan pero no se referencian desde VehicleJourneys
- **Conversión sample OK**: 17 paradas, 6 líneas, 10 viajes → 52.886 chars XML en 0.01s
- **Cobertura NeTEx**: 80% — faltan AdminAreas, Network, GroupOfLines, PlatformElements

### Métricas de calidad
- Estado: 7/10 (funcional pero necesita pulido)
- Potencial: 9.5/10 (cubre 80% de necesidades reales)
- Prioridad 1: Fijar 3 bugs + validación XSD + tests integración
- Prioridad 2: frequencies.txt, levels.txt, AdminAreas, CI/CD

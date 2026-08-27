# Disk Space Warning — GTFSSpain

**Fecha de detección:** 2026-06-28

**Estado:** 94% disco usado, solo 1.3 GB libres sobre 20 GB.

El directorio `GTFSSpain/data/` ocupa 379 MB. Con la infraestructura del sistema (Mastermind, TimeIneco, esios-dashboard, etc.) el disco está muy justo.

## Recomendaciones

1. **Limpiar ZIPs antiguos** — si hay datasets que no se usan, mover a almacenamiento externo.
2. **Comprimir ZIPs** — algunos GTFS ZIPs podrían comprimirse mejor (ej: Xunta Galicia 118 MB podría reducirse).
3. **Ampliar disco** — 20 GB es insuficiente para el sistema + datos GTFS.
4. **Mover data/ a volumen externo** si hay opción de montaje.

## Monitoreo

```bash
du -sh /root/workspace/GTFSSpain/data/
df -h /root
```

Si `df -h /` muestra >90% usado, ejecutar limpieza urgente.

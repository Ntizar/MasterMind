# Targets de Autopistas Españolas para DRISH-ES

## Sites predefinidos en el código

| ID | Nombre | Bbox (min_lat, min_lon, max_lat, max_lon) | Tipo |
|---|---|---|---|
| m30 | M-30 Madrid (Anillo Interior) | 40.420, -3.720, 40.470, -3.640 | high_volume |
| a1_norte | A-1 Madrid–Burgos (Entrada Norte) | 40.460, -3.710, 40.540, -3.680 | high_volume |
| a2 | A-2 Madrid–Zaragoza (Corredor NE) | 40.430, -3.660, 40.500, -3.560 | high_volume |
| a4 | A-4 Madrid–Sevilla (Corredor Sur) | 40.340, -3.730, 40.420, -3.680 | standard |
| a5 | A-5 Madrid–Badajoz (Corredor SW) | 40.380, -3.780, 40.440, -3.710 | standard |
| ap7_bcn | AP-7 Barcelona (Mediterráneo) | 41.340, 2.100, 41.420, 2.180 | high_volume |
| a7_val | A-7 Valencia (Corredor Mediterráneo) | 39.460, -0.400, 39.520, -0.320 | standard |
| a6 | A-6 Madrid–A Coruña (Corredor NW) | 40.420, -3.780, 40.500, -3.860 | high_volume |

## Zonas adicionales recomendadas

### Autopistas principales
- **A-1**: Madrid→Burgos→Bilbao (corredor industrial norte)
- **A-2**: Madrid→Zaragoza→Barcelona (eje mediterráneo)
- **A-4**: Madrid→Córdoba→Sevilla (corredor andaluz)
- **AP-7**: Valencia→Alicante→Murcia→Almería (costa mediterránea)
- **A-62**: Valladolid→Burgos (eje meseta norte)

### Corredores portuarios
- Acceso al Puerto de Barcelona (ZAL)
- Acceso al Puerto de Valencia
- Acceso al Puerto de Bilbao
- AP-9: Corredor gallego (Vigo→A Coruña)

### Zonas industriales
- Corredor del Henares (Madrid→Guadalajara)
- Corredor del Ebro (Zaragoza)
- Polo Logístico de Madrid (Barajas→Alcalá)

## Notas técnicas

- Sentinel-2 resolución: 10m/píxel → solo detecta vehículos grandes (camiones ~18m)
- Revisita: cada 5 días → análisis de tendencias, no real-time
- Mejor rendimiento en asfalto oscuro y condiciones despejadas
- Las autopistas españolas tienen buen contraste (asfalto oscuro, carriles amplios)

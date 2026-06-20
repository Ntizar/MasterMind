# Verificación empírica de IDs ESIOS — 2026-05-28

## Metodología

Se consultó la API ESIOS para 10 indicadores con la fecha `2026-05-27`, usando `time_trunc=hour` de 00:00 a 23:59 (UTC+2). Se registró el primer valor raw (h0) y el conteo de valores no-nulos.

## Resultados

| Nombre | ID | Raw (h0) | Non-null/24 | Conversión correcta | Valor convertido |
|---|---|---|---|---|---|
| PVPC | 1001 | 168.2 | 120/120 | DIRECT (×1) | 168.2 €/MWh |
| Demanda real | 1293 | 314,675 | 24/24 | /10 | 31,467.5 MW |
| **Solar medida** | **10205** | **SIN DATOS** | **0/0** | **—** | **—** |
| **Gen real Solar** | **10206** | **5,921** | **24/24** | **/10** | **592.1 MW** |
| Gen real renovable | 10351 | 165,818 | 24/24 | /10 | 16,581.8 MW |
| Gen real no renovable | 10352 | 140,622 | 24/24 | /10 | 14,062.2 MW |
| CO₂ ratio | 10355 | 1.427 | 24/24 | DIRECT (×1) | 1.43 tCO₂/MWh |
| Gen libre CO₂ | 10006 | 226,490 | 24/24 | /10 | 22,649 MW |
| Interconexión Francia | 10207 | -813.52 | 24/24 | **DIRECT (×1)** | -813.52 MW |
| Interconexión Portugal | 10208 | -294.07 | 24/24 | **DIRECT (×1)** | -294.07 MW |

## Hallazgos clave

### 1. ID 10205 (Solar medida) NO funciona
Confirmado: devuelve 0 resultados. Usar **10206** (Gen real Solar) en su lugar.

### 2. Interconexiones 10207-10208 son MW DIRECTOS
Raw -813.52 → -813.52 MW. **NO dividir entre 10 ni 1000.** Valor negativo = importación, positivo = exportación.

### 3. CO₂ ratio 10355 es directo
Raw 1.427 → 1.43 tCO₂/MWh. Es un ratio, no un valor acumulado. No dividir.

### 4. Demanda 1293 requiere /10
Raw 314,675 → 31,467.5 MW. La API devuelve en unidades de 10 MW.

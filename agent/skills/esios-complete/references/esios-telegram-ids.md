# Mapeo de IDs correctos para scripts ESIOS

## Script esios-telegram.js — IDs y unidades

| Variable | ID | Nombre ESIOS | Unidad | Conversión |
|---|---|---|---|---|
| precios | 1001 | Término de facturación energía PVPC | €/MWh | Ninguna |
| demanda | 1293 | Demanda real | MW | /10 |
| genRenReal | 10351 | Gen T.Real renovable | MW | /10 |
| genNoRenReal | 10352 | Gen T.Real no renovable | MW | /10 |
| co2Libre | 10006 | Generación libre CO2 | MW | /10 |
| co2Ratio | 10355 | CO2 asociado gen real | tCO2/MWh | Ninguna |
| demandaPrev | 2052 | Demanda prevista nacional | MW | /10 |
| eolicaPrev | 1777 | Previsión D+1 eólica | MW | Ninguna |
| solarPrev | 1779 | Previsión D+1 fotovoltaica | MW | Ninguna |
| renovablePrev | 10358 | Previsión D+1 renovable total | MW | Ninguna |
| interFR | 10207 | Saldo interconexión Francia | MW | DIRECTO |
| interPT | 10208 | Saldo interconexión Portugal | MW | DIRECTO |

## IDs que ya NO existen o son incorrectos

| ID incorrecto | Por qué está mal | ID correcto |
|---|---|---|
| 460 | previsionDemanda — no existe en índice | 2052 |
| 541 | previsionEolica — no existe en índice | 1777 |
| 14 | solar FV PBF programada (no D+1) | 1779 |
| 10350 | demanda medida gen SNP (no previsión) | 10358 |

## IDs de interconexión completa

| ID | Nombre | Unidad |
|---|---|---|
| 10207 | Saldo interconexión Francia (telemedida) | MW (DIRECTO) |
| 10208 | Saldo interconexión Portugal (telemedida) | MW (DIRECTO) |
| 10209 | Saldo interconexión Marruecos (telemedida) | MW (DIRECTO) |
| 10044-10049 | Gen medida Saldo (por tecnología) | MWh (/1000) |

> ⚠️ **Distinción clave**: IDs 10207-10209 son **telemedida** (MW directo). IDs 10044-10049 son **medida por tecnología** (MWh, requieren /1000). No confundirlos.

## Regla de verificación

NUNCA confiar en una tabla de IDs sin verificarla contra `convertEsiosValue()` (fuente de verdad). Si hay discrepancia, la tabla es incorrecta.

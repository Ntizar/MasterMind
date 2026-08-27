# Verificación de unidades ESIOS — Procedimiento

## Problema recurrente

Los indicadores ESIOS/REE tienen unidades inconsistentes:
- Algunos vienen en MW directo
- Algunos en MWh/periodo (necesitan /1000)
- Algunos en decenas (históricamente /10, pero YA NO)
- time_trunc=hour SUMA valores en lugar de promediar

Si un valor parece demasiado grande (ej. 313k MW para demanda española), probablemente las unidades están mal convertidas.

## Procedimiento de verificación

1. **Duda de unidades → consultar `convertEsiosValue()`** en `/root/workspace/esios-dashboard/src/shared/esios-units.js` — es la fuente de verdad
2. **Cross-check con REE**: comparar contra datos de REE en https://www.ree.es/es/datos-generacion-electrica (valores reales conocidos)
3. **Si el valor es absurdo**:
   - ¿Es 10× demasiado alto? → Busca IDs que deberían ser DIRECT_IDS
   - ¿Es 1000× demasiado alto? → Faltó dividir entre 1000 (PBF)
   - ¿Es suma en lugar de promedio? → time_trunc=hour está causando SUMA

## Lista de IDs por categoría

### DIRECTOS (sin conversión)
PVPC (1001), Pool OMIE (600), Demanda (1293), Previsión demanda (2052), Solar (10206), GenRen (10351), GenNoRen (10352), CO2gen (10006), CO2ratio (10355, 10356), InterFR (10207), InterPT (10208), InterMR (10209), Telemedida (2038-2067), Batería (2198, 2199), Potencia disp. (10232), Previsión D+1 (1777-1780, 10358-10359)

### /1000 (MWh/periodo → MW)
PBF programados (IDs 1-462, 623), 10035-10049

### ⚠️ ANTES /10 — YA NO EXISTE
Los IDs que antes estaban en DIV10_IDS (10206, 1293, 2052, 10351, 10352, 10006, 10232, 2198, 2199) son DIRECTOS. Si ves un script que los divide entre 10, está roto.

## Referencias
- `/root/workspace/esios-dashboard/src/shared/esios-units.js` — fuente de verdad

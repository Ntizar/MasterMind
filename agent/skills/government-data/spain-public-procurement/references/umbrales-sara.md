# Umbrales SARA y matching PLACSP ↔ TED

Extraído del README real de `BquantFinance/licitaciones-espana` (consultado 2026-09-15). Fuente primaria para no volver a consultar el repo.

## Umbrales de publicación obligatoria en TED (no son un importe fijo)

Varían por **bienio**, **tipo de contrato** y **tipo de comprador**:

| Bienio | Obras | Servicios (AGE) | Servicios (resto) | Sectores especiales |
|--------|-------|------------------|---------------------|---------------------|
| 2016-2017 | 5.225.000 € | 135.000 € | 209.000 € | 418.000 € |
| 2018-2019 | 5.548.000 € | 144.000 € | 221.000 € | 443.000 € |
| 2020-2021 | 5.350.000 € | 139.000 € | 214.000 € | 428.000 € |
| 2022-2023 | 5.382.000 € | 140.000 € | 215.000 € | 431.000 € |
| 2024-2025 | 5.538.000 € | 143.000 € | 221.000 € | 443.000 € |

## Resultados del cruce

| Métrica | Valor |
|---|---|
| Contratos SARA identificados | 442.835 |
| Validados en TED | 177.892 (40,2 %) |
| Missing | 257.258 |
| Missing de alta confianza | 202.383 |

## Estrategias de matching (secuenciales: cada una actúa solo sobre lo que las anteriores no encontraron)

| # | Estrategia | Matches | % del total |
|---|-----------|---------|-------------|
| E1 | NIF adjudicatario + importe ±10 % + año ±1 | 43.063 | 9,7 % |
| E2 | Nº expediente + importe ±10 % | 7.891 | 1,8 % |
| E3 | NIF del órgano contratante + importe | 77.816 | 17,6 % |
| E4 | Lotes agrupados (suma de importes mismo órgano + año) | 31.365 | 7,1 % |
| E5 | Nombre del órgano normalizado + importe | 17.757 | 4,0 % |

**Hallazgo clave:** E3 (NIF del órgano) es la estrategia más potente. TED registra el NIF del **comprador**; PLACSP, el del **adjudicatario**. Sin cruzar ambos se pierde el 17,6 % de los matches.

## Validación por año (SARA / matches / %)

```
2016   10.948    2.643  24,1%
2017   17.360    6.532  37,6%
2018   32.605   14.720  45,1%
2019   42.951   14.182  33,0%
2020   40.693    9.214  22,6%   <- COVID + baja cobertura TED
2021   47.971    7.472  15,6%
2022   56.649   22.250  39,3%
2023   60.518   31.829  52,6%
2024   59.114   38.216  64,6%   <- máximo
2025   48.276   26.920  55,8%
```

## Contexto de interpretación

- El sector salud es el 17 % de los contratos SARA, con tasa de validación del 42,3 %.
- El 38 % del missing se explica por **patrones de lotes**: un anuncio TED agrupa N adjudicaciones individuales de PLACSP. La cobertura real ajustada por lotes es **~54 %**.
- Los indicadores de calidad siguen el marco **PPDS**, con umbrales LCSP aportados por Jaime Gómez-Obregón y benchmarks PBL de OIRESCON.

## Ficheros del pipeline (nombres reales)

`ted/run_ted_crossvalidation.py` (cross-validation con reglas SARA + matching avanzado, 5 estrategias), `ted/ted_module.py`, `ted/cross-validation_ted_placsp.py`, `ted/diagnostico_missing_ted.py`, `borme/scripts/borme_placsp_match.py`, `calidad/calidad_licitaciones.py`.

Artefactos intermedios citados por el README: `ted/crossval_sara_v2.parquet` (columna `_ted_missing` marca los no publicados).

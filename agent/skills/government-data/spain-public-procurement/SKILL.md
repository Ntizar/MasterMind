---
name: spain-public-procurement
description: "Licitaciones públicas de España: dataset y cruce PLACSP-TED."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [licitaciones, placsp, ted, contratacion, datos-espana, parquet, borme]
    related_skills: [boe-borme-api, government-data-pipelines, catastro-api]
---

# Contratación pública española (PLACSP + TED + BORME)

Dataset y metodología para trabajar con **~44,4 M de registros** de licitaciones públicas españolas (2000-2026, ~2,3 GB) y cruzarlas con el diario europeo TED mediante reglas reproducibles.

## When to Use (cuándo usarlo)

- Analizar **quién gana qué** contratos (organismo, adjudicatario, importe, CCAA).
- Detectar **anomalías** (cruce BORME × PLACSP) o medir competencia por sector.
- Preparar informes/lecturas de mercado antes de licitar (perspectiva de ingeniería/consultoría).

## Cobertura del dataset

PLACSP nacional 8,7 M (2012-2026) · Catalunya 20,6 M · València 8,5 M · Madrid 2,56 M + Ayto. 119 K · Euskadi 704 K · Galicia 1,7 M · Andalucía 857 K · Asturias 375 K · **TED España 591 K**.

## Pitfall crítico: Git LFS

Los `.parquet`/`.csv` están en **Git LFS**: un `git clone` normal devuelve punteros de ~130 bytes. Hacer `git lfs pull` o descargar los ZIP de GitHub Releases (`nacional.zip` 1,34 GB, `borme.zip` 750 MB).

## Matching PLACSP ↔ TED (secuencial)

1. **E1** NIF adjudicatario + importe ±10 % + año ±1 → 43.063 casos.
2. **E2** nº de expediente + importe ±10 % → 7.891.
3. **E3** NIF del órgano contratante + importe → 77.816.
4. **E4** lotes agrupados (suma de importes).

Resultado publicado: 442.835 contratos SARA identificados, solo **177.892 (40,2 %)** localizados en TED → 202.383 *missing* de alta confianza.

## Umbrales SARA (no son un importe fijo)

Por bienio, tipo de contrato y tipo de comprador. Ejemplo 2024-2025: obras **5.538.000 €**, servicios AGE 143.000 €, servicios resto 221.000 €, sectores especiales 443.000 € (tabla completa 2016-2025 en el README).

## Código real

- `ted/ted_module.py` (v6.0): descarga CSV bulk de `data.europa.eu` (2006-2023) y usa la **API v3** `POST https://api.ted.europa.eu/v3/notices/search` con body `query`/`page`/`limit` y `scope="ALL"` (sintaxis eForms, sin corchetes).
- Pipeline: `ted/run_ted_crossvalidation.py`, `ted/cross-validation_ted_placsp.py`, `ted/diagnostico_missing_ted.py`, `scripts/ccaa_*.py`, `borme/scripts/borme_placsp_match.py` (5 flags de anomalía), `calidad/calidad_licitaciones.py` (20 indicadores).
- Requisitos: `pip install pandas pyarrow requests beautifulsoup4 pdfplumber python-dateutil`; tests con pytest en `tests/`.

## Cadencia de actualización

PLACSP mensual · TED trimestral (API) y anual (CSV bulk) · Galicia ~8 h de scraper. Revisar licencias de reutilización por portal (están listadas en el README).

## Referencia

- Repo: `BquantFinance/licitaciones-espana` (~218 ⭐, Python, consultado 2026-09-15).
- Complementa a `boe-borme-api` (API oficial) — aquí el valor está en el **dataset ya normalizado + la metodología de cruce**.

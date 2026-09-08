---
name: dna-analysis
description: "Usa al analizar ADN crudo: ascendencia, rasgos, sexo."
version: 1.0.0
author: Mastermind
license: CC BY 4.0
tags: [adn, adn-crudo, genetica, ascendencia, grafanc, myheritage, 23andme, haplotipo]
related_skills: [genealogy-research, genealogia-espanola, browser-local-tools, github-pages-modern-deploy]
---

# Analisis de ADN crudo (MyHeritage / 23andMe / Ancestry)

## Cuando usar
- El usuario sube/comparte un fichero de ADN crudo (`MyHeritage_raw_dna_data.csv`, `.zip`, 23andMe, Ancestry) y quiere sacar ascendencia, rasgos, sexo o "lo que se pueda aprender".
- Construir una herramienta/analizador de ADN (web cliente o script).

## 1. Formato de los datos crudos
- **MyHeritage**: CSV con columnas `RSID,CHROMOSOME,POSITION,RESULT` (puede ir en `.zip`). Cabeceras `##fileformat=MyHeritage`, `##reference=build37`. Genotipo en **hebra forward (+) de GRCh37**. **~585.000 SNP**, autosomas + cromosoma X.
- **23andMe / Ancestry**: `rsid,chromosome,position,genotype` (o `allele1/allele2`). Escribir un parser que detecte columnas por cabecera.
- ⚠️ **Los chips de consumo NO incluyen cromosoma Y ni ADN mitocondrial** en su raw data → **no se pueden calcular haplogrupos (paterno/materno)** con este fichero. Decirlo claro; no intentar calcularlos.
- Para **comparar con familiares (primos)** se necesita una base de datos de ADN de otros individuos (GEDmatch, etc.) — imposible en local con un solo fichero.

## 2. Sexo (determinacion rapida)
- Muestra **varon** si el cromosoma X es casi 100% homocigoto (X hemicigoto): heterocigosidad X < ~10%. **Mujer** si ~50%.
- En el ejemplo: 250/24.045 heterocigotos (1,04%) → hombre. Heterocigosidad autosomica normal ~21%.

## 3. Ascendencia continental — metodo GrafAnc / GRAF-pop (NCBI)
Metodo validado, open-source, model-free: compara genotipos con frecuencias alelicas (AF) de poblaciones de referencia.
- Panel de referencia: **`AncSnpPopAFs.txt.gz`** (282.424 SNP de ascendencia, build 37). Columnas: `chr pos_37 pos_38 rs ref alt` + **26 poblaciones** (UKBBEUR, UKBBAFR, UKBBEAS, Nigeria, Ghana, Zimbabwe, Uganda, Iran, Barbados, China, Philippines, Thailand, Japan, Nepal, Pakistan, Bangladesh, SriLanka, India2, Irish, Finland, Italy, PUR, UKBSAS, UKBMEX, France, Poland).
- **3 vertices (E/F/A)** = UKBBEUR / UKBBAFR / UKBBEAS. **5 ref pops** = EUR, AFR, EAS, Nigeria, Ghana.
- **15 sub-scores** (EA1-4, AF1-3, EU1-3, SA1-2, IC1-3), cada uno = par de poblaciones via `scorePopIdx1/2`. Normalizacion a [-1,1].
- Salida: GD1/GD2/GD3, %EUR/AFR/EAS (coordenadas baricentricas sobre el triangulo E-F-A) y `AncGroupID` (reglas de decision, ver `references/grafanc-ancestry.md`).
- **Validacion clave**: un europeo debe dar GD1/GD2 ≈ vertice europeo (1.4758/1.4370) y %EUR ≈ 98-99%. Ejemplo real validado: GD1=1.4719, GD2=1.4335, EUR 98.98%, grupo 303 (Europa Occidental, al limite con 304 Meridional — tipico iberico).
- **Repos**: `github.com/jimmy-penn/grafanc` (binario Linux + C++), `github.com/ncbi/graf`. El binario es **Linux**; reimplementar en Python/JS (el algoritmo esta completamente especificado en `SampleGenoDist.cpp`, `SampleGenoAncestry.cpp`, `AncestrySnps.cpp`).

## 4. Rasgos geneticos — TRAMPA de hebra/alelo (importante)
⚠️ **No interpretar los genotipos crudos comparandolos directamente con los alelos "de efecto" de la literatura.** Hay dos problemas reales:
1. **Sitios multi-alelicos** (p. ej. rs4988235 lactosa es G/A/C/T; el alelo de persistencia T no aparece como "A" en el genotipo) → interpretacion ambigua.
2. **Convencion de hebra variable por SNP**: el panel/el chip pueden reportar los alelos en la hebra complementaria (p. ej. MTHFR C677T se reporta como A/G en el panel, no C/T). El desfase no es detectable "a ojo".

**Solucion (tecnica reutilizable):** para cada SNP de rasgo, obtener la **base de referencia forward** consultando **Ensembl GRCh37**:
```
GET https://grch37.rest.ensembl.org/sequence/region/human/{chr}:{pos}-{pos}?content-type=application/json   → {"seq":"G"}
GET https://grch37.rest.ensembl.org/variation/human/{rsid}?content-type=application/json   → mapping strand, allele_string
```
Con la base de referencia forward conocida, orientar el genotipo y mapear el alelo de efecto de la literatura. Nunca adivinar la hebra.
- `myvariant.info` y `web_extract` (Firecrawl sin key) fallaron en este entorno; Ensembl grch37 funciono fiable.
- Tabla curada de rasgos con alelos de efecto verificados: `references/trait-snp-panel.md`.

## 5. App cliente de privacidad total (GitHub Pages)
Patron: analizador 100% en el navegador, sin servidor, sin guardar datos de nadie.
- Descomprimir zip con **JSZip** (vendored local), CSV parseable en JS.
- Panel de referencia compacto como asset estatico: preprocesar `AncSnpPopAFs.txt.gz` a un **binario compacto** (`build_reference.py` → `panel.bin.gz`), descomprimir en JS con `DecompressionStream('gzip')`.
- Cargar el panel una vez, cachear.

## 6. Trampas tecnicas (de la implementacion JS)
- **Cuantizacion de AFs**: guardar AFs como **uint16** (÷65535), no uint8. Con uint8, valores que se redondean a exactamente 0 o 1 hacen `log(0)=-Inf` → NaN en el calculo de distancias esperadas. uint16 (clamped a [1,65534]) evita los bordes y mantiene precision.
- **Cabecera binaria**: layout `magic(6) + version(1) + n_snps(4)` = 11 bytes; registros desde el byte 11. No sobreescribir los primeros bytes con el conteo.
- **Map con claves numericas vs string**: si el panel indexa por `rs` numerico y el genotipo por string, usar `Number(rs)` al buscar.
- **Orden de argumentos en la asignacion de grupo**: pasar el % de **Asia Oriental** (aPct) como primer argumento a `assignGroup`, no el europeo — causa un grupo equivocado.

## Archivos de apoyo
- `references/grafanc-ancestry.md` — algoritmo completo (transformacion geometrica, baricentrico, scorePopIdx, reglas AncGroupID), formato del panel, como obtenerlo, y la reimplementacion Python validada.
- `references/trait-snp-panel.md` — tabla curada de rasgos con alelos de efecto (hebra forward GRCh37) y nivel de confianza.
- `scripts/build_reference.py` — convierte el panel gz a binario compacto para la web.

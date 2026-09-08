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

> Consolidado 2026-09-08: fusiona las versiones duplicadas `dna-raw-analysis` (data-science) y
> `dna-ancestry-analysis` (genetics); sus referencias específicas se movieron a este skill.

## Cuando usar
- El usuario sube/comparte un fichero de ADN crudo (`MyHeritage_raw_dna_data.csv`, `.zip`, 23andMe, Ancestry) y quiere sacar ascendencia, rasgos, sexo o "lo que se pueda aprender".
- Construir una herramienta/analizador de ADN (web 100% cliente o script).

## 1. Formato de los datos crudos
- **MyHeritage**: CSV con columnas `RSID,CHROMOSOME,POSITION,RESULT` (puede ir en `.zip`). Cabeceras `##fileformat=MyHeritage`, `##reference=build37`. Genotipo en **hebra forward (+) de GRCh37**. **~585.000 SNP**, autosomas + cromosoma X. **NO incluye cromosoma Y ni mtDNA → NO se pueden calcular haplogrupos (paterno/materno)**. Decirlo claro; no intentar calcularlos.
- **23andMe / Ancestry**: columnas `rsid,chromosome,position,genotype` (o `allele1`/`allele2`). Parser flexible que detecte cabecera por nombres (`rsid`,`chromosome`,`position`,`genotype`/`result`); si no hay cabecera, asumir `rsid,chrom,pos,genotype`. Aceptar delimitador `,` o tab.
- Guardar el **número** del rsid (sin prefijo `rs`); las claves del panel de referencia son numéricas.
- **No es diagnóstico**: los datos de consumo no son para uso médico. Añadir aviso; enmarcar salud/portador como curiosidad (portador ≠ enfermo).

## 2. Sexo (determinacion rapida)
- **Varon** si el cromosoma X es casi 100% homocigoto (X hemicigoto): heterocigosidad X < ~10%. **Mujer** si ~50%. En el ejemplo: 250/24.045 heterocigotos (1,04%) → hombre. Heterocigosidad autosomica normal ~21%.

## 3. Ascendencia continental — metodo GrafAnc / GRAF-pop (NCBI)
Metodo peer-reviewed (Jin et al., HGG Advances 2025), open-source, model-free: compara genotipos con frecuencias alelicas (AF) de poblaciones de referencia y estima mezcla por coordenadas baricentricas sobre el triangulo E-F-A.
- Panel de referencia: **`AncSnpPopAFs.txt.gz`** (~282.424 SNP de ascendencia, build 37). Columnas: `chr pos_37 pos_38 rs ref alt` + **26 poblaciones** (UKBBEUR, UKBBAFR, UKBBEAS, Nigeria, Ghana, Zimbabwe, Uganda, Iran, Barbados, China, Philippines, Thailand, Japan, Nepal, Pakistan, Bangladesh, SriLanka, India2, Irish, Finland, Italy, PUR, UKBSAS, UKBMEX, France, Poland) = columnas 6–31.
- **3 vertices (E/F/A)** = UKBBEUR / UKBBAFR / UKBBEAS. **5 ref pops** para distancias: EUR, AFR, EAS, Nigeria, Ghana.
- **15 sub-scores** (EA1-4, AF1-3, EU1-3, SA1-2, IC1-3), cada uno = par de poblaciones via `scorePopIdx1/2`. Normalizacion a [-1,1].
- Salida: GD1/GD2/GD3, %EUR/AFR/EAS (baricentricas) y `AncGroupID`.
- **Repos**: `github.com/jimmy-penn/grafanc` (binario Linux + C++), `github.com/ncbi/graf`. El binario es **Linux**; reimplementar en Python/JS (algoritmo especificado en `SampleGenoDist.cpp`, `SampleGenoAncestry.cpp`, `AncestrySnps.cpp`).
- Detalle completo (indices, transformacion geometrica, reglas AncGroupID, formato binario): `references/grafanc-ancestry.md` · `references/grafanc-panel-algorithm.md` · `references/grafanc-algorithm.md`.

### Verificar que el resultado es cierto (3 indicadores)
- **Correlacion** genotipos (frecuencia ALT observada 0/0.5/1) vs AFs de referencia. Un europeo da ~0.57 con EUR, mucho menos con AFR (~0.25) y EAS (~0.34).
- **Posicion GD1/GD2** sobre el triangulo: un europeo cae sobre el vertice europeo (1.4758, 1.4370). Ejemplo validado: GD1=1.4719, GD2=1.4335, EUR 98.98%, grupo 303 (Europa Occidental, al limite con 304 Meridional — tipico iberico).
- **Precision** σ = a + b/√n (GD1: a=−0.0001 b=0.83). Con >71.000 SNP, σ≈0.003 → error infimo.

## 4. Rasgos geneticos — TRAMPA de hebra/alelo (importante)
⚠️ **No interpretar los genotipos crudos comparandolos directamente con los alelos "de efecto" de la literatura.** Dos problemas:
1. **Sitios multi-alelicos** (p. ej. rs4988235 lactosa es G/A/C/T; el alelo de persistencia T no aparece como bialelico simple) → interpretacion ambigua.
2. **Convencion de hebra variable por SNP**: el chip puede reportar en la hebra complementaria. El desfase no es detectable "a ojo".

**Solucion (tecnica reutilizable):** para cada SNP de rasgo, obtener la **base de referencia forward** consultando **Ensembl GRCh37**:
```
GET https://grch37.rest.ensembl.org/sequence/region/human/{chr}:{pos}-{pos}?content-type=application/json   → {"seq":"G"}   (OBLIGATORIO el rango pos-pos)
GET https://grch37.rest.ensembl.org/variation/human/{rsid}?content-type=application/json   → mapping strand, allele_string
```
Con la base forward conocida, orientar el genotipo y mapear el alelo de efecto. Nunca adivinar la hebra. Ademas, **confirmar la orientacion con SNPedia** (`bots.snpedia.com/index.php?title=RsXXXX&action=raw`): pagina con `Orientation: plus|minus`, tabla `geno1/geno2/geno3` + resumen fenotipico, y PMIDs. Si SNPedia dice `minus`, el alelo del chip es el complemento (A↔T, C↔G).
- `myvariant.info` y `web_extract` (Firecrawl sin key) fallaron; Ensembl grch37 funciono fiable.
- **SNPedia se bloquea tras ~12 peticiones** (Incapsula/JS challenge) → pausas de 1.5–3s y reintentos, o `web_extract` en lotes de 5.
- Correcciones reales confirmadas: rs4988235 (lactosa) chip `AA` = `T/T` minus = **tolerante**; rs12913832 (ojos) chip `AA` = **marron**, solo `G/G` = azul; rs1229984 (ADH1B) chip `CC` = `G/G` minus = metabolismo tipico.
- Tabla curada de rasgos con alelos de efecto verificados: `references/trait-snp-panel.md`.

### Estudios por gen (3 reales)
Para "3 estudios de cada gen": extraer PMIDs de SNPedia y adjuntar `[autor/año/PMID, qué encontró]` por gen, agrupados en un diccionario `STUDIES` (keyed por rsid). Siempre basarse en SNPedia/PubMed, nunca en memoria. Tabla snpedia corregida por gen: `references/snpedia-genes.md`.

## 5. App cliente de privacidad total (GitHub Pages)
Patron: analizador 100% en el navegador, sin servidor, sin guardar datos de nadie.
- Descomprimir zip con **JSZip** (vendored local), CSV parseable en JS, `DecompressionStream('gzip')` para el panel, `fetch` del panel como asset estatico.
- Panel de referencia compacto como asset: preprocesar a **binario compacto** (`scripts/build_reference.py` → `panel.bin.gz`, ≈16 MB uint16 correcto).
- **Mapa**: Leaflet + OpenStreetMap (free, sin key). Usar `circleMarker` y **zonas/regiones coloreadas** (no solo puntos) + resaltar la zona de la muestra. Poblaciones de referencia como markers. CSS de Leaflet debe cargarse.
- **Nada se sube**: solo se descarga el panel anonimo; el ADN del usuario se procesa en su maquina.
- **GitHub Pages**: `gh repo create <owner>/<name> --public --source . --push` + `gh api repos/<owner>/<repo>/pages -X POST -f source[branch]=master -f source[path]=/`. El build tarda ~1 min.

## 6. Trampas tecnicas (de la implementacion JS)
- **Cuantizacion de AFs**: guardar AFs como **uint16** (÷65535, clamp [1,65534]), NO uint8. uint8 redondea a 0/1 y `log(0)=-Inf` → NaN.
- **Cabecera binaria**: layout `magic(6) + version(1) + n_snps(4)` = 11 bytes; registros desde el byte 11. Escribir el conteo en `buf[7:11]`, no `buf[6:10]` (pisa la version). Registro 63 bytes con uint16 (1+4+4+1+1+52).
- **Map con claves numericas vs string**: usar `Number(rs)` al buscar.
- **Orden de argumentos en la asignacion de grupo**: pasar el % de **Asia Oriental** (aPct) como primer argumento, no el europeo.
- **Node para testear JS de navegador**: `vm.createContext` + `vm.runInContext` (concatenar data.js + app.js); los `const` top-level no se comparten entre scripts vm separados. Proveer stubs de `window/document/L/fetch`.
- **Verificacion visual**: el harness (Browser Use) exige aprobar la depuracion remota de Chrome; si no, validar en Node y desplegar.

## Preferencias de presentacion (David)
- Explicar **en lenguaje humano/natural** ("en cristiano"), no tecnicismos: que es el gen + que significa PARA TI + que hacer.
- **Adjuntar 3 estudios reales por gen** con cita (autor/año/PMID + que encontro).
- Mapa con **zonas/regiones** coloreadas + la zona de la muestra destacada.
- Seccion de **verificacion** (correlacion, posicion en triangulo, σ): la "prueba de que es cierto".

## Archivos de apoyo
- `references/grafanc-ancestry.md` — algoritmo GraAnc completo (transformacion geometrica, baricentrico, scorePopIdx, reglas AncGroupID) + formato del panel + reimplementacion Python validada.
- `references/grafanc-panel-algorithm.md` — detalle del panel (columnas, indices de score) y el formato binario.
- `references/grafanc-algorithm.md` — algoritmo GraAnc + verificacion de hebra (de la version genetics).
- `references/trait-snp-panel.md` — tabla curada de rasgos con alelos de efecto (hebra forward GRCh37) y nivel de confianza.
- `references/snpedia-genes.md` — orientacion (plus/minus) y genotipo→fenotipo corregidos por gen + PMIDs (3 por gen).
- `scripts/build_reference.py` — convierte el panel gz a binario compacto para la web.
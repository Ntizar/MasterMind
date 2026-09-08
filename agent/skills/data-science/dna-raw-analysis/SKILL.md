---
name: dna-raw-analysis
description: "Usa al analizar ADN crudo: ascendencia GrafAnc y rasgos."
version: 1.0.0
author: Mastermind
license: CC BY 4.0
metadata:
  hermes:
    tags: [adn, dna, genética, ascendencia, grafanc, myheritage, privacidad, pages]
    related_skills: [browser-local-tools, genealogy-research, github-pages-modern-deploy]
---

# Análisis de ADN crudo (consumidor)

## When to Use
- Analizar un fichero de ADN crudo (MyHeritage/23andMe/Ancestry) para ascendencia, rasgos o sexo.
- Construir una app web 100% client-side (sin servidor, sin guardar datos) que analice ADN.
- Responder "¿qué se puede aprender de este ADN?" con un estudio fiable.

## Cuándo usar
- Analizar un fichero de ADN crudo de MyHeritage/23andMe/Ancestry (raw data) para ascendencia, rasgos o sexo.
- Construir una app web **100% client-side** (sin servidor, sin guardar datos) que analice ADN.
- Responder "¿qué se puede aprender de este ADN?" con un estudio fiable.

## Formatos de entrada
- **MyHeritage**: `RSID,CHROMOSOME,POSITION,RESULT`, cabecera `##fileformat=MyHeritage`, **build 37, hebra forward (+)**. ~585.000 SNP. **NO incluye cromosoma Y ni mtDNA → NO se pueden calcular haplogrupos.** El genotipo son 2 bases (ej. `GA`), orden no garantizado.
- **23andMe / Ancestry**: columnas `rsid,chromosome,position,genotype` (o `allele1`/`allele2`).
- Parser flexible: detectar cabecera (rsid/chromosome/position) y aceptar delimitador `,` o tab.

## Método de ascendencia: GrafAnc / GRAF-pop (NCBI)
Peer-reviewed (Jin et al., HGG Advances 2025). Compara los genotipos con las **frecuencias alélicas de 26 poblaciones de referencia** (UK Biobank + 1000 Genomas + HGDP) y estima proporciones de mezcla por coordenadas baricéntricas sobre el triángulo **Europeo (E) – Africano (F) – Este-asiático (A)**.
- Panel de referencia: `AncSnpPopAFs.txt.gz`, **282.424 SNP**. Columnas: `chr, pos_37, pos_38, rs, ref, alt`, luego **26 AFs** (UKBBEUR, UKBBAFR, UKBBEAS, Nigeria, Ghana, …, Poland) = columnas 6–31.
- **Vértices**: E=UKBBEUR (idx0), F=UKBBAFR (idx1), A=UKBBEAS (idx2). **5 ref pops** para las distancias: [EUR, AFR, EAS, Nigeria, Ghana].
- **15 scores subcontinental** (EA1–4, AF1–3, EU1–3, SA1–2, IC1–3) con pares de poblaciones definidos por `scorePopIdx1/2`.
- Detalle completo (índices, transformación geométrica, asignación de grupo, formato binario) en `references/grafanc-panel-algorithm.md`.

## Pipeline
1. Parsear CSV → `Map(rs -> {chr,pos,gt})`.
2. Matchear por **rsid numérico** al panel (no por posición; el rsid evita validación de alelo).
3. `countAlt(gt, ref, alt)`: nº de alelos ALT con manejo de hebra complementaria (A↔T, C↔G). Devuelve 0/1/2, −1 si no determinable.
4. Calcular distancias genéticas (log-likelihood por población) + transformación + baricéntricas → GD1/GD2/GD3, Pe/Pf/Pa, AncGroupID.
5. Asignar grupo subcontinental con las reglas `SetGrafAncGroups` (ver references).

## Verificación de que el resultado es cierto
Tres indicadores independientes:
- **Correlación** genotipos (frecuencia ALT observada 0/0.5/1) vs AFs de referencia. Un europeo da ~**0.57 con EUR**, mucho menos con AFR (~0.25) y EAS (~0.34). La media de AF observada coincide con la media EUR.
- **Posición GD1/GD2** sobre el triángulo E-F-A: un europeo cae sobre el vértice europeo (1.4758, 1.4370); el resultado fue (1.4719, 1.4335).
- **Precisión** σ = a + b/√n (tabla del paper; GD1: a=−0.0001 b=0.83). Con >71.000 SNP, σ≈0.003 → error ínfimo.

## Interpretación de rasgos — SIEMPRE consultar SNPedia (orientación + genotipo→fenotipo)
La fuente autorizada para el mapeo genotipo→fenotipo y para los estudios es **SNPedia** (`bots.snpedia.com/index.php?title=RsXXXX&action=raw`). Cada página tiene:
- **Orientation: plus|minus** — la convención de alelos en la que se dan los genotipos.
- La tabla `geno1/geno2/geno3` + el resumen fenotípico (p. ej. `|(C;C)||2.5|lactose intolerant`).
- Muchos **PMIDs** (`{{PMID|NNNNN}}` y `[PMID NNNNN]`) para citar estudios.

**PITFALL CRÍTICO (causó 3 errores reales):** el chip reporta en hebra **forward (+)**; si SNPedia dice **minus**, el alelo del chip es el **complemento** (A↔T, C↔G). NO interpretar el genotipo del chip directo contra el efecto de SNPedia. Correcciones confirmadas en esta sesión:
- **rs4988235 (lactosa):** chip `AA` (forward, ref G→alt A) = `T/T` en minus = **tolerante**, NO intolerante. (Es sitio multi-alélico G/A/C/T; el alelo de persistencia es T.)
- **rs12913832 (ojos):** chip `AA` = **marrón** (~80%); solo `G/G` = azul (~99%).
- **rs1229984 (ADH1B):** chip `CC` = `G/G` minus = **Arg/Arg = metabolismo típico**, NO el rápido His48.
Regla: antes de dar un rasgo, leer la página de SNPedia del SNP, mirar `Orientation`, y mapear el genotipo del chip a esa convención (complementar si minus).

## Estudios por gen (3 reales)
Para responder "3 estudios de cada gen": extraer PMIDs de SNPedia y adjuntar `[autor/año/PMID, qué encontró]` por gen. Agruparlos en un diccionario `STUDIES` (keyed por rsid) y mostrarlos en la app y el informe. **SNPedia se bloquea tras ~12 peticiones** (Incapsula/JS challenge) → añadir pausas de 1.5–3s y reintentos, o usar `web_extract` de la página renderizada en lotes de 5.

## Pitfalls (críticos)
1. **Hebra/alelos ambiguos**: el genotipo de consumidor puede estar en hebra distinta a la convención del efecto alélico. **Anclar con la base de referencia forward (GRCh37)**: `https://grch37.rest.ensembl.org/sequence/region/human/{chr}:{pos}-{pos}?content-type=application/json` → campo `seq`. El endpoint `rest.ensembl.org` (GRCh38) no mapea igual; usar `grch37.rest`. Para rsid multialélico, el `variation/human/{rsid}` da `allele_string`. Y **confirmar la orientación con SNPedia** (ver sección anterior) — la base de referencia por sí sola no basta.
2. **Sitios multi-alélicos**: rs4988235 (lactosa) es G/A/C/T — NO interpretar como bialélico simple; el alelo de persistencia es T.
3. **Cuantización uint8 → NaN**: al empaquetar el panel a binario, usar **uint16** (AF×65535, clamp [1,65534]) — uint8 redondea AFs a 0/1 y `log(0)=-Inf` rompe `vtxExpGenoDists`. Cabecera: magic "DNAANC" (6B) + versión (1B) + n_snps u32 (bytes 7–10) + registros de 63 bytes (chr u8, pos u32, rs u32, ref u8, alt u8, 26×u16). El n_snps va en bytes 7–10, NO 6–10 (eso pisa la versión).
4. **No Y/mtDNA** en MyHeritage raw → imposible haplogrupos; matches con familiares → GEDmatch.
5. **Bug de orden de argumentos** en la asignación de grupo: pasar primero el **% EAS** (aPct), luego % AFR — no el % EUR.
6. **Test del algoritmo sin navegador**: usar Node `vm` con stubs (`window.addEventListener`, `document.querySelector`→mock) y `fetch` que sirve el panel desde disco; cargar `data.js`+`app.js` concatenados (los `const` top-level no se comparten entre scripts vm separados). Render con DOM mock (mock `createElement`/`createElementNS`).
7. **Verificación visual en navegador**: el harness (Browser Use) exige que el usuario apruebe la depuración remota de Chrome (chrome://inspect). Si no está aprobada, NO repetir en bucle — validar en Node y desplegar.

## App client-side (privacidad total)
- Todo en el navegador: **JSZip** para descomprimir el zip, **`DecompressionStream('gzip')`** para el panel, `fetch` del panel como asset estático.
- Empaquetar el panel a binario compacto + gzip (≈9 MB uint8 con bugs, ≈16 MB uint16 correcto) en `data/panel.bin.gz`.
- **Leaflet + OSM** para el mapa geográfico (markers de poblaciones de referencia + punto de la muestra). Usar `circleMarker` (no requiere imágenes de marker). El CSS de Leaflet debe cargarse.
- **Nada se sube**: solo se descarga el panel anónimo; el ADN del usuario se procesa en su máquina.
- GITHUB PAGES: `gh repo create <owner>/<name> --public --source . --push` + `gh api repos/<owner>/<repo>/pages -X POST -f source[branch]=master -f source[path]=/`. El build tarda ~1 min (404 "Site not found" hasta entonces).

## Preferencias de presentación (David)
- Explicar **en lenguaje humano/natural** ("en cristiano"), no tecnicismos: qué es el gen + qué significa PARA TI + qué hacer.
- **Adjuntar 3 estudios reales por gen** con cita (autor/año/PMID + qué encontró) — siempre basarse en fuentes (SNPedia/PubMed), nunca en memoria.
- Mapa con **zonas/regiones** coloreadas (no solo puntos) + la zona de la muestra destacada; el círculo solo no sorprende.
- El estudio debe ser "digno de lo mejor": verificación (correlación, posición en triángulo, σ), informes regenerados con valores reales.

## Referencias
- `references/grafanc-panel-algorithm.md` — detalle del panel (columnas, índices de score), el algoritmo GrafAnc (vtxExpGenoDists, transformación, baricéntricas, reglas de grupo) y el formato binario del panel.
- `references/snpedia-genes.md` — orientación (plus/minus) y genotipo→fenotipo corregidos por gen, + PMIDs reales (3 por gen) para citar estudios.

---
name: dna-ancestry-analysis
description: Use al analizar ADN crudo (ascendencia, rasgos y sexo).
version: 1.0.0
author: Mastermind
license: CC BY 4.0
tags: [adn, genetica, ascendencia, grafanc, myheritage, haplogrupos, rasgos, navegador]
related_skills: [genealogy-research, browser-local-tools, github-pages-modern-deploy]
---

# Análisis de ADN crudo de consumo (ascendencia + rasgos)

## Cuándo usar
- El usuario entrega un fichero de ADN crudo (MyHeritage `.zip`/`.csv`, 23andMe, Ancestry) y quiere ascendencia, rasgos, sexo o haplogrupos.
- Construir una app/tool que analice ADN crudo (sobre todo 100% en el navegador, privacidad).

## Formatos de datos crudos
- **MyHeritage** (`MyHeritage_raw_dna_data.csv`): columnas `RSID, CHROMOSOME, POSITION, RESULT`. Cabecera con `##fileformat=MyHeritage`, `##reference=build37`, "reported on the forward (+) strand with respect to build 37". Genotipo en `RESULT` (ej. `GG`, `GA`).
- **23andMe / Ancestry**: columnas `rsid, chromosome, position, genotype` (o `allele1/allele2`). Parser flexible: detectar cabecera por nombres (`rsid`, `chromosome`, `position`, `genotype`/`result`); si no hay cabecera, asumir `rsid,chrom,pos,genotype`.
- Sinónimos rsid: guardar siempre el **número** (sin prefijo `rs`); las claves del panel de referencia son numéricas.

## Datos CLAVE que el usuario debe saber
- **Haplogrupos paterno (Y) y materno (mtDNA) NO se pueden calcular** con un fichero de consumo estándar: MyHeritage/23andMe/Ancestry **no incluyen** SNP de cromosoma Y ni mitocondria en el raw data. No intentarlo ni prometerlo.
- **Sexo**: del cromosoma X. X casi 100% homocigoto (heterocigosidad <~10%) → hombre (hemicigoto); alta heterocigosidad → mujer.
- **No es diagnóstico.** Los datos de consumo no son para uso médico. Añadir aviso claro y enmarcar salud/portador como curiosidad (portador ≠ enfermo).

## Ascendencia: método GrafAnc / GRAF-pop (NCBI)
Reimplementado en Python y JS (Jin et al., HGG Advances 2025). Algoritmo en `references/grafanc-algorithm.md`:
- Panel de referencia `AncSnpPopAFs.txt.gz` (~282.424 SNP, 26 poblaciones: UKBBEUR, UKBBAFR, UKBBEAS, Nigeria, Ghana, Zimbabwe, Uganda, Iran, Barbados, China, Philippines, Thailand, Japan, Nepal, Pakistan, Bangladesh, SriLanka, India2, Irish, Finland, Italy, PUR, UKBSAS, UKBMEX, France, Poland).
- Tres vértices E/F/A = UKBBEUR / UKBBAFR / UKBBEAS. Distancia genética = media negativa del log-likelihood del genotipo dada la AF de la población. Coordenadas baricéntricas sobre el triángulo E-F-A → % EUR/AFR/EAS, GD1/GD2/GD3, sub-pop scores, AncGroupID.
- Validación: el punto GD1/GD2 de un europeo cae sobre el vértice europeo (1.4758/1.4370). Correlación de genotipos con la referencia EUR > AFR/EAS. Fiabilidad σ = a + b/√n (a,b del paper).

## Interpretación de rasgos: verificar la HEBRA (crítico)
Los alelos reportados por el chip y los "efecto" de la literatura NO siempre coinciden en hebra. **Nunca interpretar a ciegas.**
1. Tomar chr:pos(build 37) del fichero y pedir la base de referencia forward a **Ensembl GRCh37**:
   `https://grch37.rest.ensembl.org/sequence/region/human/{chr}:{pos}-{pos}?content-type=application/json` → `.seq`. **Obligatorio el formato rango `pos-pos`** (sin el guion el endpoint interpreta mal y da 400).
2. Comparar el genotipo (forward) con ref; el no-ref es el alt. Definir el alelo efecto en la convención forward.
3. Cuidado con sitios **multi-alélicos** (ej. rs4988235 = G/A/C/T en GRCh37): la interpretación clásica (alelo T = persistencia lactasa) no mapea limpio a un genotipo A/A → enmarcar como "probable, no concluyente".
4. Para conteo de alelos alt en el algoritmo: considerar hebra complementaria (A↔T, C↔G) como fallback.

## Construir una app de análisis (mejor versión)
- **Privacidad total**: 100% cliente, sin servidor ni almacenamiento. Solo descargar un panel anónimo de referencia. Procesar zip con JSZip, descomprimir con `DecompressionStream('gzip')`, parsear CSV en JS.
- **Panel compacto**: convertir el `.gz` de referencia a binario (`magic+version+n+registros`) para cargarlo rápido y pequeño.
- **Mapa geográfico**: Leaflet + OpenStreetMap (free, sin key). Usar **zonas/regiones** (círculos coloreados + etiqueta) y resaltar la zona de la muestra. Poblaciones de referencia como marcadores.
- **Sección de verificación** (el usuario la pide): correlación de genotipos vs poblaciones de referencia, posición GD en el triángulo E-F-A, σ de fiabilidad, nº de SNP. Es la "prueba de que es cierto".
- **Lenguaje humano** (preferencia fuerte del usuario): cada rasgo = qué es el gen (en cristiano) + qué significa PARA TI + consejo práctico. La ascendencia con un resumen "En cristiano". Evitar tecnicismos sin explicar.
- **GitHub Pages** para el deploy (rama master, raíz `/`); el asset del panel se sirve estático (~16 MB) y se cachea.

## Pitfalls (aprendidos)
- **Binario del panel**: cabecera = magic(6)+version(1)+n(4)=11 bytes, registros empiezan en byte 11. Escribir el conteo en `buf[7:11]`, no `buf[6:10]` (sobrescribe la versión). Registro de 63 bytes si AFs son uint16 (1+4+4+1+1+52).
- **Cuantizar AFs a uint8 → exactos 0/1 → `log(0)=-Inf` → NaN** en el cálculo. Usar **uint16** (÷65535) y clampear a [1,65534].
- **JS `Map` claves**: si el panel guarda `rs` numérico y el genotipo del usuario viene como string, hacer `rsToIdx.get(Number(rs))`.
- **assignGroup (AncGroupID)**: el primer argumento es el % **este-asiático**, NO el europeo. Pasar `(aPct, fPct, gd1, gd2, gd3, subPopScores)`.
- **Node para testear JS de navegador**: usar `vm.createContext` + `vm.runInContext` (concatenando data.js + app.js) — `eval` en modo estricto no expone las funciones. Proveer stubs de `window/document/L/fetch`; `fetch` que sirva el panel desde disco.
- **web_extract/WebSearch** a veces falla (Firecrawl sin key 403); para APIs REST usar `curl` o `urllib` con `User-Agent`.
- La API `myvariant.info` devolvió vacío; **Ensembl grch37** sí funcionó.

## Referencias
- `references/grafanc-algorithm.md` — algoritmo GrafAnc completo (constantes, índices de población, transformación, asignación de grupo) y verificación de hebra.

# GrafAnc / GRAF-pop — algoritmo y panel (NCBI)

Método: *Jin et al., HGG Advances 2025* (https://github.com/jimmy-penn/grafanc). Model-free: compara genotipos con AF de poblaciones de referencia.

## Panel de referencia
`cpp/data/AncSnpPopAFs.txt.gz` (282.424 SNP, build 37), columnas:
`chr pos_37 pos_38 rs ref alt` + 26 poblaciones (índices 0-25 sobre columnas 6-31):
`UKBBEUR UKBBAFR UKBBEAS Nigeria Ghana Zimbabwe Uganda Iran Barbados China Philippines Thailand Japan Nepal Pakistan Bangladesh SriLanka India2 Irish Finland Italy PUR UKBSAS UKBMEX France Poland`

Constantes (headers):
- `numAllAncSnps=282424`, `numRefPops=5`, `numVtxPops=3`, `numSubPops=26`, `numSubPopScores=15`, `ancSnpFileOthCols=6`.
- `scorePopIdx1=[9,9,9,9,3,3,6,18,18,24,16,17,23,20,20]`
- `scorePopIdx2=[11,12,10,13,5,4,8,20,19,25,15,14,22,21,7]`
- `subPopGdNormP1=-1`, `subPopGdNormP2=1`. `minAncSnps=100` (10K continental, 50K subcontinental).

## Algoritmo (portado a Python/JS)
1. `vtxPopAfs` = [EUR,AFR,EAS] (cols 6-8); `refPopAfs[5]` = [EUR,AFR,EAS,Nigeria,Ghana].
2. **vtxExpGenoDists[vtx][e/f/a][snp]** (esperado de log-likelihood bajo cada ref-pop, con genotipos dibujados del vértice):
   `eGd = aaPev*pv^2 + bbPev*qv^2 + abPev*2*pv*qv`, donde `pv=vtxPopAfs[vtx]`, `aaPev=ln(pev)*2`, `bbPev=ln(qev)*2`, `abPev=ln(pev)+ln(qev)+ln2`, `pev=refPopAfs[0]` (EUR), etc. Sumado sobre todos los SNP → `vtxPopExpGds[vtx]`.
3. **Por muestra** (solo SNP con genotipo):
   - `popPvalues[pop]` += log-likelihood del genotipo (geno 0 → `ln(qv)*2`, 1 → `ln(pv*qv*2)`, 2 → `ln(pv)*2`); `popMeanPvals[pop]=-sum/refPopSnps[pop]`.
   - `vtxExpPeSums[vtx]` += `vtxExpGenoDists[vtx][0][snp]` (y Pf/Pa).
   - sub-scores: `smpGd[s]`, `nomGdScoreSumP1/P2` con `logp=ln(p2/p1)`, `logq=ln((1-p2)/(1-p1))`; `smpGdScore[s]=-1+2*(raw-n1)/(n2-n1)`.
4. **Transformación geométrica** (SampleGenoDist.cpp): punto `(x=a,y=e,z=f)`; mover F a origen; rotar en z, y, x; mover a `afrPosition=(1.08,1.10,0.00)`.
5. **Baricéntrico**: `det=(y2-y3)*(x1-x3)+(x3-x2)*(y1-y3)`; `eWt`,`fWt`,`aWt=1-eWt-fWt`.
6. `gd1=eWt*g0e.x+fWt*g0f.x+aWt*g0a.x` (g0 = transformación fija de `vtxPopExpGds`); `gd2` con .y; `gd3=sPt.z`.
7. `ePct/fPct/aPct` = pesos >=0 normalizados a 100. `AncGroupID` por reglas (ver SampleGenoAncestry.cpp `SetGrafAncGroups`): Oceania/SouthAsia/Multi/EastAsia/Europe-MENA/Africa, usando ePct(aPct), fPct, gd1, gd3, ic1, eu1, eu2, eu3, sa1, sa2, ea1, ea2, ea4, af1, af2, af3.

## Validación
Un europeo real dio: GD1=1.4719, GD2=1.4335, GD3=-0.0088, EUR 98.98%, AFR 1.01%, EAS 0.01%, AncGroupID=303. El vértice europeo del panel es (1.4758, 1.4370) → cae encima. La media de la frecuencia alélica observada (0.8418) == media EUR (0.8418) → codificación correcta, sin desvío de hebra.

## Codificación de genotipo (alt count)
Contar alelos ALT con manejo de hebra complementaria: A↔T, C↔G. Para cada base del genotipo, si ==alt → alt; si ==ref → ref; si complemento==alt → alt; si complemento==ref → ref; si no → -1 (missing).

## Reimplementar
El binario `grafanc` es Linux. El algoritmo está íntegro en `SampleGenoDist.cpp`, `SampleGenoAncestry.cpp`, `AncestrySnps.cpp`. Portarlo a Python/JS. No hay WSL/g++ en Windows por defecto → no compilar, portar.

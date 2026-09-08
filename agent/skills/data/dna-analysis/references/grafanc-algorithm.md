# Algoritmo GrafAnc / GRAF-pop — detalle de implementación

Fuente: Jin Y, Wang H, Naj AC, Wang L-S, Lee W-P. "GrafAnc: Reliable and Reproducible Inference of Continental and Regional Population Structure." *Human Genetics and Genomics Advances* 7:100530 (2025). Reimplementado en Python y JS.

## Panel de referencia `AncSnpPopAFs.txt.gz` (282.424 SNP)
Columnas (tab separado, 0-based): `0=chr, 1=pos_37, 2=pos_38, 3=rs, 4=ref, 5=alt, 6..31 = 26 AFs`.
Las 26 poblaciones (índice `refSubPopAfs` 0..25, = columna 6+i):
0 UKBBEUR, 1 UKBBAFR, 2 UKBBEAS, 3 Nigeria, 4 Ghana, 5 Zimbabwe, 6 Uganda, 7 Iran, 8 Barbados, 9 China, 10 Philippines, 11 Thailand, 12 Japan, 13 Nepal, 14 Pakistan, 15 Bangladesh, 16 SriLanka, 17 India2, 18 Irish, 19 Finland, 20 Italy, 21 PUR, 22 UKBSAS, 23 UKBMEX, 24 France, 25 Poland.

`refPopAfs[0..4]` (para las 5 distancias GD) = cols 6,7,8,9,10 = EUR, AFR, EAS, Nigeria, Ghana.
`vtxPopAfs[0..2]` (vértices E,F,A) = cols 6,7,8 = EUR, AFR, EAS.

## Constantes
- `numAllAncSnps = 282424`, `numRefPops = 5`, `numVtxPops = 3`, `numSubPops = 26`, `numSubPopScores = 15`.
- `scorePopIdx1 = [9,9,9,9, 3,3,6, 18,18,24, 16,17, 23,20,20]`
- `scorePopIdx2 = [11,12,10,13, 5,4,8, 20,19,25, 15,14, 22,21,7]`
  → EA1..EA4 (China vs Thailand/Japan/Philippines/Nepal), AF1..AF3 (Nigeria vs Zimbabwe/Ghana, Uganda vs Barbados), EU1..EU3 (Irish vs Italy/Finland, France vs Poland), SA1..SA2 (SriLanka vs India2, Bangladesh vs Pakistan), IC1..IC3 (MEX vs SAS, Italy vs PUR, Italy vs Iran).
- Normalización sub-pop: `-1 + 2*(raw-n1)/(n2-n1)`.

## Cálculo (por individuo)
Codificar genotipo como nº de alelos ALT (`geno` 0,1,2; 3=missing). Si el panel ref/alt puede estar en hebra complementaria, contar alt con fallback complementario (A↔T, C↔G).

1. **Distancias a 5 poblaciones de referencia** (`popMeanPvals`): para cada SNP con genotipo, sumar log-likelihood dado la AF de cada población:
   - geno 0 → `log(qv)*2`; geno 1 → `log(pv*qv*2)`; geno 2 → `log(pv)*2`. Luego `popMeanPvals[pop] = -sum/refPopSnps[pop]`.
2. **Genotipos esperados de los vértices** (`vtxExpGenoDists[vtx][ref][snp]`): E[ log-likelihood bajo la ref ] con genotipos del vértice vtx. Sumar → `vtxExpDists[vtx].{e,f,a} = -sum/numGenoSnps`.
3. **Transformar a coordenadas**: `point = (x=a, y=e, z=f)`. Mover F al origen, rotar en z,y,x, volver, mover A a `(1.08,1.10,0)`. (Rotaciones estándar con `atan2` y grados→radianes.)
4. **Baricéntricas** (`eWt,fWt,aWt`) del punto de la muestra en el triángulo E-F-A transformado.
5. **GD1/GD2/GD3**: aplicar los pesos a los vértices **fijos** (`vtxExpGd0`, calculados con los centroides E/F/A del panel completo). `gd3 = sPt.z` (coordenada z de la muestra).
6. **Pe/Pf/Pa**: pesos con negativos a 0 y normalizados a 100.
7. **Sub-pop scores**: con `scorePopIdx` y normalización.
8. **AncGroupID**: reglas anidadas (ver abajo).

## Asignación de grupo (ancGroupId)
Orden de condiciones (usa `aPct`=**este-asiático**, `fPct`=africano, `gd1`, `gd3`, y scores sub-pop `ic1,ic3,ea*,eu*,sa*,af*`):
```
if aPct>50 && fPct>10 && ic1>0.4 && gd3>0.035 -> 700 (Oceania)
elif ic1>0.5 && fPct<15 -> Sur de Asia (401-405)
elif aPct>15 && fPct>15 -> 800 (multi)
elif ic1>-0.3 && aPct>40 -> Este de Asia (501-511)
elif eu1<1.6 && ic2<-0.25 -> Europa/MENA:
    if ic3<3.5-3.1*eu1 -> Europa (301-308, 304=Sur, 303=Oeste)
    else -> MENA (202/203)
elif eu1>1.6 && ic2<0.4 -> 201/202 (N. África / ME2)
elif eu1>2.2 && ic2<1.4 -> 106 (Noreste África)
elif gd1>1.4758 -> Latinoamericano (601-603)
else -> africano (101-108, 601 en el ramo ic1<0.9*gd1-1.36)
```
⚠️ Argumento 1 de la función = % **este-asiático** (NO el europeo).

## Fiabilidad (verificación)
`σ = a + b/√n` por score; para GD1: a=-0.0001 b=0.83; GD2: a=-0.0001 b=0.95; GD3: a=-0.0002 b=1.31.
Con ~71.000 SNP, σ(GD1)≈±0.003. El punto GD1/GD2 de un europeo cae sobre el vértice europeo (1.4758, 1.4370).

## Validación de hebra de un SNP de rasgo
1. Tomar `chr:pos` (build 37) del fichero crudo.
2. GET `https://grch37.rest.ensembl.org/sequence/region/human/{chr}:{pos}-{pos}?content-type=application/json` → `.seq` = base de referencia forward. **Formato rango `pos-pos` obligatorio.**
3. El alelo no-ref = alt. Interpretar el genotipo (forward) contra ese ref/alt.
4. Sitios multi-alélicos (ej. rs4988235 → G/A/C/T) no mapean limpio: enmarcar como "probable, no concluyente".

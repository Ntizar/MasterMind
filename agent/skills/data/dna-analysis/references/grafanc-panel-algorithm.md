# GrafAnc / GRAF-pop — panel y algoritmo (detalle)

Fuente: `github.com/jimmy-penn/grafanc` (Jin et al., HGG Advances 2025). Reimplementado en Python y JS, validado contra la referencia.

## Panel de referencia `AncSnpPopAFs.txt.gz` (282.424 SNP)

Columnas (tab-separated):
```
chr  pos_37  pos_38  rs  ref  alt  UKBBEUR  UKBBAFR  UKBBEAS  Nigeria  Ghana  Zimbabwe  Uganda  Iran  Barbados  China  Philippines  Thailand  Japan  Nepal  Pakistan  Bangladesh  SriLanka  India2  Irish  Finland  Italy  PUR  UKBSAS  UKBMEX  France  Poland
```
Índices (0-based):
- 0–5: chr, pos_37, pos_38, rs, ref, alt
- 6–31: 26 sub-poblaciones (refSubPopAfs[0..25])

Mapeo `refSubPopAfs` (columnas 6–31): 0 UKBBEUR, 1 UKBBAFR, 2 UKBBEAS, 3 Nigeria, 4 Ghana, 5 Zimbabwe, 6 Uganda, 7 Iran, 8 Barbados, 9 China, 10 Philippines, 11 Thailand, 12 Japan, 13 Nepal, 14 Pakistan, 15 Bangladesh, 16 SriLanka, 17 India2, 18 Irish, 19 Finland, 20 Italy, 21 PUR, 22 UKBSAS, 23 UKBMEX, 24 France, 25 Poland.

- `refPopAfs` (5, para distancias): [UKBBEUR, UKBBAFR, UKBBEAS, Nigeria, Ghana] (columnas 6,7,8,9,10).
- `vtxPopAfs` (3 vértices): [UKBBEUR, UKBBAFR, UKBBEAS].

## Índices de los 15 scores subcontinentales (`scorePopIdx1` / `scorePopIdx2`)

```
#        EA1 EA2 EA3 EA4 AF1 AF2 AF3 EU1 EU2 EU3 SA1 SA2 IC1 IC2 IC3
idx1 = [  9,  9,  9,  9,  3,  3,  6, 18, 18, 24, 16, 17, 23, 20, 20]
idx2 = [ 11, 12, 10, 13,  5,  4,  8, 20, 19, 25, 15, 14, 22, 21,  7]
```
Normalización: `score = -1 + 2*(raw - n1)/(n2 - n1)` con `subPopGdNormP1=-1`, `subPopGdNormP2=1`.

## Algoritmo (por individuo)

1. **Código de genotipo** `geno` = nº de alelos ALT (0,1,2), o 3=missing. `countAlt` maneja hebra complementaria.
2. **popPvalues[pop]** (5 refs): suma de log-likelihood `log(qv)*2` (geno 0), `log(pv*qv*2)` (geno 1), `log(pv)*2` (geno 2). Solo si `0<pv<1`.
   `popMeanPvals[pop] = -popPvalues[pop]/n`.
3. **vtxExpGenoDists[vtx][ref][snp]**: valor esperado del log-likelihood de la población-ref bajo la distribución genotípica del vértice `vtx`:
   `eGd = aaPev*pv² + bbPev*qv² + abPev*2pv*qv`, con `pv = vtxPopAfs[vtx]` y `aaPev=log(pev)*2` etc. (pev = EUR AF). Sumado por SNP → `vtxExpPeSums[vtx]`.
4. **vtxExpDists[vtx]** = `(-vtxExpPeSums[vtx]/n, -vtxExpPfSums[vtx]/n, -vtxExpPaSums[vtx]/n)`. `smpDist` = `(popMeanPvals[0], popMeanPvals[1], popMeanPvals[2])` (E,F,A).
5. **Transformación** (`transformAll`): puntos `(x=a, y=e, z=f)`; mover F al origen; rotar z por `atan2(aP.y,aP.x)*-180/π`; rotar y por `atan2(aP.z,aP.x)*180/π`; rotar x por `atan2(eP.y,eP.z)*180/π − 90`; mover atrás; mapear A a (1.08, 1.10, 0).
6. **Baricéntricas**: `eWt, fWt, aWt` del punto de la muestra en el triángulo E-F-A (determinante `(y2-y3)(x1-x3)+(x3-x2)(y1-y3)`).
7. **GD1/GD2/GD3**: `gd1 = eWt*g0e.x + fWt*g0f.x + aWt*g0a.x`, idem y; `gd3 = sPt.z`. `g0` es la transformación fija de los centroides `vtxPopExpGds` (suma sobre todos los SNP del panel).
8. **Pe/Pf/Pa**: pesos baricéntricos con negativos a 0, normalizados a 100.

## Reglas de asignación de grupo (`SetGrafAncGroups`)

Recibe `(aPct=EAS %, fPct=AFR %, gd1, gd2, gd3, subPopScores)`. OJO: el primer argumento es el **% EAS**, no el % EUR (bug común de orden). Reglas (abreviado):
- `aPct>50 && fPct>10 && ic1>0.4 && gd3>0.035` → 700 (Oceania)
- `ic1>0.5 && fPct<15` → Sur de Asia (402/403/404/405/401)
- `aPct>15 && fPct>15` → 800 (multi)
- `ic1>-0.3 && aPct>40` → Este de Asia (501–511)
- `eu1<1.6 && ic2<-0.25` → Europa/MENA: si `ic3<3.5-3.1*eu1` → Europa (308/301/305/307/306/304/302/303); si no → MENA (203/202)
- `eu1>1.6 && ic2<0.4` → 201/202; `eu1>2.2 && ic2<1.4` → 106
- `gd1>1.4758` → Latinoam. (603/602/308)
- else → africano (601/108/104/105/103/107/101/102)

Grupos principales: 100 AFR, 200 MEN, 300 EUR, 400 SAS, 500 EAS, 600 AMR, 700 OCN, 800 MIX. Subcontinental europeo: 304 = Sur de Europa (España/Italia/Portugal), 303 = Oeste (Francia/Alemania/UK). Para un español el resultado suele caer en el límite 303/304.

## Formato binario del panel (para la web client-side)

Cabecera: `magic "DNAANC" (6B) + versión (1B) + n_snps u32 LE (bytes 7–10)` + registros de **63 bytes**:
`chr u8, pos u32, rs u32, ref u8, alt u8, afs[26] u16` (AF×65535, clamp [1,65534]).
- El n_snps va en bytes **7–10**; si se escribe en 6–10 pisa el byte de versión y desalinea el primer registro.
- `uint8` (AF×255) rompe el cálculo: algunos AF se redondean a 0/1 y `log(0)=-Inf` → NaN en `vtxExpGenoDists`. Usar `uint16`.
- Gzip del binario → `data/panel.bin.gz` (~16 MB). En el navegador: `fetch` + `DecompressionStream('gzip')`.
- En JS: `afs` como `Uint16Array(n*26)`, acceso `afs[i*26+j]/65535`.

## Puntos de verificación

- Un europeo: GD1≈1.472, GD2≈1.434 (vértice E=1.4758,1.4370), EUR≈99%, correlación vs EUR ≈0.57, vs AFR ≈0.25, vs EAS ≈0.34.
- σ (fiabilidad) = a + b/√n. GD1: a=-0.0001 b=0.83; GD2: -0.0001/0.95; GD3: -0.0002/1.31.

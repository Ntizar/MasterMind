# Panel de rasgos — alelos de efecto en hebra forward GRCh37

⚠️ Para interpretar: obtener la **base de referencia forward** de cada SNP con Ensembl GRCh37
`GET /sequence/region/human/{chr}:{pos}-{pos}` y orientar el genotipo. No comparar a ojo con la literatura (sitios multi-alélicos y hebra variable). Ejemplos de posiciones (build 37) y referencia forward:

| SNP | Gen | chr:pos37 | ref | efecto (forward) | confianza |
|---|---|---|---|---|---|
| rs4988235 | LCT/MCM6 | 2:136608646 | G | T = persistencia lactasa (sitio **multi-alélico** G/A/C/T; A/A → probable no persistente) | baja-media |
| rs762551 | CYP1A2 | 15:75041917 | C | A = metabolizador rápido (AA/AC/CC) | alta |
| rs12913832 | HERC2 | 15:28365618 | A | A = ojos claros | alta |
| rs4680 | COMT | 22:19951271 | G | A = Met (Val158Met) | alta |
| rs6265 | BDNF | 11:27679916 | C | T = Met (Val66Met) | alta |
| rs9939609 | FTO | 16:53820527 | T | A = riesgo IMC | media-alta |
| rs1229984 | ADH1B | 4:100239319 | T | C = Arg48 (alcohol rápido) | media |
| rs671 | ALDH2 | 12:112241766 | G | A = enrojecimiento (E.Asia); G/G normal | alta |
| rs1801133 | MTHFR | 1:11856378 | G | C677T (complemento); A/G = 677 C/T | media |
| rs1544410 | VDR | 12:48239835 | C | T = BsmI | media |
| rs1042713 | ADRB2 | 5:148206440 | G | Arg16Gly | media |
| rs1045642 | ABCB1 | 7:87138645 | A | C3435T (hebra variable) | baja |
| rs3827760 | EDAR | 2:109513601 | A | V370A → pelo grueso/incisivos pala (típico E.Asia) | baja-media |
| rs713598 | TAS2R38 | 7:141673345 | C | gusto amargo (PTC) | media |
| rs1805008 | MC1R | 16:89986144 | C | T = pelo rojo; C/C = no | alta |
| rs1800414 | SLC45A2 | 15:28197037 | T | E272K (piel) | media |
| rs1426654 | SLC24A5 | 15:48426484 | A | A = piel clara (europea) | media-alta |
| rs12203592 | IRF4 | 6:396321 | C | T = freckles/piel | media |
| rs1799945 | HFE | 6:26091179 | C | G = H63D (portador hemocromatosis; ~25% europeos) | alta (portador) |
| rs7412 | APOE | 19:45412079 | C | e2/e4 (requiere también rs429358, a menudo ausente) | n/a |
| rs3892097 | CYP2D6 | 22:42524947 | C | T = *4 (metabolizador pobre) | media |
| rs4986893 | CYP2C19 | 10:96540410 | G | A = *3 (metabolizador pobre) | media |

## Ejemplo de resultado (David, varón europeo)
Lactosa A/A (probable intolerante), cafeína A/C (intermedio), ojos A/A (claro), COMT Val/Met, BDNF Val/Val, FTO T/A (1 riesgo), ADH1B C/C (alcohol rápido), ALDH2 G/G (sin enrojecimiento), MTHFR A/G (677 CT), SLC24A5 A/A (piel clara), MC1R C/C (sin rojo), HFE C/G (portador H63D). Sin Y/mtDNA → sin haplogrupos.

## Ausentes habituales en chips de consumo
rs1805007 (MC1R rojo), rs1815739 (ACTN3 potencia), rs72921001 (cilantro), rs1800562 (HFE C282Y), rs334 (HbS), rs429358 (APOE), rs4244285 (CYP2C19*2), rs1057910 (CYP2C9*2).

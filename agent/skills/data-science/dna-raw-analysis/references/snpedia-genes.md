# SNPedia: orientación, genotipo→fenotipo y estudios por gen

Fuente: `https://bots.snpedia.com/index.php?title=RsXXXX&action=raw`. El chip (MyHeritage/23andMe/Ancestry) reporta hebra **forward (+)**. Si SNPedia indica **Orientation: minus**, complementar los alelos del chip (A↔T, C↔G).

## Correcciones confirmadas (estaban al revés antes de consultar SNPedia)

| rsid | Gen | Chip (forward) | SNPedia orientación | Lectura correcta |
|---|---|---|---|---|
| rs4988235 | MCM6/LCT | AA | minus (C/T) | T/T → **tolerante** (sitio multi-alélico G/A/C/T; persistencia = T) |
| rs12913832 | HERC2 | AA | plus (A/G) | A/A → **marrón** (~80%); G/G → azul (~99%) |
| rs1229984 | ADH1B | CC | minus (G/A) | G/G → **Arg/Arg = típico** (no rápido); A = His48 (rápido/protector) |
| rs4680 | COMT | GA | plus | A/G → **Val/Met intermedio** |
| rs6265 | BDNF | CC | minus | C/C forward = G/G minus → **Val/Val común** |
| rs762551 | CYP1A2 | AC | plus | A/C → un alelo *1F, metabolismo normal |
| rs9939609 | FTO | TA | plus | A/T → un alelo de riesgo |
| rs671 | ALDH2 | GG | plus | G/G → sin el alelo *2 (no se pone rojo) |

## Estudios reales (PMID) por gen — 3 por gen

- **CYP1A2 (cafeína)**: 10233211 (Sachse 1999), 23167834, 20390257.
- **COMT**: 17008817 (warrior/worrier), 18989660 (paroxetina), 19417742.
- **BDNF**: 19745020 (aprendizaje motor), 20042999 (introversión), 17293537 (Alzheimer).
- **FTO**: 17434869 (Frayling, Science 2007 — original), 17554300, 18159244.
- **ALDH2**: 6582480, 16046871, 19698717.
- **MTHFR**: 10366020, 11742229, 17408099.
- **VDR**: 12436222, 15819500, 18376465.
- **ADRB2**: 10673119, 15878488, 16387853.
- **EDAR**: 16751771, 21900102, 23512934.
- **TAS2R38**: 10978373, 15128849, 17190809.
- **MC1R**: 10861880, 17039839, 20462831.
- **SLC24A5**: 16329642 (Lamason, Science 2005), 16444068, 20398819.
- **IRF4**: 18262051, 20398819, 23512934.
- **HFE**: 8696330, 9242511, 15649156.
- **ABCC11**: 16710291, 16325037, 23512934.
- **CHRNA3**: 19673608, 20380725, 22006067.
- **DRD2**: 8514723, 9352537, 19277520.
- **OPRM1**: 9920815, 12967930, 16877413.
- **F5 (Leiden)**: 7969297 (Bertina, Nature 1994), 8537167, 10504366.
- **F2 (protrombina)**: 8557253 (Poort, Blood 1996), 8903300, 11890560.
- **CYP4F2**: 16672007, 18955005, 19691295.
- **CYP2D6**: 11074920, 19934337, 20140677.
- **CYP2C19**: 10197801, 16672365, 21061824.
- **SLC45A2**: 16444068, 18087688, 17081623.

## Nota
SNPedia se bloquea tras ~12 peticiones seguidas (Incapsula JS challenge, devuelve una página `<script src="/_Incapsula_Resource...">`). Usar pausas de 1.5–3s, reintentos, o `web_extract` de la página renderizada en lotes de 5.

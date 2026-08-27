# Validación del total en presupuestos Presto — Caso Nogal9

## Problema

Al extraer TODAS las líneas de "Capítulo" de un PDF Presto moderno (como GLAM), la suma da un número muy superior al Presupuesto General del documento.

### Caso real: GLAM Nogal9

- **Presupuesto General del documento:** 1.218.453,83 € (página final, línea "PRESUPUESTO_P")
- **Suma de TODAS las líneas de Capítulo extraídas:** 2.042.054,69 €
- **Diferencia:** +823.600 € (+67%)

### Causas

1. **Padres e hijos duplicados:** Presto tiene capítulos padre que incluyen sus hijos.
   - Ej: `SAN.07.01` = 20.316 € incluye `SAN.07.01.01` (3.510 €) + `.02` (7.691 €) + `.03` (1.171 €)
   - Si sumas padre + hijos, duplicas el importe

2. **Complementos de materiales incluidos:**
   - `CA` (Micropilotes = 89.894 €) → incluido en capítulo 03 (Cimentación)
   - `EA` (Acero = 4.229 €) → incluido en capítulo 04 (Estructuras)
   - `EH` (Hormigón armado = 173.007 €) → incluido en capítulo 04 (Estructuras)

3. **Instalaciones dentro de capítulos numéricos:**
   - ELE.03.01-07 → dentro del capítulo 13 (Electricidad = 82.846 €)
   - FON.02.01.01-05 → dentro del capítulo 15 (Fontanería = 48.382 €)
   - TEL.10.01-04 → dentro del capítulo 14 (Telecomunicaciones = 19.413 €)
   - TER.01.01-05 → dentro del capítulo 17 (Instalaciones Térmicas = 124.771 €)
   - VMC.09.01.01-03 + VMC09.02 → dentro del capítulo 18 (Calidad del Aire = 60.048 €)

## Solución encontrada

**Capítulos correctos:** 01-27 + SAN.07.01 = 1.218.453,83 € (exacto)

### Reglas de inclusión

| Grupo | Incluir | Excluir |
|-------|---------|---------|
| Capítulos 01-27 | ✅ Todos | — |
| SAN.07.01 | ✅ (fuera de 01-27) | SAN.07.01.01, .02, .03 |
| SAN.07.02 | ✅ | SAN.07.02.01, .02, .03 |
| SAN.07.03 | ✅ | — |
| ELE.03.01-07 | — (dentro de cap. 13) | — |
| FON.02.01.01-05 | — (dentro de cap. 15) | — |
| FON.02.02 | ✅ (no tiene padre numérico) | — |
| TEL.10.01-04 | — (dentro de cap. 14) | — |
| TER.01.01-05 | — (dentro de cap. 17) | — |
| VMC.09.01.01-03 | — (dentro de cap. 18) | — |
| VMC09.01 | — (dentro de cap. 18) | — |
| VMC09.02 | — (dentro de cap. 18) | — |
| PCI.06.01-04 | — (dentro de cap. 21) | — |
| CA, EA, EH | — (complementos materiales) | — |
| 03.04.01, 03.04.02 | — (dentro de cap. 03) | — |
| 07.2 | — (dentro de cap. 07) | — |
| 25.01, 25.02, 25.03 | — (dentro de cap. 25) | — |

## Verificación

Siempre verificar contra el total del documento (última página):

```
PRESUPUESTO_P  1,00  1.218.453,83 €  1.218.453,83 €
```

La diferencia debe ser < 0,01 €.

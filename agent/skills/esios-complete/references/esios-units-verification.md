# Verificación de unidades API ESIOS — 2026-05-28

## Fuente de verdad

**NUNCA confiar en nombres o suposiciones.** Usar siempre `convertEsiosValue()` del dashboard.

## Reglas verificadas empíricamente

### IDs DIRECTOS (NO dividir)
| ID | Nombre | Raw ejemplo | Resultado |
|---|---|---|---|
| 1001 | PVPC | 152.61 | 152.61 €/MWh |
| 10355 | CO2 Ratio | 0.54 | 0.54 tCO2/MWh |
| 10207 | Inter Francia | -1114 | -1114 MW |
| 10208 | Inter Portugal | -2344 | -2344 MW |
| 1777-1780 | Previsión D+1/H+3 | ~35000 | ~35000 MW |

### IDs /10 (dividir entre 10)
| ID | Nombre | Raw ejemplo | Resultado |
|---|---|---|---|
| 1293 | Demanda real | 398380 | 39838 MW |
| 2052 | Demanda prevista | 425743 | 42574 MW |
| 10351 | Gen renovable | 327715 | 32771 MW |
| 10352 | Gen no renovable | 62493 | 6249 MW |
| 10006 | Gen libre CO2 | 388468 | 38846 MW |
| 10206 | Gen solar real | ~300000 | ~30000 MW |

### IDs /1000 (dividir entre 1000)
| ID | Rango | Nombre |
|---|---|---|
| 1-462 | PBF programados | MWh/periodo |
| 10035-10049 | Gen medida por tecnología | MWh |
| 623 | Llenado hidráulico | MWh |

## Patrón de verificación rápida

```javascript
const data = await fetchIndicator(id, fecha, token);
const sample = data.indicator.values[9]?.value;
// Si sample > 100000 → probablemente /10 (telemedida)
// Si sample 100-10000 → probablemente directo (interconexiones, previsión)
// Si sample 1-100 → probablemente directo (PVPC, CO2 ratio)
// Si sample > 1000 y es PBF → /1000
```

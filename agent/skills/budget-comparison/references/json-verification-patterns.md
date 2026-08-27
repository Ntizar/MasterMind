# Patrones de verificación de JSON — Presupuestos de construcción

**Caso real:** Nogal 9 — 8 JSON derivados con problemas de calidad detectados y corregidos.

## Problema 1: Floating point artifacts

```json
// MAL:
"total": 1218453.8299999998
"total": 921275.5999999999

// BIEN:
"total": 1218453.83
```

**Causa:** Python `sum()` con floats produce precisión de punto flotante.
**Fix:** `round(value, 2)` al escribir CUALQUIER total en JSON.

## Problema 2: Nombres con cantidades embebidas

```json
// MAL:
"nombre": "CIMENTACION 108.327,64 €"
"nombre": "REVESTIMIENTOS Y FALSOS TECHOS 5"
"nombre": "INSTALACION DE ELECTRICIDAD 8"

// BIEN:
"nombre": "CIMENTACION"
```

**Causa:** Parsing regex captura parte del importe junto con el nombre.
**Fix:** Limpiar nombres al generar:
```python
import re
def clean_name(name):
    # Quitar "N.NNN,NN €" al final
    name = re.sub(r'\s+[\d]{1,3}(?:\.[\d]{3})*,[\d]{2}\s*€?\s*$', '', name)
    # Quitar dígitos sueltos al final (artifacts)
    name = re.sub(r'\s+\d{1,2}\s*$', '', name)
    return name.strip()
```

## Problema 3: Mapeo inconsistente de capítulos

GLAM usa `SAN.07.01` para saneamiento, Trevicon usa `02`. Si no se mapea, uno queda en 0.

```json
// comparaciones.json MAL (doble conteo):
{"codigo": "02", "glam": 0, "trevicon": 21023.20}
{"codigo": "SAN.07.01", "glam": 20316.59, "trevicon": 0}

// BIEN (un solo registro):
{"codigo": "SAN.07.01", "glam": 20316.59, "trevicon": 21023.20}
```

**Fix:** Usar las claves de la referencia como canonical y mapear explícitamente:
```python
if cap == 'SAN.07.01':
    trev_val = trev['capitulos'].get('02', {}).get('total', 0)
```

## Problema 4: Sumas que no cuadran

```python
# Verificación obligatoria:
for name, data in [('Ref', ref), ('GLAM', glam), ('Trev', trev)]:
    chapters_sum = sum(ch['total'] for ch in data['capitulos'].values())
    assert abs(chapters_sum - data['total']) < 1.0, f"{name} mismatch"
```

## Problema 5: Referencia incorrecta

Un archivo usaba la referencia vieja de 523.705€ (CYPE antiguo) en vez de la correcta de 1.218.453,83€ (GLAM).

**Regla:** SIEMPRE verificar que la referencia es la más reciente antes de generar comparaciones. La referencia se define en el JSON fuente (`presupuesto_referencia.json`), no se inventa.

## Problema 6: Capítulos con total=0

Parsing del PDF falló para ciertos capítulos (ej: Trevicon 03, 08, 19, 20, 24, 25, 27).

**Fix:** Reconstruir desde el JSON fuente que tiene los totales correctos. El JSON fuente debe ser la única fuente de verdad.

## Patrón de reconstrucción completa

Cuando hay múltiples JSON derivados con problemas:

1. Verificar y limpiar SOLO el JSON fuente
2. Reconstruir todos los derivados programáticamente
3. Verificar sumas en todos
4. Commitear todo junto

```python
# Script de reconstrucción (ejemplo nogal9):
import json

with open('presupuesto_referencia.json') as f:
    src = json.load(f)

# Reconstruir comparacion.json
all_caps = sorted([k for k in src['referencia']['capitulos'] if k.isdigit()], key=int)
all_caps.append('SAN.07.01')

comparacion = []
for cap in all_caps:
    ref_val = src['referencia']['capitulos'][cap]['total']
    glam_val = src['ofertas']['glam']['capitulos'].get(cap, {}).get('total', 0)
    trev_val = src['ofertas']['trevicon']['capitulos'].get(cap if cap != 'SAN.07.01' else '02', {}).get('total', 0)
    comparacion.append({...})

# Verificar
assert abs(sum(c['referencia'] for c in comparacion) - src['referencia']['total']) < 0.01
```

## Archivos típicos en un proyecto de comparación

| Archivo | Propósito | Verificar |
|---------|-----------|-----------|
| `presupuesto_referencia.json` | Fuente de verdad (3 entidades) | Sumas, nombres limpios |
| `comparacion.json` | Array de 27 capítulos con diffs | Sumas Ref/GLAM/Trev |
| `comparacion_final.json` | Objeto con 3 bloques de capítulos | Totales, sin zeros, sin floats |
| `comparaciones.json` | Mismo que comparacion (nombre alternativo) | Sin duplicados, mapeo 02↔SAN |
| `comparacion_triptica.json` | Versión tripartita con detalle | Totales, capítulos completos |
| `glam_presupuesto_final.json` | Capítulos GLAM planos | Nombres limpios, totals correctos |
| `oferta_glam_final.json` | Mismo que glam_presupuesto | Nombres limpios |
| `offer_trevicon.json` | Detalle Trevicon con partidas | Verificar contra PDF original |

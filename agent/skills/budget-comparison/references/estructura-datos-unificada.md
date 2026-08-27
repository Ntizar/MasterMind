# Estructura de datos unificada — Comparador presupuestal

**Caso real:** Nogal 9 (9 Viviendas y Trasteros, Madrid)

## Estructura JSON unificada

Un solo archivo `presupuesto_referencia.json` contiene las 3 fuentes:

```json
{
  "proyecto": "NOGAL 9 - 9 VIVIENDAS Y TRASTEROS",
  "localizacion": "Madrid",
  "referencia": {
    "nombre": "Dmarche (CYPE - Proyecto Base)",
    "tipo": "Presupuesto de Ejecución Material (PEM)",
    "total": 1218453.83,
    "capitulos": {
      "01": { "nombre": "MOVIMIENTO DE TIERRAS", "total": 2041.83 },
      "03": { "nombre": "CIMENTACION", "total": 108327.64 },
      ...
    }
  },
  "ofertas": {
    "glam": {
      "nombre": "GLAM (Constructora)",
      "tipo": "Oferta PEM",
      "total": 1218453.83,
      "capitulos": { ... }
    },
    "trevicon": {
      "nombre": "Trevicon (Constructora)",
      "tipo": "Oferta PEM",
      "total": 1098001.21,
      "capitulos": { ... }
    }
  }
}
```

## Estructura comparaciones.json

Resumen capítulo a capítulo con diffs calculados:

```json
[
  {
    "codigo": "01",
    "nombre": "MOVIMIENTO DE TIERRAS",
    "referencia": 2041.83,
    "glam": 2041.83,
    "trevicon": 1863.37,
    "diff_glam_pct": 0.0,
    "diff_trevicon_pct": -8.7,
    "diff_glam_vs_trevicon_pct": 9.9
  },
  ...
]
```

## Normalización de claves

- CYPE/Dmarche: claves alfanuméricas (`"01"`, `"SAN.07.01"`)
- Presto/GLAM: claves alfanuméricas (`"01"`, `"03"`...)
- Trevicon: claves con prefijo `"Cap-01"`, `"Cap-02"` → normalizar a `"01"`, `"02"`

```python
def normalize_key(key):
    num = re.search(r'(\d+)', key)
    return num.group(1) if num else key
```

## Casos especiales detectados

### GLAM = Referencia
GLAM usa exactamente los mismos importes base que el proyecto CYPE/Dmarche.
Esto es NORMAL: GLAM toma los precios del proyecto como base.
→ El comparador muestra las 3 columnas, el usuario decide.

### Trevicon más barato
Trevicon ofrece 9,9% menos que la referencia.
→ Detectar automáticamente y mostrar en alertas.

### Capítulos sin extraer
Algunos capítulos de Trevicon no tenían total en el nombre del PDF
(03, 08, 19, 20, 24, 25, 27).
→ Usar el `resumen` del JSON que tiene `total_euros` por capítulo.

### Mapeo SAN.07.01 ↔ 02 (CRÍTICO)
GLAM/Dmarche usa `SAN.07.01` para Instalación de Saneamiento. Trevicon usa `02` para el mismo capítulo.
Al generar comparaciones, SIEMPRE mapear explícitamente:
```python
if cap == 'SAN.07.01':
    trev_val = trev['capitulos'].get('02', {}).get('total', 0)
```
Si no se hace, uno queda en 0 y la comparación es incorrecta.
En comparaciones.json, usar UN SOLO registro por capítulo (no duplicar 02 + SAN.07.01).

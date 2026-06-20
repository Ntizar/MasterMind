# Comparador de presupuestos — Flujo de comparacion de ofertas

## Contexto de la sesion (2026-06-17)

Crear un sistema para comparar presupuestos de constructoras contra el presupuesto base de ejecucion material.

## Flujo de trabajo

### Paso 1: Presupuesto base (ya hecho)
- Extraer PDF → JSON con `pdfplumber`
- Estructura: resumen (27 capitulos) + detalle (partidas)
- Guardar en `presupuesto_referencia.json`

### Paso 2: Cuando llegue una oferta de constructora
1. Extraer texto del PDF con pdfplumber (mismo metodo)
2. Parsear capitulos y partidas
3. Comparar con referencia:
   - **Partidas eliminadas:** en referencia pero no en oferta
   - **Partidas añadidas:** en oferta pero no en referencia
   - **Diferencias de importe:** mismo concepto, precio diferente
   - **Variaciones de cantidad:** misma partida, medicion diferente

### Paso 3: Analisis de diferencias
- Calcular % de diferencia por capitulo
- Detectar si la oferta es significativamente menor (posible omision de partidas)
- Alertar si capitulos completos faltan

## Analisis real — Nogal 9 (Trevicon)

### Datos reales
- **Referencia:** 523.705,00 € (PEM CYPE)
- **Oferta Trevicon:** 1.098.001,21 € (+109,7%)
- **Total contrata (IVA 10%):** 1.207.801,33 €

### Patrones detectados
1. **Incremento uniforme ~142%** en capítulos de instalaciones (fontaneria, electricidad, telecomunicaciones, saneamiento, incendios, gestion residuos). Parece recargo estandar (indirectos + generales + beneficio).
2. **Incremento ~109-128%** en capítulos estructurales (albañilería, cimentación, estructuras).
3. **Incremento menor ~16-38%** en acabados (revestimientos, pinturas).

### Interpretacion
Un incremento del ~142% en instalaciones sugiere que la constructora aplica un **multiplicador uniforme** sobre los precios unitarios del PEM base, probablemente para cubrir indirectos, generales y beneficio. Los capítulos estructurales suben menos (%) porque incluyen partidas fijas (hormigón, acero) con precios más estables.

## Herramienta generada

- `comparador.html` — Herramienta interactiva con 4 vistas:
  - Tabla comparativa con filtros y ordenación
  - Gráfico de barras (referencia vs oferta + diferencias)
  - Ranking de capítulos por mayor diferencia
  - Detalle de capítulos

## Estructura del JSON de comparacion

```json
{
  "referencia": {
    "total_euros": 523705.00,
    "capitulos": {
      "Cap-1": { "descripcion": "...", "total_euros": 873.19, "partidas": [...] }
    }
  },
  "oferta": {
    "constructora": "Empresa X",
    "total_euros": 0,
    "capitulos": { ... }
  },
  "comparacion": {
    "diferencia_euros": 0,
    "diferencia_porcentual": 0,
    "capitulos": {
      "Cap-1": {
        "referencia": 873.19,
        "oferta": 800.00,
        "diferencia_euros": -73.19,
        "diferencia_porcentual": -8.38,
        "partidas_nuevas": [...],
        "partidas_eliminadas": [...],
        "partidas_con_diferencia": [...]
      }
    }
  }
}
```

## Reglas de comparacion

- **Umbral de alerta:** si la oferta es < 90% del presupuesto base en un capitulo, alertar
- **Partidas obligatorias:** todos los capitulos del presupuesto base deben aparecer en la oferta
- **Precios unitarios:** comparar si la partida tiene mismo codigo o descripcion similar
- **Totales:** la diferencia global no debe superar ±15% sin justificacion

## ⚠️ Normalizacion de claves

CYPE usa `Cap-1`, `Cap-2`... pero ofertas Presto pueden usar `Cap-01`, `Cap-02`.
**Siempre normalizar:** `offer_key = f"Cap-{cap_num.zfill(2)}"` para matching.

## Referencia: Nogal 9

- Repo: github.com/Ntizar/nogal9
- JSON referencia: presupuesto_referencia.json
- JSON oferta: offer_trevicon.json
- Comparacion: comparacion.json
- Herramienta: comparador.html

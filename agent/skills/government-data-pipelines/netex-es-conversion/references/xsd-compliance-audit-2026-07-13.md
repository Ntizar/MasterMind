# Auditoría de Compatibilidad XSD — NeTEx-ES v3.5.0

> **Fecha:** 2026-07-13
> **XSD oficial:** NeTEx-CEN 1.14 (`NeTEx_publication.xsd`, 622 KB)
> **XML probado:** `examples/complete-example.xml` (2,237 líneas)

## Resultado

**NeTEx-ES NO valida contra el XSD oficial.** 14 categorías de errores, 100+ incidencias totales.

### La estructura de alto nivel SÍ es correcta

```
PublicationDelivery
  └── dataObjects           ← ✅ Correcto según XSD
       └── CompositeFrame
            └── frames
                 ├── ResourceFrame           ← ✅ Existe en XSD (substitutionGroup="CommonFrame")
                 ├── SiteFrame               ← ✅ Existe en XSD (netex_part_1)
                 ├── ServiceFrame             ← ✅ Existe en XSD (netex_part_2)
                 ├── ServiceCalendarFrame     ← ✅ Existe en XSD (netex_framework)
                 ├── TimetableFrame           ← ✅ Existe en XSD (netex_part_2)
                 └── FareFrame               ← ✅ Existe en XSD (netex_part_3)
```

## Las 14 Categorías de Errores

### Fáciles (casing, formato, atributos extra)

| # | Error | Fix |
|---|-------|-----|
| E1 | `<version>` elemento bajo `PublicationDelivery` | El version es un *atributo* (`version="1.0"` en el tag), no un elemento hijo. Eliminar `<version>1.0</version>` |
| E2 | `validBetween` (camelCase) → debe ser `ValidBetween` (PascalCase) | El XSD es estricto con PascalCase en elementos |
| E3 | `daysOfWeek` (camelCase) → debe ser `DaysOfWeek` (PascalCase) | Ídem |
| E9 | `PropertyOfDay` NO debe tener atributos `id` ni `version` | Eliminar atributos, el XSD no los permite |
| E13 | Fechas en formato date (`2025-01-06`) → debe ser dateTime (`2025-01-06T00:00:00Z`) | Añadir hora al formato ISO 8601 |

### Medios (enumeraciones, nombres de elementos)

| # | Error | Fix |
|---|-------|-----|
| E4 | `LineType` usa `metro`, `rail`, `bus`, `tram` | El XSD espera: `local`, `urban`, `longDistance`, `express`, `seasonal`, `replacement`, `flexible`, etc. **Atención:** `LineType` NO es el modo de transporte — es el *tipo de servicio*. El modo de transporte va en `TransportMode` |
| E11 | `<tariffs>` no válido bajo `FareFrame` | El XSD espera `priceGroups`, `fareTables`, `distributionChannels`, etc. en esa posición |
| E12 | `<FareProduct>` no válido como hijo directo | El XSD espera `PreassignedFareProduct`, `SaleDiscountRight`, `ThirdPartyProduct`, etc. |

### Graves (reestructuración de árbol XML)

| # | Error | Impacto |
|---|-------|---------|
| E5 | Elementos dentro de `Line` en orden incorrecto | El XSD es estricto: `TypeOfLineRef` → `TransportMode` → ... NeTEx-ES pone `transportMode` donde el XSD espera otra cosa |
| E6 | `<PostalAddress>` no válido bajo `StopPlace` | El XSD espera `TransportMode`/submodes en esa posición, no dirección postal |
| E7 | `<publishedLineReference>` no válido bajo `JourneyPattern` | Debería ser `LineRef` u otro elemento |
| E8 | `<routes>` no válido bajo `ServiceFrame` | El XSD espera `groupsOfLines`, `destinationDisplays`, `scheduledStopPoints`, etc. |
| E10 | `<operatingPeriods>` no válido bajo `ServiceCalendarFrame` | Elemento en posición incorrecta |
| E14 | Orden incorrecto en múltiples niveles | El XSD es estrictamente secuencial. NeTEx-ES pone elementos en orden "lógico" que no coincide con el orden XSD |

## Contradicción Spec vs Ejemplo

**La sección 2.2 de la spec (regla 1) dice: "NO usar `dataObjects`"**

**Pero:**
- ✅ El XSD oficial SÍ requiere `dataObjects` como contenedor de `CompositeFrame`
- ✅ El ejemplo XML (`complete-example.xml`) SÍ usa `dataObjects` — correctamente
- ❌ La regla de la spec está mal redactada

**Lo que realmente debería decir:** "NO poner entidades directamente bajo `dataObjects` en lugar de dentro de frames" — no prohibir `dataObjects` por completo.

## Procedimiento de Validación con lxml

```python
from lxml import etree

xsd_doc = etree.parse('path/to/NeTEx_publication.xsd')
xsd = etree.XMLSchema(xsd_doc)

xml_doc = etree.parse('archivo.xml')

try:
    xsd.assertValid(xml_doc)
    print('VALIDACION XSD: OK')
except etree.DocumentInvalid as e:
    for err in xsd.error_log:
        print(f'  Linea {err.line}: {err.message}')
```

**Nota:** `root.iter()` itera comentarios en lxml. Siempre usar `root.iter("*")` para filtrar.

## Recomendación: Modo Dual de Serialización

La solución óptima NO es reescribir NeTEx-ES, sino implementar un modo dual:

```
Modo NeTEx-ES (actual)        → desarrollo, debugging, legibilidad
Modo XSD-compatible (nuevo)   → producción, NAP, interoperabilidad europea
         ↑
    Mismo modelo de datos (shared_model.py)
```

El convertidor ya tiene `shared_model.py` compartido. Añadir un segundo serializador en el writer que:
1. Reordene elementos según orden XSD
2. Corrija enumeraciones (`LineType`, etc.)
3. Use `ValidBetween` en vez de `validBetween`
4. Use `dateTime` en vez de `date` para fechas
5. Elimine atributos extra en `PropertyOfDay`

Es un cambio mucho menor que reescribir todo el proyecto.

## Estimación de Esfuerzo

| Nivel | Errores | Esfuerzo |
|-------|---------|----------|
| FÁCIL (casing, formato, atributos) | E1, E2, E3, E9, E13 | ~2-3h |
| MEDIO (enumeraciones, nombres) | E4, E11, E12 | ~4-6h |
| ALTO (reestructuración árbol) | E5, E6, E7, E8, E10, E14 | ~2-3 semanas |
| **Total** | 14 categorías | **~3-4 semanas** |
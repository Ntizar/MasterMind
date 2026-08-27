# Auditoría de Estado Real — netex-es (15 Jul 2026)

## Resumen ejecutivo

El proyecto **netex-es** está en **estado de producción parcial**: la conversión GTFS→NeTEx-ES funciona correctamente con datos reales (Ouigo: 68 viajes, 231 stop_times, 16 paradas, 11 rutas), genera XML sin duplicados, con IDs en formato ES correcto, y el validador español reporta **0 errores y solo 3 warnings**. Sin embargo, el **round-trip NeTEx→GTFS pierde TODOS los viajes y stop_times** porque el reader no lee la estructura `<passingTimes><TimetablePassingTime>` que el writer genera.

## Estado de tests

| Componente | Pass | Fail | Skip | Xfail | Total |
|-----------|------|------|------|-------|-------|
| gtfs-to-netex-es | 91 | 0 | 18 | 2 | 111 |
| netex-es-to-gtfs | 13 | 0 | 0 | 0 | 13 |
| netex-es-validator | 34 | 0 | 0 | 0 | 34 |
| **Total** | **138** | **0** | **18** | **2** | **153** |

**0 fallos reales.** Los 18 skip y 2 xfail son features no implementadas, no bugs.

## Prueba con feed real (Ouigo)

### GTFS → NeTEx
- **68 viajes**, **231 stop_times**, **16 paradas**, **11 rutas**
- XML: 356 KB, 1.932 IDs
- ✅ Sin IDs duplicados
- ✅ Todos los IDs en formato ES (ES:{TIPO}:{OP}:{SEQ})
- ✅ Namespace correcto

### Validación española
- **0 errores**
- **3 warnings**:
  1. `NETEX_ID_8`: Codespace sin version attribute
  2. `OPERATOR_1`: Operator sin CompanyNumber
  3. `COMPOSITE_FRAME_6`: CompositeFrame sin AvailabilityCondition

### Round-trip NeTEx → GTFS
- Stops: 16/16 ✅
- Routes: 11/11 ✅
- **Trips: 0/68 ❌**
- **StopTimes: 0/231 ❌**
- Shapes: 0/0 (el feed Ouigo no tiene shapes)

## Bugs críticos identificados

### 1. Round-trip pierde TODOS los viajes (CRÍTICO)

**Causa:** El writer genera `<passingTimes><TimetablePassingTime>` pero el reader busca `<calls><Call>`.

El reader (`netex_reader.py` línea 515-548) hace:
```python
calls = self._find_children(vj, 'calls')
if not calls:
    calls_elem = self._find_one(vj, 'calls')
```

Pero el XML generado contiene `<passingTimes>` con `<TimetablePassingTime>`, no `<calls>` con `<Call>`.

**Impacto:** El round-trip NeTEx→GTFS es funcionalmente roto. Se lee el feed, se generan trips vacíos, y los stop_times nunca se crean.

**Nota:** Esto está documentado en el skill como feature pendiente (Punto 3: "Round-trip NeTEx→GTFS — NeTExReader no implementa lectura de trips/stop_times").

### 2. 3 warnings del validador (MENOR)

- `NETEX_ID_8`: El writer no añade `version="1"` al elemento Codespace
- `OPERATOR_1`: El writer no genera `CompanyNumber` para el Operator
- `COMPOSITE_FRAME_6`: El writer no genera `AvailabilityCondition` en el CompositeFrame

Estos son fixes de 3 líneas cada uno.

### 3. No hay XSD validation real (INFORMACIÓN)

La URL del XSD oficial NeTEx-CEN 1.14 no está disponible públicamente (404). El validador usa `_basic_validation` (regex) como fallback. No se puede validar contra el schema oficial.

## Features NO implementadas (documentadas como TODO)

1. **TicketingMode en FareProduct** — No genera `SingleTicket`, `DayTicket`, `SeasonTicket` a partir de la duración del producto
2. **fare_media_type mapping** — Usa valores numéricos (`0`, `1`, `2`) en vez de strings NeTEx
3. **Round-trip NeTEx→GTFS** — Roto: pierde todos los viajes y stop_times
4. **GTFS-Fares v2 → FareStructureElement por zona** — Se generan FareProducts pero no FareStructureElements desplegados por zona

## Arquitectura

- **Monorepo consolidado** en `/root/workspace/netex-es/`
- 3 tools + 1 package + 13 tests files
- Writer modularizado en 7 archivos (<400 líneas c/u)
- Validador: 218 reglas en 18 módulos de reglas
- Spec-driven: el paquete `netex-es-spec` existe pero **no es importado por ningún tool** (spec no es fuente de verdad)

## Especificación vs código

| Aspecto | Spec | Código | XSD |
|---------|------|--------|-----|
| `ValidBetween` | PascalCase ✅ | PascalCase ✅ | PascalCase ✅ |
| `dataObjects` | Dice NO | Lo usa ✅ | Lo requiere ✅ |
| `LineType` | `tram`/`metro` | Diferente mapeo | `local`/`urban`/`express` |
| `version` | Atributo | Elemento en ejemplo | Atributo |
| Orden elementos | No especificado | Variable | Muy estricto |

## Veredicto

**¿Está en producción?** Sí, para el caso de uso principal: **GTFS→NeTEx-ES con validación española**. Con feeds reales (Ouigo) funciona sin errores.

**¿Hay errores muy grandes?** Sí, uno: **el round-trip NeTEx→GTFS es funcionalmente roto** (pierde 100% de los viajes). Esto no afecta a la conversión GTFS→NeTEx que es el caso de uso principal, pero si se necesita bidireccional, hay que arreglar el reader.

Los 3 warnings del validador son triviales (3 líneas cada uno).

## Prioridad de fixes

1. **Alta**: Arreglar reader para leer `<passingTimes><TimetablePassingTime>` → restaurar round-trip
2. **Media**: Añadir `version="1"` al Codespace
3. **Media**: Añadir `CompanyNumber` al Operator
4. **Media**: Añadir `AvailabilityCondition` al CompositeFrame
5. **Baja**: Implementar TicketingMode
6. **Baja**: Mapear fare_media_type a strings NeTEx
7. **Baja**: Implementar GTFS-Fares v2 → FareStructureElement
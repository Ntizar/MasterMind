# Comparativa NeTEx-ES vs NeTEx-Nórdico vs NeTEx-FR

> Generado 2026-07-07. Fuente: specs oficiales, GitHub repos, Confluence Entur.

## Puntuación Global

| Dimensión | NeTEx-ES | NeTEx-Nórdico | NeTEx-FR | Ganador |
|---|---:|---:|---:|---|
| IDs | 8/10 | 8/10 | 5/10 | 🤝 ES = Nórdico |
| Paradas | 10/10 | 8/10 | 5/10 | 🇪🇸 ES |
| Modos | 9/10 | 8/10 | 6/10 | 🇪🇸 ES |
| Tarifas | 6/10 | 9/10 | 4/10 | 🇳🇴 Nórdico |
| Packaging | 4/10 | 9/10 | 7/10 | 🇳🇴 Nórdico |
| Validación | 2/10 | 10/10 | 1/10 | 🇳🇴 Nórdico |
| Conversión GTFS | 9/10 | 5/10 | 7/10 | 🇪🇸 ES |
| Calendarios | 8/10 | 7/10 | 6/10 | 🇪🇸 ES |
| Geografía | 6/10 | 7/10 | 9/10 | 🇫🇷 FR |
| **TOTAL** | **62/100** | **69/100** | **48/100** | |

## Gap Crítico: Validación

NeTEx-ES tiene ~5 reglas de validación custom vs 100+ del validador nórdico.

**Reglas nórdicas prioritarias que ES debería replicar:**

| Código | Regla | Severidad |
|---|---|---|
| `LINE_4` | Line missing TransportMode | ERROR |
| `LINE_5` | Line missing TransportSubMode | ERROR |
| `SERVICE_JOURNEY_1` | ServiceJourney must exist | ERROR |
| `SERVICE_JOURNEY_12` | ServiceJourney missing OperatorRef | ERROR |
| `NETEX_ID_1` | NeTEx ID duplicated across files | ERROR |
| `NETEX_ID_5` | NeTEx ID unresolved reference | ERROR |
| `NETEX_ID_6` | NeTEx ID reference to invalid element | ERROR |
| `COMPOSITE_FRAME_3` | CompositeFrame missing ValidBetween | ERROR |
| `VALIDITY_CONDITIONS_IN_LINE_FILE_1` | ValidityConditions missing in all frames | ERROR |
| `TRANSPORT_SUB_MODE_ON_LINE` | Line Illegal TransportSubMode | WARNING |
| `INTERCHANGE_1` | Interchange invalid properties | ERROR |
| `ROUTE_4` | Route missing pointsInSequence | ERROR |
| `FLEXIBLE_LINE_1` | FlexibleLine missing FlexibleLineType | ERROR |

**Arquitectura del validador nórdico:**
1. XML Schema validation (XSD CEN) — bloqueante
2. XPath validation — 20+ reglas
3. JAXB validation — navegación objeto, reglas complejas

## Diferencias Clave de Diseño

### IDs
- **ES:** `ES:{Tipo}:{Operador}:{Secuencia}` — incluye operador (esencial para 50+ operadores españoles)
- **Nórdico:** `NO:{Tipo}:{CódigoFuente}:{Secuencia}` — similar pero sin operador granular
- **FR:** `FR:{Tipo}:{ID}` — `version="any"` fijo (sin historial)

### Paradas
- **ES:** 4 niveles (StopPlace → Quay → PassengerStoppingArea → StopPoint)
- **Nórdico:** 3 niveles (sin PassengerStoppingArea)
- **FR:** 2 niveles (Quay = StopPoint, fusionados)

### Modos
- **ES:** 12 modos con subtipos (expressBus, nightBus, longDistanceBus, regionalTrain)
- **Nórdico:** Soporte FlexibleLine/FlexibleService (servicios a demanda)
- **FR:** 6 modos básicos, sin subtipos avanzados

### Packaging
- **ES:** ZIP con 1 XML monolítico → problema con feeds grandes
- **Nórdico:** ZIP con `line_*.xml` + `_common.xml` → estándar de facto
- **FR:** ZIP con `arrets.xml`, `calendriers.xml`, `offre_*.xml`

## Mejoras Prioritarias para NeTEx-ES

1. **Crear validador NeTEx-ES** (basado en netex-validator-java) — GAP MÁS GRANDE
2. **Packaging multi-archivo** — `_common.xml` + `line_{id}.xml`
3. **Aumentar reglas a 50+** — replicar reglas nórdicas críticas
4. **Soporte FlexibleLine** — servicios a demanda (municipios <10k hab.)
5. **Sección de ventas** — ciclo de venta de billetes
6. **Convertidor en Rust** — performance para feeds grandes (Madrid, Barcelona)

## Fuentes

- [DATA4PT NeTEx Wiki](https://data4pt.org/wiki/NeTEX)
- [entur/netex-validator-java](https://github.com/entur/netex-validator-java)
- [Nordic NeTEx Profile (Håndbok N801)](https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/728891481/Nordic+NeTEx+Profile)
- [hove-io/transit_model/gtfs2netexfr](https://github.com/hove-io/transit_model/tree/master/gtfs2netexfr)
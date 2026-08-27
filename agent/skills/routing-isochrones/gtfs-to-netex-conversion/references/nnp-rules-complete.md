# 100+ Reglas de Validación NeTEx-Nórdico (NNP)

> Fuente: entur/netex-validator-java — el validador de referencia industrial para NeTEx
> Versión: 12.0.1 | Reglas: 100+ | Licencia: Apache 2.0

## Arquitectura del validador

3 capas de validación secuencial:
1. **XSD Schema** — Bloqueante. Si falla, no se ejecuta lo demás.
2. **XPath** — Reglas semánticas sobre el documento XML. Bloqueante.
3. **JAXB** — Navegación por objeto NeTEx. Para reglas complejas.

Cada regla tiene: código, nombre, severidad (INFO/WARNING/ERROR/CRITICAL), mensaje parametrizable.
Configuración YAML internacionalizable.

## Lista completa de reglas

### AUTHORITY (5 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| AUTHORITY_1 | Authority missing CompanyNumber | ERROR |
| AUTHORITY_2 | Authority missing Name | ERROR |
| AUTHORITY_3 | Authority missing LegalName | ERROR |
| AUTHORITY_4 | Authority missing ContactDetails | WARNING |
| AUTHORITY_5 | Authority missing Url for ContactDetails | WARNING |

### BLOCK (3 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| BLOCK_1 | Block missing VehicleScheduleFrame | ERROR |
| BLOCK_2 | Block missing Journey | ERROR |
| BLOCK_3 | Block missing DayType | ERROR |

### BOOKING (5 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| BOOKING_1 | Booking illegal BookingAccess | ERROR |
| BOOKING_2 | Booking illegal BookingMethod | ERROR |
| BOOKING_3 | Booking illegal BookWhen | ERROR |
| BOOKING_4 | Booking property | WARNING |
| BOOKING_5 | Missing BookWhen or MinimumBookingPeriod | WARNING |

### BUY_WHEN (1 regla)
| Código | Descripción | Severidad |
|---|---|---|
| BUY_WHEN_1 | BuyWhen illegal value | ERROR |

### COMPOSITE_FRAME (7 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| COMPOSITE_FRAME_1 | CompositeFrame - missing ValidityCondition | ERROR |
| COMPOSITE_FRAME_2 | CompositeFrame - invalid nested ValidityCondition | ERROR |
| COMPOSITE_FRAME_3 | CompositeFrame - missing ValidBetween | ERROR |
| COMPOSITE_FRAME_4 | CompositeFrame - invalid ValidBetween | ERROR |
| COMPOSITE_FRAME_5 | CompositeFrame - invalid AvailabilityCondition | ERROR |
| COMPOSITE_FRAME_6 | CompositeFrame - missing AvailabilityCondition | ERROR |
| COMPOSITE_FRAME_SITE_FRAME | CompositeFrame - unexpected SiteFrame | ERROR |

### COMPOSITE_TIMETABLE_FRAME_IN_COMMON_FILE (1 regla)
| Código | Descripción | Severidad |
|---|---|---|
| COMPOSITE_TIMETABLE_FRAME_IN_COMMON_FILE | CompositeFrame - Illegal TimetableFrame in common file | ERROR |

### DATED_SERVICE_JOURNEY (5 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| DATED_SERVICE_JOURNEY_1 | DatedServiceJourney missing OperatingDayRef | ERROR |
| DATED_SERVICE_JOURNEY_2 | DatedServiceJourney missing ServiceJourneyRef | ERROR |
| DATED_SERVICE_JOURNEY_3 | DatedServiceJourney multiple ServiceJourneyRef | ERROR |
| DATED_SERVICE_JOURNEY_4 | DatedServiceJourney multiple versions | ERROR |
| DATED_SERVICE_JOURNEY_5 | DatedServiceJourney multiple references to same DSJ | ERROR |

### DEAD_RUN (3 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| DEAD_RUN_1 | DeadRun missing PassingTime references | ERROR |
| DEAD_RUN_2 | DeadRun missing JourneyPattern references | ERROR |
| DEAD_RUN_3 | DeadRun missing DayType references | ERROR |

### DESTINATION_DISPLAY (2 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| DESTINATION_DISPLAY_1 | DestinationDisplay missing FrontText | ERROR |
| DESTINATION_DISPLAY_2 | DestinationDisplay missing DestinationDisplayRef on Via | ERROR |

### FLEXIBLE_LINE (5 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| FLEXIBLE_LINE_1 | FlexibleLine missing FlexibleLineType | ERROR |
| FLEXIBLE_LINE_8 | FlexibleLine illegal FlexibleLineType | ERROR |
| FLEXIBLE_LINE_9 | FlexibleLine illegal FlexibleServiceType | ERROR |
| FLEXIBLE_LINE_10 | FlexibleLine illegal use of both BookWhen and MinimumBookingPeriod | ERROR |
| FLEXIBLE_LINE_11 | FlexibleLine BookWhen without LatestBookingTime | ERROR |

### FLEXIBLE_SERVICE (4 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| FLEXIBLE_SERVICE_1 | FlexibleService missing Id on FlexibleServiceProperties | ERROR |
| FLEXIBLE_SERVICE_2 | FlexibleService missing version on FlexibleServiceProperties | ERROR |
| FLEXIBLE_SERVICE_3 | FlexibleService illegal use of both BookWhen and MinimumBookingPeriod | ERROR |
| FLEXIBLE_SERVICE_4 | FlexibleService BookWhen without LatestBookingTime | ERROR |

### INTERCHANGE (3 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| INTERCHANGE_1 | Interchange invalid properties | ERROR |
| INTERCHANGE_2 | Interchange unexpected MaximumWaitTime | ERROR |
| INTERCHANGE_3 | Interchange excessive MaximumWaitTime | WARNING |

### JOURNEY_PATTERN (9 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| JOURNEY_PATTERN_1 | JourneyPattern illegal element ServiceJourneyPattern | ERROR |
| JOURNEY_PATTERN_2 | JourneyPattern missing JourneyPattern | ERROR |
| JOURNEY_PATTERN_3 | JourneyPattern missing RouteRef | ERROR |
| JOURNEY_PATTERN_4 | JourneyPattern missing DestinationDisplayRef on first stop | ERROR |
| JOURNEY_PATTERN_5 | JourneyPattern illegal DestinationDisplayRef on last stop | ERROR |
| JOURNEY_PATTERN_6 | JourneyPattern stop point without boarding or alighting | ERROR |
| JOURNEY_PATTERN_7 | JourneyPattern illegal repetition of DestinationDisplay | ERROR |
| JOURNEY_PATTERN_8 | JourneyPattern illegal use of both BookWhen and MinimumBookingPeriod | ERROR |
| JOURNEY_PATTERN_9 | JourneyPattern BookWhen without LatestBookingTime | ERROR |

### LINE (9 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| LINE_1 | Line missing Line or FlexibleLine | ERROR |
| LINE_2 | Line missing Name | ERROR |
| LINE_3 | Line missing PublicCode | ERROR |
| LINE_4 | **Line missing TransportMode** | ERROR |
| LINE_5 | **Line missing TransportSubMode** | ERROR |
| LINE_6 | Line with incorrect use of Route | ERROR |
| LINE_7 | Line missing Network or GroupOfLines | ERROR |
| LINE_8 | Invalid color coding length on Presentation | WARNING |
| LINE_9 | Invalid color coding value on Presentation | WARNING |

### NETEX_ID (7 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| NETEX_ID_1 | **NeTEx ID duplicated across files** | ERROR |
| NETEX_ID_5 | **NeTEx ID unresolved reference** | ERROR |
| NETEX_ID_6 | **NeTEx ID reference to invalid element** | ERROR |
| NETEX_ID_7 | NeTEx ID invalid value | ERROR |
| NETEX_ID_8 | NeTEx ID missing version on elements | ERROR |
| NETEX_ID_9 | NeTEx ID missing version on reference | ERROR |
| NETEX_ID_10 | Duplicate NeTEx ID across common files | ERROR |

### NETWORK (3 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| NETWORK_1 | Network missing AuthorityRef | ERROR |
| NETWORK_2 | Network missing Name on Network | ERROR |
| NETWORK_3 | Network missing Name on GroupOfLines | ERROR |

### NOTICE (7 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| NOTICE_1 | Notice missing Text | ERROR |
| NOTICE_2 | Notice missing Text with alternative text | ERROR |
| NOTICE_3 | Notice missing language with alternative text | ERROR |
| NOTICE_4 | Notice duplicated alternative texts | ERROR |
| NOTICE_5 | Notice duplicated assignment | ERROR |
| NOTICE_6 | Notice assignment missing reference to noticed object | ERROR |
| NOTICE_7 | Notice assignment missing reference to notice | ERROR |

### OPERATOR (7 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| OPERATOR_1 | Operator missing CompanyNumber | ERROR |
| OPERATOR_2 | Operator missing Name | ERROR |
| OPERATOR_3 | Operator missing LegalName | ERROR |
| OPERATOR_4 | Operator missing ContactDetails | ERROR |
| OPERATOR_5 | Operator missing Url for ContactDetails | WARNING |
| OPERATOR_6 | Operator missing CustomerServiceContactDetails | WARNING |
| OPERATOR_7 | Operator missing Url for CustomerServiceContactDetails | WARNING |

### PASSENGER_STOP_ASSIGNMENT (3 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| PASSENGER_STOP_ASSIGNMENT_1 | PassengerStopAssignment missing ScheduledStopPointRef | ERROR |
| PASSENGER_STOP_ASSIGNMENT_2 | PassengerStopAssignment missing QuayRef | ERROR |
| PASSENGER_STOP_ASSIGNMENT_3 | PassengerStopAssignment duplicated Quay assignment | ERROR |

### RESOURCE_FRAME (1 regla)
| Código | Descripción | Severidad |
|---|---|---|
| RESOURCE_FRAME_IN_LINE_FILE | ResourceFrame must be exactly one | ERROR |

### ROUTE (6 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| ROUTE_1 | Route missing | ERROR |
| ROUTE_2 | Route missing Name | ERROR |
| ROUTE_3 | Route missing LineRef | ERROR |
| ROUTE_4 | Route missing pointsInSequence | ERROR |
| ROUTE_5 | Route illegal DirectionRef | ERROR |
| ROUTE_6 | Route duplicated order | ERROR |

### SERVICE_CALENDAR (5 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| SERVICE_CALENDAR_1 | ServiceCalendar unused DayType | WARNING |
| SERVICE_CALENDAR_2 | ServiceCalendar empty ServiceCalendar | ERROR |
| SERVICE_CALENDAR_3 | ServiceCalendar missing ToDate | ERROR |
| SERVICE_CALENDAR_4 | ServiceCalendar missing FromDate | ERROR |
| SERVICE_CALENDAR_5 | ServiceCalendar invalid time interval | ERROR |

### SERVICE_FRAME (6 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| SERVICE_FRAME_1 | ServiceFrame unexpected element GroupOfLines | ERROR |
| SERVICE_FRAME_2 | ServiceFrame unexpected element timingPoints | ERROR |
| SERVICE_FRAME_3 | ServiceFrame missing Projection on RoutePoint | ERROR |
| SERVICE_FRAME_IN_COMMON_FILE_1 | ServiceFrame unexpected element Line in common | ERROR |
| SERVICE_FRAME_IN_COMMON_FILE_2 | ServiceFrame unexpected element Route in common | ERROR |
| SERVICE_FRAME_IN_COMMON_FILE_3 | ServiceFrame unexpected element JourneyPattern in common | ERROR |

### SERVICE_JOURNEY (17 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| SERVICE_JOURNEY_1 | **ServiceJourney must exist** | ERROR |
| SERVICE_JOURNEY_2 | ServiceJourney illegal element Call | ERROR |
| SERVICE_JOURNEY_3 | ServiceJourney missing PassingTimes | ERROR |
| SERVICE_JOURNEY_4 | ServiceJourney missing arrival and departure | ERROR |
| SERVICE_JOURNEY_5 | ServiceJourney missing departure times | ERROR |
| SERVICE_JOURNEY_6 | ServiceJourney missing arrival time for last stop | ERROR |
| SERVICE_JOURNEY_7 | ServiceJourney identical arrival and departure | ERROR |
| SERVICE_JOURNEY_8 | ServiceJourney missing id on TimetabledPassingTime | ERROR |
| SERVICE_JOURNEY_9 | ServiceJourney missing version on TimetabledPassingTime | ERROR |
| SERVICE_JOURNEY_10 | ServiceJourney missing reference to JourneyPattern | ERROR |
| SERVICE_JOURNEY_11 | ServiceJourney invalid overriding of transport modes | ERROR |
| SERVICE_JOURNEY_12 | **ServiceJourney missing OperatorRef** | ERROR |
| SERVICE_JOURNEY_13 | ServiceJourney missing reference to calendar data | ERROR |
| SERVICE_JOURNEY_14 | ServiceJourney duplicated reference to calendar data | ERROR |
| SERVICE_JOURNEY_15 | ServiceJourney missing some passing times | ERROR |
| SERVICE_JOURNEY_16 | ServiceJourney multiple versions | ERROR |
| SERVICE_JOURNEY_17 | Non-unique NeTEx id for TimetabledPassingTime | ERROR |

### SERVICE_LINK (5 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| SERVICE_LINK_1 | ServiceLink missing FromPointRef | ERROR |
| SERVICE_LINK_2 | ServiceLink missing ToPointRef | ERROR |
| SERVICE_LINK_3 | ServiceLink missing element Projections | ERROR |
| SERVICE_LINK_4 | ServiceLink missing coordinate list | ERROR |
| SERVICE_LINK_5 | ServiceLink less than 2 points | ERROR |

### SITE_FRAME (2 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| SITE_FRAME_IN_COMMON_FILE | Unexpected SiteFrame in Common file | ERROR |
| SITE_FRAME_IN_LINE_FILE | Unexpected SiteFrame in Line file | ERROR |

### TIMETABLE_FRAME (1 regla)
| Código | Descripción | Severidad |
|---|---|---|
| TIMETABLE_FRAME_IN_COMMON_FILE | TimetableFrame illegal in Common file | ERROR |

### TRANSPORT_MODE (4 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| TRANSPORT_MODE_ON_LINE | **Line Illegal TransportMode** | WARNING |
| TRANSPORT_MODE_ON_SERVICE_JOURNEY | ServiceJourney Illegal TransportMode | WARNING |
| TRANSPORT_SUB_MODE_ON_LINE | **Line Illegal TransportSubMode** | WARNING |
| TRANSPORT_SUB_MODE_ON_SERVICE_JOURNEY | ServiceJourney Illegal TransportSubMode | WARNING |

### VALIDITY_CONDITIONS (9 reglas)
| Código | Descripción | Severidad |
|---|---|---|
| VALIDITY_CONDITIONS_IN_COMMON_FILE_1 | Missing in ServiceFrame or ServiceCalendarFrame | ERROR |
| VALIDITY_CONDITIONS_IN_COMMON_FILE_2 | Missing in ResourceFrames | ERROR |
| VALIDITY_CONDITIONS_IN_COMMON_FILE_3 | Missing in ServiceFrames | ERROR |
| VALIDITY_CONDITIONS_IN_COMMON_FILE_4 | Missing in ServiceCalendarFrames | ERROR |
| VALIDITY_CONDITIONS_IN_LINE_FILE_1 | **ValidityConditions missing in all frames** | ERROR |
| VALIDITY_CONDITIONS_IN_LINE_FILE_2 | Missing in ServiceFrames (line file) | ERROR |
| VALIDITY_CONDITIONS_IN_LINE_FILE_3 | Missing in ServiceCalendarFrames (line file) | ERROR |
| VALIDITY_CONDITIONS_IN_LINE_FILE_4 | Missing in TimeTableFrames | ERROR |
| VALIDITY_CONDITIONS_IN_LINE_FILE_5 | Missing in VehicleScheduleFrame | ERROR |

### VERSION (1 regla)
| Código | Descripción | Severidad |
|---|---|---|
| VERSION_NON_NUMERIC | Non-numeric NeTEx version | ERROR |

## Total: 103 reglas

### Distribución por severidad:
- **ERROR**: ~85 reglas (bloquean la validación)
- **WARNING**: ~15 reglas (no bloquean pero alertan)
- **INFO**: ~3 reglas (informativas)
- **CRITICAL**: 0 (todas las críticas son ERROR)

### Reglas prioritarias para NeTEx-ES (top 20):
1. LINE_4 — TransportMode obligatorio
2. LINE_5 — TransportSubMode obligatorio
3. SERVICE_JOURNEY_1 — ServiceJourney must exist
4. SERVICE_JOURNEY_12 — OperatorRef obligatorio
5. NETEX_ID_1 — IDs únicos
6. NETEX_ID_5 — Referencias no resueltas
7. NETEX_ID_6 — Referencias a elementos inválidos
8. VALIDITY_CONDITIONS_IN_LINE_FILE_1 — ValidityConditions en todos los frames
9. COMPOSITE_FRAME_3 — ValidBetween obligatorio
10. ROUTE_4 — pointsInSequence obligatorio
11. SERVICE_JOURNEY_4 — arrival y departure obligatorios
12. SERVICE_JOURNEY_10 — JourneyPatternRef obligatorio
13. TRANSPORT_MODE_ON_LINE — Modo válido
14. TRANSPORT_SUB_MODE_ON_LINE — Submodo válido
15. JOURNEY_PATTERN_3 — RouteRef obligatorio
16. LINE_2 — Name obligatorio
17. LINE_3 — PublicCode obligatorio
18. SERVICE_CALENDAR_2 — ServiceCalendar no vacío
19. SERVICE_JOURNEY_13 — Calendar data obligatorio
20. NETEX_ID_8 — Version en elementos

# Caso de estudio: NeTEx-ES — Valoración de trabajo IA

> Análisis real del proyecto NeTEx-ES (perfil español de NeTEx-CEN 1.14) realizado el 2026-07-11.

## El proyecto

**5 repositorios privados** en GitHub (Ntizar/):
- `netex-es-spec` — Especificación NeTEx-ES v3.5.0 (1.491 líneas, 27 secciones, 18 decisiones arquitectónicas)
- `netex-es-validator` — Validador con 218 reglas en 18 módulos (~7.600 líneas Python, 30 archivos)
- `gtfs-to-netex-es` — Conversor GTFS→NeTEx-ES (~9.400 líneas Python, 27 archivos, 11 tests)
- `netex-es-to-gtfs` — Conversor NeTEx-ES→GTFS (~3.000 líneas Python, 12 archivos, round-trip verificado)
- `netex` — Repo monolito original con todo integrado (126 archivos, ~18.100 líneas Python)

## Métricas totales

| Métrica | Valor |
|---|---|
| Repositorios | 5 |
| Archivos Python | ~128 (únicos, contando overlap) |
| Líneas Python (aprox) | ~38.000 |
| Tests | 164 |
| Reglas de validación | 218 en 18 módulos |
| Secciones de spec | 27 |
| Decisiones arquitectónicas documentadas | 18 |
| Ejemplo XML completo | 2.237 líneas |
| Tiempo real con IA | ~19 horas (07-jul 07:30 → 08-jul 02:33) |

## Conocimiento de dominio requerido

1. **NeTEx-CEN 1.14** (CEN/TS 16614) — 3 partes, cientos de páginas. En España: 5-10 personas que lo entienden a este nivel.
2. **Transmodel** (EN 12896) — modelo conceptual europeo detrás de NeTEx.
3. **GTFS spec** — estática + Flexible + Fares v2.
4. **Sistema de transporte español** — 50+ operadores, consorcios (CRTM, TMB, EMT), códigos INE, 12 modos.
5. **Festivos españoles** — 14 nacionales + 19 autonómicos, algoritmo Butcher/Meeus para Pascua.
6. **Multilingüismo** — 4 lenguas co-oficiales + valenciano + aranés, mapeo CCAA→idioma.
7. **Sistemas de coordenadas** — WGS84, ETRS89/UTM (3 husos), REGCAN95/UTM, fórmulas USGS/Snyder.
8. **Diseño de schemas XML** — XSD, namespaces, frames tipados vs dataObjects.
9. **Arquitectura de software** — modular, solo stdlib Python, round-trip bidireccional.
10. **Testing de integridad** — verificación con feeds reales EMT Valencia (236K stop_times, 0 pérdida).

## Estimación de horas equipo humano

| Fase | Equipo | Tiempo | Horas |
|---|---|---|---|
| Investigación del estándar | 2-3 expertos | 4-6 semanas | 320-480h |
| Escritura de spec | 1-2 personas | 3-4 semanas | 120-320h |
| Validador (218 reglas) | 2 devs | 3-4 meses | 1.000-1.300h |
| Conversor GTFS→NeTEx | 2-3 devs | 3-4 meses | 1.300-1.600h |
| Conversor NeTEx→GTFS | 1-2 devs | 2-3 meses | 320-520h |
| Tests e integración | 1-2 testers | 2-3 meses | 320-520h |
| Documentación | 1-2 personas | 2-4 semanas | 80-320h |
| **TOTAL** | **3-5 personas** | **1.5-2.5 años** | **3.500-5.000h** |

## Valor monetario

- A precio consultoría (80-120€/h): **280.000€ - 600.000€**
- Competencia europea (Entur, Hove): **500.000€+ y 2 años**
- Coste real con IA: tiempo de David + API de IA

## Tabla de asimetría

| | Equipo tradicional | David con IA |
|---|---|---|
| Tiempo | 1.5-2.5 años | 19 horas |
| Coste | 280K-600K€ | Tiempo + IA |
| Conocimiento necesario | 5-10 expertos raros | Juicio + IA |
| Precio de venta potencial | 500K€+ | Lo que decida |
| Margen | 30-40% | 90%+ |

## Modelos de monetización aplicables

### A — Producto repetible
Cada operador de transporte español (EMT, TMB, Metro Madrid, Renfe, consorcios) necesita cumplir Reglamento UE 2017/1926 (NAP). NeTEx-ES es la única solución completa que existe.
- Licencia por operador: 15.000-50.000€
- Integración + soporte anual: 10.000-30.000€/año

### B — Proyecto de consultoría
Vender al Ministerio de Transportes o consorcio grande:
- "Implementación perfil NeTEx español + validador + conversores" → 150.000-300.000€
- Precio basado en valor entregado (cumplimiento normativo), no en horas

### C — Servicio continuo
- "Mantenimiento y evolución del perfil NeTEx-ES" → 50.000-100.000€/año
- IA permite mantener con esfuerzo mínimo, valor para cliente es constante

## Argumento de venta clave

> "El Reglamento UE 2017/1926 exige que todos los operadores publiquen datos en el NAP español en formato NeTEx. No hay perfil español oficial. Nosotros lo hemos creado, con validador y conversores verificados. Es el único que existe."

## Lección

El cliente no necesita saber que tardaste 19 horas. Necesita saber que tienes la única solución completa que existe. El valor no está en el tiempo invertido — está en el resultado entregado y en el conocimiento de dominio que se aplicó para diseñarlo.

*Hecho con ❤️ por David Antizar*

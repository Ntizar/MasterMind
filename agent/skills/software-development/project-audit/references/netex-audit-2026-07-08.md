# Caso de Estudio: Auditoría NeTEx-ES v3.5.0 (2026-07-08)

## Contexto

Auditoría en solitario de `Ntizar/netex-es-spec` v3.5.0. El proyecto había evolucionado de v2.0 a v3.5 en dos días (FlexibleLine, multi-archivo, 218 reglas, GTFS-Fares v2, Bookings, CRS UTM, multilingüismo), pero la comparativa competitiva (`references/comparativa-netex-perfiles.md`) no se actualizó — seguía describiendo v2.0.

## Artefactos auditados (6)

- `NeTEx-ES.md` — Spec principal (1.491 líneas, 27 secciones)
- `DECISIONES.md` — 18 decisiones arquitectónicas
- `CHANGELOG.md` — Historial v2.0 → v3.5
- `README.md` — Resumen del proyecto
- `references/comparativa-netex-perfiles.md` — Comparativa con nórdico y francés
- `examples/complete-example.xml` — XML generado (2.237 líneas)

## 10 incoherencias detectadas

| # | Problema | Severidad | Causa raíz |
|---|---|---|---|
| 1 | Spec prohíbe `dataObjects` pero ejemplo XML lo usa | Alta | Ejemplo generado por código viejo |
| 2 | Comparativa dice "80+ reglas" cuando son 218 | Alta | Comparativa congelada en v2.0 |
| 3 | Comparativa marca FlexibleLine como ausente (ya implementado) | Alta | Misma causa |
| 4 | Comparativa marca packaging como monolítico (ya multi-archivo) | Alta | Misma causa |
| 5 | Spec secc 4.2 usa `AccessibilitySuitable` (D6 lo prohíbe) | Media | Spec no actualizada tras D6 |
| 6 | IDs del ejemplo no siguen formato declarado en spec | Media | Ejemplo usa IDs de test, no del formato ES:{Tipo}:{Op}:{Sec} |
| 7 | Spec usa `<Address>`, ejemplo usa `<PostalAddress>` | Media | Nombres de elemento divergentes |
| 8 | Spec secc 4.2 usa `<StopPlaces>` (D3 exige camelCase) | Baja | PascalCase residual en spec |
| 9 | Comparativa referencia repo `Ntizar/netex` (incorrecto) | Baja | Typo |
| 10 | Score 66/100 autoinfravalorado (basado en v2.0) | Media | Misma causa que #2-4 |

## Patrón detectado

**La causa raíz de 6 de 10 incoherencias fue la misma: la comparativa se escribió antes de v3.0 y nunca se actualizó.** Mientras spec, DECISIONES y changelog evolucionaron a v3.5, la comparativa se quedó congelada describiendo debilidades ya resueltas. Esto es un anti-patrón: cuando un documento compara el proyecto contra competencia, debe actualizarse en cada release mayor, no solo la spec y el changelog.

## Corrección aplicada

- Comparativa reescrita completa: score 66 a 91, FlexibleLine marcado como implementado, packaging actualizado, 218 reglas, nuevas secciones (multilingüismo, FlexibleLine+Bookings), GTFS-Fares v2, CRS UTM
- Commit `a1b1d12` pushed a `main`

## Lección para auditorías futuras

1. **Auditar TODOS los artefactos, no solo spec y código.** La comparativa era el artefacto más dañino desactualizado porque es el que alguien externo leería para evaluar el proyecto.
2. **El ejemplo XML generado debe regenerarse tras cada cambio estructural de la spec.** Si la spec prohibe `dataObjects` pero el ejemplo lo usa, el ejemplo pierde credibilidad como referencia.
3. **Usar `execute_code` para checks automatizados** — ver `scripts/cross-coherence-check.py` para el patrón reutilizable.

# Monorepo Spec-Driven — Arquitectura NeTEx-ES

## Contexto

Julio 2026: los 4 repos independientes (estilo Entur) se fusionan en un monorepo con paquete Python compartido. Decisión tomada tras auditoría de compatibilidad XSD que reveló ~14 categorías de errores y duplicación masiva de código.

## Problemas que resuelve

1. **Duplicación de código:** 6 archivos idénticos entre convertidores
2. **Enumeraciones en 4 sitios:** config.py, semantic_validator.py, line_rules.py, mode_rules.py
3. **shared_model.py inexistente:** el modelo GTFSFeed estaba dentro de gtfs_reader.py
4. **Writer monolítico:** 1995 líneas, una clase para todo
5. **Spec desincronizada:** la spec decía "no usar dataObjects" pero el XSD y el ejemplo lo usaban

## Referencias

- `spec/SPEC.md` — Plan detallado de refactorización spec-driven
- `spec/NeTEx-ES.md` — Especificación principal (a actualizar)
- `spec/DECISIONES.md` — Decisiones arquitectónicas
- `spec/enums.yaml` — Enumeraciones machine-readable (a crear)
- `spec/elements.yaml` — Árboles de elementos con orden XSD (a crear)
- `spec/frames.yaml` — Estructura de frames (a crear)
- `spec/id-patterns.yaml` — Patrones de IDs (a crear)
- `packages/netex-es-spec/src/netex_es_spec/models.py` — Modelo compartido (a crear)
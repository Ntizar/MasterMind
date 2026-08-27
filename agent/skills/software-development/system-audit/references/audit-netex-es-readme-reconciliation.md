# NeTEx-ES — Audit de README vs Realidad

> **Fecha:** 2026-07-07
> **Contexto:** Auditoría del proyecto NeTEx-ES para reconciliar documentación con estado real.

## Problemas encontrados en README.md

### Números inflados

| Afirmación README | Realidad | Delta |
|---|---|---|
| "29/29 passing" | 78/84 passing (6 failed) | -6 |
| "49 tests" | 84 tests collectados | +35 |
| "2.900+ líneas de validación" | 4.042 líneas (18 módulos) | +1.142 |
| "200+ reglas" | ~150 rule classes | -50 |
| "Coverage increasing" badge | No existe | ❌ |
| "Docker (en desarrollo)" | Sin Dockerfile | ❌ |
| "schema_cache/" en estructura | No existe | ❌ |

### Archivos eliminados

1. `auditoria.md` — Artefacto de sesión (387 líneas). Sin valor para usuarios.
2. `README2.md` — Desactualizado (v1.0.0, sin validador ni app web).
3. `gtfs-sample.xml` — Archivo XML huérfano sin contexto.

## Estado real del proyecto

| Componente | Líneas | Estado |
|---|---|---|
| converter/ | ~2.600 | ✅ Funcional |
| validator/ | 4.042 | ✅ Funcional |
| app/index.html | 791 | ✅ Funcional |
| spec/NeTEx-ES.md | 777 | ✅ Completa |
| tests/ | 84 tests | ⚠️ 78/84 passing |

## Tests failing

1. `test_cli.py::test_directory` — OSError
2. `test_cli.py::test_nonexistent` — AssertionError
3. `test_gtfs_reader.py::test_feed_info` — AssertionError
4. `test_gtfs_reader.py::test_get_stop` — None
5. `test_gtfs_reader.py::test_get_route` — None
6. `test_gtfs_reader.py::test_get_trip` — None

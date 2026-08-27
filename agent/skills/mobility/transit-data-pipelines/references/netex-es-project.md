# NeTEx-ES — Proyecto de referencia

Repositorio: `github.com/Ntizar/netex`
Branch: `master`
Versión: 2.0.0
Última auditoría: 2026-07-07

## Estructura del proyecto

```
netex/
├── app/                    # Aplicación web para empresas
│   └── index.html          # Frontend profesional (791 líneas)
├── converter/
│   ├── __init__.py         # Paquete v2.0.0
│   ├── cli.py              # CLI con progreso y timing
│   ├── config.py           # Config + 25+ mapeos de transporte
│   ├── gtfs_reader.py      # Lector GTFS (.zip o directorio) — 463 líneas
│   ├── netex_writer.py     # Generador XML NeTEx-ES — 1.103 líneas
│   ├── xsd_validator.py    # Validador NeTEx 3 niveles — 225 líneas
│   ├── flexible_converter.py
│   ├── coordinate_converter.py
│   ├── id_generator.py
│   └── server.py           # Servidor HTTP para app web — 189 líneas
├── validator/              # VALIDADOR NeTEx-ES — 4.042 líneas, 150+ reglas
│   ├── reference_validator.py  # Validación de referencias e IDs — 218 líneas
│   ├── schema_validator.py     # Validación XSD — 112 líneas
│   ├── xpath_validator.py      # Validación XPath — 105 líneas
│   ├── semantic_validator.py   # Validación semántica — 797 líneas
│   ├── validator_runner.py     # Motor principal — 306 líneas
│   ├── config.py           # Configuración de reglas — 99 líneas
│   ├── cli.py              # CLI del validador — 160 líneas
│   ├── configuration.yaml
│   └── rules/              # Reglas por categoría (12 módulos)
│       ├── base_rule.py          # Clase base — 97 líneas
│       ├── id_rules.py           # Unicidad y formato IDs — 222 líneas
│       ├── line_rules.py         # Reglas de líneas — 237 líneas
│       ├── stop_rules.py         # Reglas de paradas — 169 líneas
│       ├── journey_rules.py      # Reglas de viajes — 352 líneas
│       ├── service_rules.py      # Reglas de servicios — 165 líneas
│       ├── frame_rules.py        # Reglas de frames — 318 líneas
│       ├── mode_rules.py         # Reglas de modos — 93 líneas
│       ├── es_specific.py        # Reglas España — 272 líneas
│       ├── flexible_rules.py     # FlexibleLine — 233 líneas
│       └── validity_rules.py     # Valididad temporal — 93 líneas
├── references/
│   └── comparativa-netex-perfiles-2026-07-07.md  # ES vs Nórdico vs FR
├── gtfs-sample/            # Datos ejemplo Metro de Madrid (7 archivos)
├── spec/
│   └── NeTEx-ES.md         # Especificación NeTEx-ES (777 líneas)
│       └── examples/
│           └── complete-example.xml
├── tests/                  # 84 tests — TODOS PASING
├── LICENSE                 # MIT
├── convertidor.bat         # Script Windows
├── requirements.txt
└── README.md               # Docs técnicas
```

## Tests

```bash
cd netex && python -m pytest tests/ -v        # 84 tests — 84 passing
python -m pytest tests/test_integration.py -v  # 10 integration tests
python -m pytest tests/test_validator.py -v    # 30 validator tests
```

**Estado:** 84/84 passing. Sin fallos.

## Validación

```python
# Validador CLI
python -m validator.reference_validator archivo.xml

# Validador API
from validator.validator_runner import ValidatorRunner
runner = ValidatorRunner()
result = runner.validate_file("archivo.xml")
# result.valid, result.errors, result.warnings, result.infos
```

4 niveles:
1. XSD Schema (blocking)
2. XPath (no blocking)
3. Referencias ID — unicidad y resolución
4. Semántica — reglas de negocio

## Deployment

```bash
python server.py              # localhost:8080
python server.py 9090         # custom port
```

## Notas

- 0 dependencias externas (solo stdlib Python)
- Compatible EN 12896:2016, NeTEx 1.14
- RD 571/2023 (datos abiertos transporte público España)
- Comparativa: NeTEx-ES 62/100 vs Nórdico 69/100 vs FR 48/100
- Pitfall GTFSFeed `__post_init__` índice vacío: siempre llamar `feed.rebuild_indices()` después de `reader.read()`
- Pitfall: `feed_info.txt` debe existir en sample GTFS o `test_feed_info` falla

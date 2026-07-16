# NeTEx-ES: Case Study de Machine-Readable SDD

## Contexto

**Ecosistema:** Perfil español NeTEx-CEN para datos de transporte público.
**Antes:** 4 repos independientes con código duplicado (enums, modelos, reglas de validación).
**Después:** 1 monorepo con spec YAML como fuente de verdad, paquete Python compartido.

## Estructura final

```
netex-es/
├── spec/                          ← Spec humana + machine-readable
│   ├── NeTEx-ES.md               ← Documento humano (v3.6.0, XSD-compatible)
│   ├── enums.yaml                ← Enumeraciones (LineType, TransportMode, etc.)
│   ├── elements.yaml             ← Árboles y orden XSD de elementos
│   └── frames.yaml               ← Estructura de cada frame NeTEx
├── packages/
│   └── netex-es-spec/            ← Paquete Python compartido
│       ├── pyproject.toml
│       └── src/netex_es_spec/
│           ├── __init__.py       ← Re-exporta todo
│           ├── models.py         ← GTFSFeed (modelo de datos compartido)
│           ├── enums.py          ← LineType, TransportMode, Casing, DateFormat
│           ├── elements.py       ← ELEMENT_ORDER + get_entity_order()
│           ├── frames.py         ← FRAMES + get_entity_order()
│           └── validators.py     ← Validación XSD-compartida
├── tools/
│   ├── gtfs-to-netex-es/         ← Convertidor GTFS → NeTEx-ES
│   ├── netex-es-to-gtfs/         ← Convertidor NeTEx-ES → GTFS
│   └── netex-es-validator/       ← Validador semántico + XSD
├── tests/
├── README.md
└── .gitignore
```

## Problemas resueltos

| Problema | Antes (4 repos) | Después (monorepo) |
|----------|-----------------|-------------------|
| **Enums duplicados** | LineType, TransportMode copiados en 3 repos | Una fuente: `enums.yaml` → `netex_es_spec.enums` |
| **Orden XSD** | Cada tool hardcodeaba el orden de elementos | `elements.yaml` → `get_entity_order()` centralizado |
| **Estructura de frames** | Cada tool definía los frames por su cuenta | `frames.yaml` → `FRAMES` dict compartido |
| **Validación** | Reglas esparcidas | `validators.py` con funciones reutilizables |
| **Cambio XSD** | Había que modificar N herramientas | Cambiar 1 YAML, el paquete se sincroniza |

## Lecciones aprendidas

### 1. Subagent truncation en archivos grandes
Cuando un subagente refactoriza un archivo de >1000 líneas y el timeout se alcanza durante la escritura, el archivo se trunca. **Solución:** No delegar rewrites completos de archivos grandes. Preferir parches incrementales (patch) o refactorizar primero en módulos pequeños.

### 2. YAML como runtime, no build-time
El paquete Python lee los YAMLs en tiempo de ejecución (`import yaml; yaml.safe_load()`). Esto asegura que cualquier cambio en `spec/*.yaml` se refleje inmediatamente sin reinstalar.

### 3. Orden XSD: el diablo está en los detalles
NeTEx-CEN 1.14 tiene un orden estricto de elementos hijos. Usar `_ordered_children()` con un mapa de orden evita generar XML inválido. Los errores más comunes:
- `validBetween` → `ValidBetween` (PascalCase)
- Fechas `2025-01-06` → `2025-01-06T00:00:00Z` (xs:dateTime)
- `FareProduct` → `PreassignedFareProduct`
- `PostalAddress` en posición incorrecta

### 4. Streaming mode doble mantenimiento
El writer tiene un modo streaming para sets de datos grandes. Cada cambio en el modo normal debe replicarse en streaming. **Solución:** Refactorizar streaming para que llame a las mismas funciones helper que el modo normal.

### 5. Backup antes de refactor
Al fusionar 4 repos, mantener los originales como backup antes de tocar nada. Esto permite revertir si algo sale mal.

## Comandos útiles

```bash
# Instalar paquete compartido en editable mode
cd /root/workspace/netex-es/packages/netex-es-spec
pip install -e .

# Verificar que el paquete funciona
python3 -c "from netex_es_spec import *; print('OK:', GTFSFeed.__name__, LineType.BUS, len(FRAMES), 'frames')"

# Validar XML generado contra XSD
xmllint --noout --schema /path/to/NeTEx_publication.xsd output.xml
```

## Archivos clave

- `spec/enums.yaml` — Definiciones de enumeraciones (6.3KB)
- `spec/elements.yaml` — Árboles y orden XSD (3.9KB)
- `spec/frames.yaml` — Estructura de frames (19KB)
- `packages/netex-es-spec/src/netex_es_spec/` — Paquete Python (6 módulos)
- `tools/gtfs-to-netex-es/src/converter/netex_writer.py` — Writer refactorizado (~2000 líneas)
# Auditoría netex-es monorepo — 15 Julio 2026

## Contexto
Auditoría de producción del monorepo `netex-es` (convertidores GTFS↔NeTEx-ES + validador 218 reglas). Usuario quería cerrar el proyecto con una versión de producción limpia.

## Hallazgos

### Bug casing (causa de test failure)
- **Writer** genera `TransportMode` (PascalCase) y `TransportSubmode`
- **Semantic validator** busca `TransportMode` (PascalCase) ✅
- **Standalone line_rules.py** busca `transportMode` (camelCase) ❌
- **Standalone mode_rules.py** busca `transportSubMode` (camelCase) ❌
- **Test XML** usa `transportMode`/`transportSubMode` (camelCase) ❌
- **Fix:** actualizar test XML y standalone rules a PascalCase

### Dead code: standalone rules nunca ejecutadas
- `rules/` tiene 218 reglas con `get_all_rules()`
- `validator_runner.py` nunca las importa ni llama
- Solo usa `SemanticValidator.validate()` con lógica propia duplicada
- Tests pasan al 100% porque testean el módulo directamente, no el flujo completo
- **Lección:** dual validation systems → verificar que ambos caminos se ejecutan

### Inconsistencia en conteo de reglas
- README.md principal: 218 ✅
- DECISIONES.md: 218 ✅
- validator/README.md: 209 ❌ (obsoleto)
- validator/src/validator/README.md: 209 ❌ (obsoleto)

### READMEs de tools vacíos
- `gtfs-to-netex-es/README.md`: solo título (3 líneas)
- `netex-es-to-gtfs/README.md`: solo título (3 líneas)

### CHANGELOG con archivos fantasma
- `app/server.py` (v3.0.0) — no existe
- `scripts/generar-gtfs-es.py` (v3.1.0) — no existe
- `FEEDS-REALES.md` (v3.1.0) — no existe
- **Fix:** marcar como "incluido en repo de desarrollo, no distribuido"

## Resultado
- 138 passed, 0 failed, 18 skipped, 2 xfail
- 6 fixes ejecutados, 0 fallos tras corrección

## Patrón general aplicable
1. Explorar estructura → leer docs → ejecutar tests → analizar código → cruzar referencias
2. Buscar inconsistencias de casing entre generador y validador
3. Verificar que código importado es realmente llamado (dead code detection)
4. Contar tests reales vs lo que dicen los READMEs
5. Verificar que CHANGELOG no referencia archivos inexistentes

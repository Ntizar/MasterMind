# Lecciones de Adela_cli (2026-06-15)

## Sesión: Creación del módulo Adela_cli

### Problemas encontrados y fixes

#### 1. `TemplateContext` no exportado desde `template.ts`
- **Síntoma:** `src/commands/new.ts` importa `TemplateContext` desde `template.ts` pero TypeScript dice "declares 'TemplateContext' locally, but it is not exported"
- **Fix:** Añadir `export type { TemplateContext } from './types.js'` en `template.ts`
- **Causa raíz:** El tipo se importa desde `types.ts` pero no se re-exporta, lo que rompe cuando otros archivos del módulo lo necesitan directamente

#### 2. `moduleResolution: "node"` vs `"bundler"`
- **Síntoma:** `npx tsc --noEmit` pasa con tsconfig.json pero el linter da errores de `Cannot find module 'node:fs'`
- **Fix:** Cambiar a `"moduleResolution": "bundler"`
- **Causa raíz:** `"bundler"` funciona mejor con `import()` dinámico en tests, `__dirname` implícito, y default imports ESM

#### 3. Type error en `config.author`
- **Síntoma:** `Type 'string | true' is not assignable to type 'string'`
- **Fix:** `config.author = typeof parsed.flags.author === 'string' ? parsed.flags.author : ''`
- **Causa raíz:** `parsed.flags[key]` tiene tipo `string | boolean` (porque `--yes` es booleano), pero `CliConfig.author` es `string`

### Patrón de tests que funciona

- Tests de **validación** (regex patterns) → funciones puras, sin filesystem, sin mocks
- Tests de **plantillas** → `await import()` en tests async, verificar estructura de archivos generados
- Tests de **CLI** → `cli.run([])`, `cli.run(['--help'])`, `cli.run(['--version'])`, `cli.run(['comando-falso'])`
- Tests de **comandos con filesystem** → evitar o mockear `execSync` para npm install (timeout)

### Stats del módulo
- 35 tests pasando (14 cli + 21 commands)
- 12 archivos fuente + tests + config
- 0 runtime deps
- Build + typecheck limpios

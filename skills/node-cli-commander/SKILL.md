---
name: node-cli-commander
description: >
  Patrones para construir CLIs en Node.js con Commander.js: módulos exportables
  reutilizables, entry points standalone, argumentos con validación, y estructura
  de proyecto preprocessing. Compatible ESM.
version: "1.0.0"
author: Hermes Agent
tags: [nodejs, cli, commander, esm, module, executable, preprocessing]
---

# Node.js CLI con Commander.js

## Cuándo aplicar

- Crear una herramienta de línea de comandos en Node.js
- Necesitar que un módulo funcione tanto como `import` como `node script.js` standalone
- Construir pipelines de datos (preprocesamiento, conversión, generación)
- Cualquier CLI con 2+ subcomandos

## Estructura de proyecto

```
apps/<name>/
├── package.json          # "type": "module", commander como dependencia
├── src/
│   ├── index.js          # CLI principal — commander, registra subcomandos
│   ├── module-a.js       # Exporta función + entry point standalone
│   └── module-b.js       # Exporta función + entry point standalone
├── test/
│   └── sample.csv        # Datos de ejemplo para pruebas
└── data/                 # Datos de entrada (no commit)
```

## Patrón 1: Módulo exportable con entry point standalone

Cada módulo de lógica sigue este patrón dual:

```js
// src/module.js

// ── Función exportable ────────────────────────────────────────────────
export function doSomething(opts) {
  const { input, output, flag } = opts;
  // ... lógica pura ...
  console.log(`✅ Hecho: ${output}`);
  return { result };
}

// ── Entry point standalone ───────────────────────────────────────────
if (process.argv[1] && process.argv[1].endsWith('module.js')) {
  const args = parseArgs(process.argv);
  try {
    doSomething({ input: args.input, output: args.output, flag: args.flag });
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}
```

**Clave:** `process.argv[1]` contiene la ruta del script ejecutado. Si termina en el nombre del archivo, estamos en modo standalone.

## Patrón 2: CLI principal con Commander

```js
// src/index.js
import { Command } from 'commander';
import { doSomething } from './module-a.js';
import { doAnother } from './module-b.js';

const program = new Command();

program
  .name('my-cli')
  .description('Descripción corta')
  .version('0.1.0');

// Subcomando A
program
  .command('subcommand-a')
  .description('Qué hace')
  .requiredOption('--input <file>', 'Descripción')
  .requiredOption('--output <file>', 'Descripción')
  .option('--flag <value>', 'Descripción', 'default')
  .action((options) => {
    try {
      doSomething({
        input: options.input,
        output: options.output,
        flag: options.flag,
      });
    } catch (err) {
      console.error(`Error: ${err.message}`);
      process.exit(1);
    }
  });

// Subcomando B (mismo patrón)
// ...

program.parse(process.argv);
```

## Patrón 3: package.json scripts

```json
{
  "name": "preprocessing",
  "type": "module",
  "scripts": {
    "start": "node src/index.js",
    "subcommand-a": "node src/index.js subcommand-a",
    "subcommand-b": "node src/index.js subcommand-b"
  }
}
```

Uso: `npm run subcommand-a -- --input file.nc --output file.bin`

## Validación de argumentos

- Commander `requiredOption()` para obligatorios
- Commander `option()` con valor default para opcionales
- Validar rangos manualmente (lat/lon, tamaños, etc.)
- Verificar existencia de archivos con `existsSync()`
- Parsear tipos manualmente (parseFloat, parseInt) — Commander no lo hace por ti

## Pitfalls

### No reasignar process.argv

El patrón antiguo de reasignar `process.argv` dentro de un action de commander y luego llamar a un módulo que lee `process.argv` es **frágil y anti-patrón**. En su lugar:

- ✅ **Correcto:** módulo exporta función, commander pasa opciones como objeto
- ❌ **Incorrecto:** módulo lee `process.argv` directamente desde el action

### No confundir entry point con import

El check `process.argv[1].endsWith('module.js')` diferencia entre:
- `node src/module.js` → ejecuta el bloque standalone
- `import { doSomething } from './module.js'` → solo exporta, no ejecuta

### ESM es obligatorio

`"type": "module"` en package.json. Usar `import/export`, no `require/module.exports`. Para `__dirname` en ESM:
```js
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const __dirname = dirname(fileURLToPath(import.meta.url));
```

### Commander no parsea tipos

`--lat-min 43.2` llega como string `"43.2"`. Hacer `parseFloat()` en el action.

### No usar commander para scripts standalone simples

Si un script solo se ejecuta directamente (nunca como subcomando de index.js), no necesita commander. Usa un parser de args mínimo (split `--flag valor`). Commander solo en `index.js`.

## Verificación

1. `npm run <subcommand> -- --help` → muestra help del subcomando
2. `npm run <subcommand> -- --input test/sample.csv --output /tmp/out.json --label "Test"` → ejecuta correctamente
3. `node src/module.js --help` → si tiene standalone, muestra su help
4. `node src/index.js --help` → muestra todos los subcomandos

## Referencias

- `references/cli-patterns/wavethree-preprocessing.md` — Caso de uso real: WaveThree preprocessing CLI con GEBCO extract y scenario generator

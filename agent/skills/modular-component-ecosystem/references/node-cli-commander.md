# Node CLI Commander.js Patterns

## Cuándo usar

Necesitas construir una CLI en Node.js con Commander.js que funcione como módulo dual (importable + executable).

## Patrón de doble export

```javascript
// commands/generate.js
import { Command } from 'commander';

export function createGenerateCommand() {
  return new Command('generate')
    .description('Generate new module')
    .option('-n, --name <name>', 'module name')
    .option('-t, --type <type>', 'module type')
    .action((options) => {
      // implementation
    });
}
```

```javascript
// CLI entry point
import { createGenerateCommand } from './commands/generate.js';

// Expose for import
export { createGenerateCommand };

// Auto-run if executed directly
if (process.argv[1] && process.argv[1].endsWith('generate')) {
  createGenerateCommand().parseAsync(process.argv);
}
```

## Reglas

1. Cada subcomando es un archivo en `commands/` con una función `createXxxCommand()`
2. El archivo principal importa todos y los añade al CLI root
3. Exportar las funciones para que otros módulos puedan importarlas
4. `if (process.argv[1]...)` para auto-ejecución cuando se corre directamente
5. ESM: `import { createGenerateCommand } from './commands/generate.js'`
6. CJS: `const { createGenerateCommand } = require('./commands/generate')`

## Pitfalls

- ❌ No mezclar ESM y CJS sin `createRequire`
- ❌ No usar `commander` v7+ con `commander` v8+ syntax — `action()` vs callback
- ❌ No olvidar `export` de las funciones — si solo se auto-ejecutan, no son reutilizables

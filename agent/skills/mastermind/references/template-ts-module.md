# Template de Módulo TypeScript — Adela Ecosystem

Estructura estandarizada para crear módulos TypeScript en el ecosistema Adela. Usado con éxito en 10 módulos (~300 tests).

## Estructura de archivos

```
modulo/
├── README.md              # Quick start + API + "Integración con otros Adela"
├── package.json           # name: "adela-*", version: "1.0.0", type: "module"
├── tsconfig.json          # Strict mode, ES2022, Node16
├── src/
│   ├── index.ts           # Barrel export
│   ├── ...                # Módulos funcionales
│   └── types.ts           # Interfaces y tipos
├── tests/
│   └── *.test.ts          # Tests con tsx --test
└── dist/                  # Compilado (gitignored)
```

## package.json

```json
{
  "name": "adela-<nombre>",
  "version": "1.0.0",
  "description": "<descripción corta> — parte del ecosistema Adela.",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsc",
    "test": "tsx --test tests/*.test.ts",
    "clean": "rm -rf dist *.tsbuildinfo"
  },
  "dependencies": {},
  "devDependencies": {
    "@types/node": "^22.0.0",
    "tsx": "^4.19.0",
    "typescript": "^5.7.0"
  },
  "keywords": ["adela", "<dominio>"],
  "license": "MIT"
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

## README.md

```markdown
# Adela_<nombre>

<descripción> — parte del ecosistema Adela.

---

## Instalación

\`\`\`bash
npm install adela-<nombre>
\`\`\`

## Uso rápido

\`\`\`typescript
import { ... } from 'adela-<nombre>'
\`\`\`

## API

### `<Función principal>`

```typescript
function nombre( ... ): Promise<Resultado>
```

## Integración con otros Adela

- **Adela_db:** almacenamiento persistente de datos
- **Adela_env:** variables de configuración
- **Adela_http:** cliente HTTP robusto

Hecho con ❤️ por David Antizar
```

## .gitignore

```
node_modules/
dist/
data/
```

## Reglas

1. **Zero dependencias runtime** siempre que sea posible (auth, export, db pueden tener deps justificadas)
2. **TODO en castellano** — nombres, comentarios, errores, README
3. **TypeScript strict** — siempre `"strict": true` en tsconfig
4. **Mínimo 15 tests** por módulo
5. **Build y test** deben pasar antes de push
6. **dist/ se compila**, NO se versiona (en .gitignore)
7. **README** debe incluir sección "Integración con otros Adela"
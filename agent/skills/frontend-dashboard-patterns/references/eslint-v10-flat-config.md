# ESLint v10 Flat Config - Referencia

## Problema

ESLint v10 (lanzado 2025) elimina completamente el soporte de `.eslintrc.json` (legacy config). Los globals definidos ahí son ignorados → falsos `no-undef` para bibliotecas CDN (`Plotly`, `Vue`), namespaces (`SEF`, `C`).

## Síntomas en CI

```
js/app.js#L10: 'Vue' is not defined. (no-undef)
js/app.js#L571: 'C' is not defined. (no-undef)
js/charts.js#L43: 'Plotly' is not defined. (no-undef)
```

## Solución: `eslint.config.js` (flat config)

### Estructura básica

```javascript
import globals from 'globals';

export default [
    {
        files: ['js/**/*.js', 'tests/**/*.js'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'module',
            globals: {
                ...globals.browser,
                ...globals.es2021,
                ...globals.node,
                // Globales CDN / namespace del proyecto
                SEF: 'readonly',
                Vue: 'readonly',
                Plotly: 'readonly',
                C: 'readonly',
            },
        },
        rules: {
            'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
            'no-console': 'off',
            eqeqeq: ['error', 'always'],
            semi: ['error', 'always'],
            quotes: ['error', 'single'],
        },
    },
    {
        ignores: ['node_modules/', 'dist/', '*.min.js'],
    },
];
```

### Reglas que vienen de `eslint:recommended`

No es necesario declarar explícitamente reglas que ya vienen en `eslint:recommended`:
- `no-undef` → error por defecto
- `no-redeclare` → error por defecto
- `no-empty` → warn por defecto
- `no-extra-semi` → warn por defecto
- `no-constant-condition` → warn por defecto

### Reglas que NO vienen de `eslint:recommended`

Si no se declaran explícitamente, no se aplican:
- `no-shadow` → no se aplica
- `no-var` → no se aplica
- `prefer-const` → no se aplica

### Migración desde `.eslintrc.json`

1. Eliminar `.eslintrc.json` (o renombrarlo a `.eslintrc.json.old`)
2. Crear `eslint.config.js` con el contenido de arriba
3. Asegurar que `globals` está en `devDependencies` o instalar: `npm install --save-dev globals`
4. Verificar que `package.json` tiene `"type": "module"` (necesario para ESM)

### Package.json

```json
{
  "type": "module",
  "scripts": {
    "lint": "eslint js/ tests/"
  },
  "devDependencies": {
    "eslint": "^10.4.1",
    "globals": "^17.6.0"
  }
}
```

### DEBUG: Verificar que ESLint usa flat config

```bash
npx eslint --print-config js/app.js | head -5
# Si falla o no muestra globals → no está usando flat config correctamente
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'Vue' is not defined` | Global no declarado en flat config | Añadir `Vue: 'readonly'` a globals |
| `'Plotly' is not defined` | Global no declarado en flat config | Añadir `Plotly: 'readonly'` a globals |
| `'C' is not defined` | Variable local esperada como global | Añadir `C: 'readonly'` a globals, o usar `SEF.COLORES` directamente |
| `'X' is defined but never used` | Variable declarada pero no referenciada | Eliminarla, o prefijar con `_` si es argumento de función |
| `Module is not defined` | `eslint.config.js` sin `"type": "module"` en package.json | Añadir `"type": "module"` o renombrar a `.mjs` |

# Vite + GitHub Pages: Deployment Pitfalls

## Cuándo consultar

Un proyecto Vite no carga en GitHub Pages: assets 404, JS no ejecuta, CSS no aplica, pantalla de carga perpetua.

## Diagnóstico rápido

| Síntoma | Causa probable |
|---------|---------------|
| Assets (JS/CSS) devuelven 404 en consola | `base` incorrecto en `vite.config.js` |
| JS module no se ejecuta, sin errores en consola | `crossorigin` en `<script>` bloquea el módulo |
| CSS no aplica estilos (position:static en vez de fixed) | `crossorigin` en `<link>` impide carga |
| Pantalla de carga se queda para siempre | El módulo JS entero falló al ejecutarse |
| Source map errors en consola | Vite genera .map; GitHub Pages los sirve pero pueden dar warning |

## Pitfall 1: `base` path incorrecto

GitHub Pages sirve project sites bajo `https://user.github.io/repo/`. Vite por defecto usa `base: '/'` que resuelve a `https://user.github.io/` — sin `/repo/`.

**Fix en `vite.config.js`:**
```js
export default defineConfig({
  base: '/NapMaps/',           // ← debe coincidir con repo name
  build: {
    outDir: 'dist',
  }
})
```

**Verificar:** el HTML build debe tener rutas como:
```html
<script type="module" src="/NapMaps/assets/index-abc123.js"></script>
<link rel="stylesheet" href="/NapMaps/assets/index-abc123.css">
```

## Pitfall 2: `crossorigin` rompe módulos ES

Vite añade automáticamente `crossorigin` a `<script type="module">` y `<link rel="stylesheet">`. En GitHub Pages esto causa que el navegador haga la petición en modo CORS, y aunque GitHub Pages devuelve `access-control-allow-origin: *`, el script puede fallar silenciosamente (error vacío en consola).

**Fix:** eliminar `crossorigin` del HTML build:
```bash
sed -i 's/ crossorigin//g' dist/index.html
```

Después de esto, los `<script>` y `<link>` deben verse así:
```html
<script type="module" src="/NapMaps/assets/index-abc123.js"></script>
<link rel="stylesheet" href="/NapMaps/assets/index-abc123.css">
```

## Pitfall 3: JavaScript con sintaxis rota → todo el módulo falla

Si el JS fuente tiene un string sin cerrar (una comilla simple `'` sin su par), el **módulo entero** falla al ejecutarse. MapLibre no se inicializa, la pantalla de carga nunca desaparece.

**Síntomas:**
- `window.state` es `undefined`
- `window.CONFIG` es `undefined`
- No hay canvas de MapLibre en el DOM
- Pantalla de carga ("Inicializando motor WebGL 3D …") permanente

**Causa típica:** Stadia Maps URLs con template literals rotos:
```js
// MAL — string con comilla simple sin cerrar:
uri: 'https://tiles.stadiamaps.com/styles/alidade_smooth.json?api_key=***      // ← SyntaxError

// BIEN — usar backtick (template literal):
uri: `https://tiles.stadiamaps.com/styles/alidade_smooth.json?api_key=API_KEY`,
```

## Pitfall 4: GitHub Pages requiere repo público

En plan free de GitHub, Pages solo funciona con repos públicos. Si el repo es privado, la API devuelve:
```
"Your current plan does not support GitHub Pages for this repository."
```

**Fix:** hacer el repo público o usar un plan de pago.

## Deploy workflow (GitHub Pages manual)

```bash
# 1. Build con base correcta
npm run build

# 2. Quitar crossorigin
sed -i 's/ crossorigin//g' dist/index.html

# 3. Preparar branch gh-pages (desde directorio limpio)
cd /tmp
rm -rf gh-deploy
mkdir gh-deploy
cd gh-deploy
git init
cp -r /path/to/proyecto/dist/* .
git add -A
git commit -m "deploy: NapMaps"

# 4. Pushear a GitHub
git remote add origin https://github.com/USER/REPO.git
git push origin master:gh-pages --force

# 5. Activar Pages (una vez)
# API: POST /repos/USER/REPO/pages -d '{"source":{"branch":"gh-pages","path":"/"}}'

# 6. Esperar 30-60s para que GitHub Pages compile
sleep 45
curl -sI "https://user.github.io/REPO/"
```
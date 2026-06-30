# Caso de Estudio: Incidente MasterFit v3 — Refactor que rompió el dashboard

## Timeline

1. **Audit original**: Usuario pide auditoría de buenas prácticas del proyecto dieta (MasterFit v3)
2. **Extraer JS a archivo separado**: Se extraen ~1500 líneas de JS inline a `dashboard.js`
3. **var→const/let + arrow functions**: Se moderniza el código (248 const, 21 let, 121 arrow fns)
4. **Deploy a NaN**: Se sube via GitHub API
5. **Dashboard roto**: "Error cargando datos" — los gráficos no cargan
6. **Causa #1 descubierta**: CDN de Chart.js y Three.js no se copiaron al reestructurar
7. **Fix #1**: Se restauran los CDN en `<head>`
8. **Dashboard sigue roto**: Los gráficos siguen vacíos
9. **Causa #2 descubierta**: Script en `<head>` se ejecuta antes del DOM → `getElementById` retorna `null`
10. **Fix #2**: Se mueve `<script>` al final de `</body>`
11. **Dashboard sigue roto**: Aún "Error cargando datos"
12. **Causa #3 descubierta**: Variables acumuladoras declaradas como `const` usan `+=` → `TypeError`
13. **Fix #3**: Se cambian 7 variables de `const` a `let`
14. **Dashboard parcialmente funciona**: KPIs muestran datos pero gráficos vacíos
15. **Causa #4 descubierta**: Cloudflare cachea JS por 4 horas → navegador ejecuta versión vieja
16. **Fix #4**: Se vuelve a JS inline en HTML (cero dependencia de cache)
17. **Dashboard funciona**: Todos los datos visibles ✅
18. **Tab Progreso roto**: No carga el modelo 3D
19. **Causa #5 descubierta**: Arrow function con `this.getAttribute()` — `this` es `window`, no el tab
20. **Fix #5**: `this.getAttribute` → `tab.getAttribute` (variable del closure)
21. **Todo funciona** ✅

## Causas raíz

| # | Causa | Síntoma | Fix |
|---|-------|---------|-----|
| 1 | CDN olvidados | "Error cargando datos" | Restaurar `<script src="cdn...">` |
| 2 | Script en `<head>` | `getElementById` retorna `null` | Mover a `</body>` |
| 3 | `const` con `+=` | `TypeError: Assignment to constant` | Cambiar a `let` |
| 4 | Cloudflare cache | curl OK pero browser ejecuta viejo | JS inline o `?v=timestamp` |
| 5 | Arrow function `this` | Tab no carga, `undefined` | Usar variable del closure |

## Lecciones clave

### 1. Inventario antes de reestructurar
El error #1 se habría evitado con un simple `grep 'script.*src' index.html` antes de mover el JS.

### 2. Un cambio a la vez
Se hicieron múltiples cambios en un commit (extraer JS + var→const/let + arrow functions + element cache). Si se hubieran hecho por separado, el error #1 se habría detectado inmediatamente.

### 3. Verificar con curl PRIMERO
El error #4 (cache) se detectó porque curl mostraba el HTML nuevo pero el browser ejecutaba el viejo. Siempre curl antes de browser.

### 4. `this` en arrow functions es un bug silencioso
El error #5 no produce error en consola — simplemente `this.getAttribute` retorna `undefined` y el tab no carga. Es uno de los bugs más difíciles de detectar porque no hay stack trace.

### 5. `.catch()` engañoso
El `.catch()` de `loadData()` capturaba errores de RENDERIZADO, no solo de red. Esto hizo que el mensaje "Error cargando datos" apareciera incluso cuando la API respondía bien. Solución: separar catch de red y catch de render.

## Patrón de debug para "dashboard roto"

```
1. curl -s URL | head -20          → ¿El HTML sirve?
2. curl -s URL/data/database.json  → ¿La API responde?
3. node --check script.js          → ¿Syntax OK?
4. grep 'Chart\|THREE' index.html  → ¿CDN presentes?
5. browser_console()               → ¿Errores JS?
6. browser_vision()                → ¿Qué se ve visualmente?
7. Buscar this. en arrow functions → ¿Bug de contexto?
```

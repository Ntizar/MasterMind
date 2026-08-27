# Patrón Closure Onclick Roto — Detección y Fix

## Problema

Funciones JS que devuelven closures (funciones dentro de funciones) se usan mal en HTML inline:

```html
<!-- ❌ ROTO: la función devuelta no recibe 'btn' -->
<button onclick="checkFillIn(['respuesta'])()">Comprobar</button>
```

`checkFillIn(['respuesta'])` devuelve `function(btn) { ... }`. El `onclick="...()()"` la llama con **cero argumentos** → `btn` es `undefined` → `btn.closest('.exercise')` falla con TypeError.

## Closures comunes en HTML educativos

| Función | Devuelve | Recibe | Signatura |
|---------|----------|--------|-----------|
| `checkFillIn(correctAnswers)` | `function(btn)` | `btn` | `onclick="checkFillIn(['x'])(this)"` |
| `checkCompleta(correct)` | `function(btn)` | `btn` | `onclick="checkCompleta('x')(this)"` |
| `checkProblem(correct)` | `function(btn)` | `btn` | `onclick="checkProblem('x')(this)"` |

## Detección

```bash
# Buscar patrones ()() — siempre roto
grep -nP '\)\s*\(\)\s*"' file.html
# Buscar patrones correctos
grep -nP '\)\s*\(this\)\s*"' file.html
```

## Fix

```html
<!-- ❌ ROTO -->
onclick="checkFillIn(['paralela'])()"

<!-- ✅ CORRECTO -->
onclick="checkFillIn(['paralela'])(this)"
```

El `(this)` pasa el botón clicado como argumento a la función devuelta.

## Regla

**Siempre verificar** `onclick` con closure pattern ANTES de cualquier mejora. Si el archivo tiene `checkFillIn`, `checkCompleta`, o cualquier función que devuelve otra función, revisar TODOS los onclicks con el patrón `)(` para asegurarse de que pasan `(this)`.

## Ejemplos reales

- `b07-04-verdadera-magnitud.html`: Ex 4 y Ex 5 con `checkFillIn(['paralela'])()` y `checkFillIn(['planta'])()` → ambos rotos
- `b07-03-interseccion-recta-recta.html`: Mismo patrón en ejercicios de completar

# Single-File Interactive App Audit

Procedimiento para auditar aplicaciones web **monolíticas** (un solo archivo HTML con CSS+JS inline): visores interactivos, dashboards vanilla, herramientas de mapa, etc.

## Cuándo usar

- Un solo archivo HTML con CSS `<style>` + JS `<script>` inline
- El usuario reporta "no funciona" o "no hace lo que debería"
- Visores interactivos (Leaflet, Three.js, D3, etc.)
- Herramientas webapp con lógica JS compleja

## Diferencia con `audit-html-project` (multi-file)

| | Multi-file educativo | Single-file interactivo |
|---|---|---|
| Alcance | 10+ archivos | 1 archivo |
| Enfoque | grep batch, enlaces rotos | Lectura línea a línea, lógica JS |
| Errores típicos | href="#", navegación rota | Variables no declaradas, comillas rotas |

## Pasos

### 1. Lectura completa del archivo

Leer TODO el archivo con `read_file`. No usar grep para este tipo de archivos — la lógica está en JS inline y necesita contexto.

### 2. Análisis de variables y scope

Buscar variables usadas antes de declararse. `let` tiene hoisting de bloque: si se usa dentro de una función definida antes pero llamada después, funciona pero es anti-pattern. Declarar arriba con las demás variables globales.

### 3. Análisis de strings HTML generados dinámicamente

Buscar `innerHTML +=` y `htmlContent +=` que contengan atributos `onclick=` con comillas. Las comillas simples dentro de un string JS con comillas simples rompen el output HTML.

**Patrón roto:** `onclick="this.parentElement.classList.toggle('open')"` dentro de `'...'`
**Fix:** Escapar con `\'open\'` o usar template literals (backticks) para el string externo.

### 4. Análisis de lecturas duplicadas

Buscar el mismo archivo/endpoint leído múltiples veces en la misma función. Unificar en una sola lectura.

### 5. Análisis de limpieza de estado entre operaciones

Verificar que variables globales se limpian o no se solapan entre operaciones (ej: múltiples ZIPs GTFS).

### 6. Análisis de UX

Verificar:
- ¿Cierra panel con Escape? → Añadir `keydown` listener
- ¿Debounce en búsqueda? → Añadir `input` listener con `setTimeout`
- ¿Rate limiting de APIs externas? → Nominatim: 1 req/seg

### 7. Verificación post-fix

- No quedan referencias a variables eliminadas
- Balance de comillas en strings HTML generados
- Variables declaradas antes de su primer uso

## Checklist de errores comunes

| Error | Dónde buscar | Fix |
|-------|-------------|-----|
| Variable usada antes de declarar | `let X` vs `X[` | Mover al scope global |
| Comillas rotas en onclick | `htmlContent +=` con `onclick=` | Escapar o usar backticks |
| Lectura duplicada de datos | Mismo archivo 2x | Unificar |
| Estado global no limpio | Variables acumulativas | Limpiar o usar scope local |
| Sin Escape para cerrar paneles | Paneles fijos | Añadir `keydown` |
| Sin debounce en búsqueda | Input sin listener | Defer 500ms |

## Ejemplo real: GTFSSpain visor (2026-06-23)

1. `tripRouteMap` declarado en línea 1085, usado en 734 → movido a línea 523
2. `classList.toggle('open')` comillas rotas → escapado con `\'open\'`
3. `stop_times.txt` leído 2x → unificado
4. Sin Escape para cerrar panel → añadido `keydown`
5. Sin debounce en geocodificación → añadido `input` listener 500ms

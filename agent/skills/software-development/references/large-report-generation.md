# Generación de Informes Grandes (60-80 páginas)

## Patrón

Cuando se necesita generar un informe HTML/PDF largo (60+ páginas, 22+ capítulos, 3000+ líneas de JS):

### 1. Delegar la generación a un subagente
Usar `delegate_task` con contexto detallado: estructura de datos disponible, estructura del informe, requisitos de estilo. El subagente genera el archivo completo.

**Ventaja:** El subagente tiene contexto fresco y puede generar 3000+ líneas sin agotar el contexto de la sesión padre.

### 2. Integrar en el sistema de export
- Añadir `import { generarInformeCompleto } from './report.js'` en export.js
- Reemplazar `exportPDF()` para llamar a la nueva función
- Mantener el código legacy comentado por si se necesita rollback

### 3. Fix iterativo de bugs
Los archivos grandes generados por subagentes suelen tener:
- **Variables no definidas** en template literals (ej: `${lat}` cuando debería ser `${centro.lat}`)
- **Parámetros no desestructurados** (ej: usar `manana` en vez de `turnos.manana`)
- **Imports circulares** o dependencias no declaradas

**Flujo de fix:**
```
navegar → browser_console → importar módulo → llamar función → capturar error → fix → recargar → repetir
```

**Verificación:** el archivo debe pasar `node --input-type=module -e "import { fn } from './js/modulo.js'"` sin SyntaxError (el `window is not defined` de Node es esperado y OK).

### 4. CSS del informe
El informe HTML autocontenido debe incluir:
- `@page` rules para A4 print
- `page-break-before: always` en cada capítulo (clase `.chapter`)
- Footer en cada página
- Colores: azul `#2563eb` headers, naranja `#f97316` accents
- Tablas con `nth-child(even)` alternado

### Pitfalls
- **Template literals con variables no declaradas** — el subagente genera `${variable}` pero la variable no está en la función scope. Fix: añadir `const variable = objeto.propiedad || default` al inicio de cada función. Verificar con: `grep -n '\${' js/report.js | grep -v 'const\|let\|var'`.
- **Unreachable code con `const` duplicados** — si añades `return` antes de código legacy que declara `const blob`, el parser falla aunque el código sea unreachable. JavaScript valida `const/let` en todo el scope sin importar el flujo de control. Fix: eliminar el código legacy o envolver en bloque `{ }`.
- **CSS `page-break-before` vs `page-break-after`** — `page-break-before: always` en `.chapter` es correcto para capítulos. `page-break-after: always` es para secciones dentro de un capítulo.
- **Browser ES module cache** — `python3 -m http.server` no establece Cache-Control headers. Los módulos ES se cachean por URL exacta. SIEMPRE usar `?v=N` en imports: `import { fn } from './js/modulo.js?v=2'`. Verificar con `fetch('./js/modulo.js?t=' + Date.now())`.
- **Variables undefined en template literals de subagentes** — patrón común: `${lat}` cuando debería ser `${centro.lat}`. Fix iterativo: browser_console → importar módulo → llamar función → capturar error → fix → recargar.

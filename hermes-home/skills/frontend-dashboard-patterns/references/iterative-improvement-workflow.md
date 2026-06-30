# Iterative Improvement Workflow — Web Apps con Backend

## Cuándo usar

- Usuario quiere mejorar un proyecto web existente (dashboard, SPA, app)
- Hay un backlog de mejoras priorizadas
- El proyecto tiene stack: HTML + JS/CSS + backend (Express/Node)
- Deploy en NaN.builders o similar

## Flujo de Mejora Iterativa

### Paso 1: Análisis del estado actual

1. Leer los archivos principales: `dashboard.html`, `server.js`, `database.json` (o data layer)
2. Verificar sintaxis: `node -c server.js`
3. Verificar tamaño del HTML (si >150KB, riesgo de problemas en NaN)
4. Buscar bugs conocidos: endpoint mismatches, arrays invertidos, paréntesis desbalanceados

### Paso 2: Identificar la siguiente mejora

Usar la lista de prioridades del proyecto:
1. Bugs críticos (página en blanco, botones rotos)
2. Mejoras UX (toasts, modo oscuro, feedback visual)
3. Features nuevas (gráficos, exportación, offline)
4. Optimizaciones (rendimiento, accesibilidad, responsive)

### Paso 3: Implementar la mejora

**Reglas:**
- NUNCA borrar código existente, solo añadir o modificar
- Mantener estilo visual del proyecto (Aurora, colores, glass)
- NUNCA inventar datos en dashboards
- Si se añade algo visual, usar componentes del design system del proyecto
- NUNCA usar `buildSummary()` recursiva (causa OOM en NaN)
- NUNCA usar `const charts` en frontend → `var charts = window.charts = {}`
- Mantener motor existente (Three.js, Chart.js) y modificar solo la lógica

### Paso 4: Verificar

1. `node -c server.js` — sintaxis del backend
2. Contar paréntesis en el `<script>` del HTML (diff debe ser 0)
3. Verificar que los nuevos elementos tienen IDs únicos
4. Verificar que los endpoints del backend coinciden con los del frontend

### Paso 5: Commit y push

```bash
cd /root/workspace/<proyecto>
git add .
git commit -m "<proyecto> v<X.Y>: <descripción corta de la mejora>"
git push origin main
```

## Patrones de Implementación

### Patrón A: Añadir nueva sección en una tab existente

1. Añadir HTML dentro del `tab-content` correspondiente
2. Añadir función JS que renderiza los datos
3. Llamar la función desde `renderDashboard()` o desde el lazy-load de la tab
4. Añadir CSS si es necesario

### Patrón B: Añadir nueva funcionalidad con backend

1. Añadir endpoint en `server.js`
2. Añadir función frontend que llama al endpoint
3. Añadir UI para interactuar con el endpoint
4. Verificar que el endpoint funciona con `curl`

### Patrón C: Modificar funcionalidad existente

1. Identificar el código actual con `search_files`
2. Modificar solo la lógica necesaria
3. Mantener compatibilidad con datos existentes
4. Verificar que no se rompen otras funcionalidades

## Prioridades típicas por proyecto

### Dashboard de datos (ESIOS, Mastermind, etc.)
1. Bug fix: página en blanco / error de sintaxis
2. Toast notifications para feedback
3. Gráficos comparativos / KPIs
4. Exportación de datos
5. Modo offline

### App de dieta/fitness (MasterFit)
1. Bug fix: endpoints mismatch, botones rotos
2. Toast notifications
3. Gráfico de macros vs objetivo
4. Recordatorio de agua
5. Exportación CSV
6. Modo offline
7. Sistema de logros

## Pitfalls

- **No implementar múltiples mejoras en un solo commit** — cada mejora debe ser atómica
- **No saltarse la verificación de sintaxis** — un paréntesis desbalanceado rompe todo el JS
- **No asumir que un endpoint existe** — siempre verificar con `grep` en server.js
- **No modificar la estructura de database.json** sin actualizar todos los puntos de lectura
- **No añadir scripts externos** sin verificar que el CDN es fiable
- **El browser tool de Hermes tiene cache agresivo** — si los cambios no se ven, navegar con `?t=<timestamp>`

## ⚠️ CRÍTICO: No Romper al Mejorar (Lección DataHub 2026-06-30)

**Señal de usuario:** *"creo que no estás planteando el crecimiento de la herramienta sin romper cosas"*

Cuando el usuario pide "mejorar" un dashboard existente, el instinto es hacer todo junto: quitar código, añadir APIs, cambiar diseño. **Esto rompe todo.** El flujo seguro es:

### 1. DIAGNÓSTICO ANTES DE TOCAR NADA
```bash
# Verificar estado actual
curl -s "https://url-del-proyecto/" > /tmp/before.html
# Contar líneas, verificar APIs
curl -s "https://api-ejemplo.com/data" -H "Accept: application/json" | head -5
# Verificar sintaxis JS actual
node --check extracted.js  # o buscar con python
```

### 2. CAMBIOS INCREMENTALES (1 cosa a la vez)
- **Primero:** solo fix de bugs (APIs rotas)
- **Segundo:** solo limpieza (quitar código muerto)
- **Tercero:** solo features nuevas
- **NUNCA** hacer los 3 en el mismo commit

### 3. VERIFICAR DESPUÉS DE CADA CAMBIO
```bash
# Después de cada patch:
python3 -c "
with open('index.html') as f:
    c = f.read()
opens = c.count('{'); closes = c.count('}')
print(f'Braces: {opens} open, {closes} close, diff={opens-closes}')
"
# Si diff != 0, HAY UN ERROR — parar y arreglar
```

### Patrón de error común: Braces huérfanos al eliminar código

Cuando eliminas un bloque de JS (como una función + event listeners), si no eliminas TODOS los `});` de cierre, el script entero deja de ejecutarse silenciosamente — sin errores en consola, solo KPIs vacíos.

```javascript
// ANTES (funciona)
searchInput.addEventListener('focus', () => {  // ← abre {
    if (searchInput.value.length >= 2) {       // ← abre {
        searchResults.classList.add('show');    // ← cierra }
    }                                            // ← cierra }
});                                              // ← cierra addEventListener

// DESPUÉS (ROTO — quedó un }); huérfano)
// (código eliminado)
    });  // ← ¡ESTE SE QUEDÓ! ← Error silencioso

// VERIFICACIÓN: buscar }; huérfanos después de edits
grep -n '^\s*});' index.html | tail -5
```

## Referencias

- `frontend-dashboard-patterns` — Patrones generales de dashboards frontend
- `references/masterfit-fullstack-audit.md` — Auditoría específica de MasterFit
- `micro-crons-pipeline` — Pipeline de mejoras iterativas con cron jobs

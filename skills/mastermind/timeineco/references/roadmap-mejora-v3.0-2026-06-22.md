# Plan de Mejora — TimeIneco al Siguiente Nivel
> Sesión: 2026-06-22 | Estado: Pendiente de aprobación

## Contexto
David tiene dos repos: TimeIneco (original, desplegado) y TimeIneco2 (fork con mejoras).
Quiere unificar, arreglar APIs, reducir ruido y añadir transparencia de fuentes.

## Diagnóstico

### TimeIneco (original) — 5.045 líneas
- ✅ ORS_API_KEY + NAP_API_KEY en .env de NaN
- ✅ Server con proxy ORS, NAP, Nominatim
- ✅ Motor isocronas real + simulación v2.1
- ❌ Solo datos de Madrid (GTFS cache)
- ❌ Sin datos población real INE
- ❌ Sin documentación de fuentes

### TimeIneco2 (fork) — 6.984 líneas
- ✅ 6 ciudades GTFS sintético
- ✅ Población real INE 2025 (299 CPs)
- ✅ Datos económicos enriquecidos
- ✅ Dashboard interactivo
- ✅ Geocodificación mejorada
- ❌ Sin .env (no tiene API keys)
- ❌ Rate limiting bug (caracteres chinos)
- ❌ Datos demográficos hardcodeados en dashboard

## Ejes de Mejora

### Eje 1: Unificar en un solo proyecto
Importar de TimeIneco2:
- `poblacion-cp.json` + READMEs
- `demographics.js` v2 (ranking, alertas, población INE)
- `shp.js` v2 (multi-formato, 8 campos)
- `utils.js` v2 (geocodificación mejorada)
- NO importar dashboard.html (ruido)

### Eje 2: APIs reales
- ORS: Verificar header Authorization
- NAP: Testear con dataset IDs reales, añadir cache localStorage
- GTFS: Priorizar NAP API > cache local > sintético

### Eje 3: Metodología y transparencia
- Sección "Fuentes y Metodología" en DOCX
- Tooltips ℹ️ en KPIs con fuente del dato
- README por dataset en /data/

### Eje 4: UI más limpia
- Sidebar simplificada (dirección + modos + tiempo + 1 botón)
- 1 botón de export principal (DOCX), resto links discretos
- Panel NAP colapsable
- Sin gráfico barras inline, sin tabla comparativa HTML

### Eje 5: Fix ORS concreto
- Verificar `Authorization: <key>` vs `Bearer <key>`
- Testear proxy con llamada real
- Añadir NAP check al /healthz

## Prioridades
1. Fix ORS + testear proxy (ALTO, bajo esfuerzo)
2. Unificar datos TimeIneco2 → TimeIneco (ALTO, medio esfuerzo)
3. Añadir sección "Fuentes" al DOCX (ALTO, bajo esfuerzo)
4. Tooltips de fuente en KPIs (MEDIO, bajo esfuerzo)
5. Limpiar UI (MEDIO, medio esfuerzo)
6. Integrar NAP real (MEDIO, medio esfuerzo)
7. Simplificar exports (BAJO, bajo esfuerzo)

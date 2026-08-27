# CDN MIME Type, AbortController y UI Progressivo — Caso TimeIneco (Jun 2026)

## 1. CDN MIME Type — Pitfall `application/node`

**Problema:** jsdelivr sirve archivos `.cjs` con `Content-Type: application/node`. Los navegadores modernos bloquean la descarga porque no es un MIME JavaScript executable (`text/javascript`). El script simplemente no carga, y la variable global (`window.docx`) queda `undefined`.

**Síntomas:**
- Página carga pero funcionalidad de la librería no funciona
- Sin errores en consola (el bloqueo es silencioso para `<script src="...">`)
- `console.log(window.libreria)` → `undefined`
- Red muestra HTTP 200 pero con `Content-Type: application/node`

**Solución — unpkg:**

```html
<!-- ❌ jsdelivr .cjs → application/node (bloqueado) -->
<script src="https://cdn.jsdelivr.net/npm/docx@9.7.1/dist/index.umd.cjs"></script>

<!-- ✅ unpkg .cjs → text/javascript (correcto) -->
<script src="https://unpkg.com/docx@9.7.1/dist/index.umd.cjs"></script>
```

**Verificación con curl:**
```bash
curl -sI "https://cdn.jsdelivr.net/npm/docx@9.7.1/dist/index.umd.cjs" | grep -i content-type
# application/node

curl -sI "https://unpkg.com/docx@9.7.1/dist/index.umd.cjs" | grep -i content-type
# text/javascript
```

**Pitfalls adicionales:**
1. jsdelivr + ESM (`?module`) funciona bien con `.js`. El problema es solo `.cjs`.
2. Siempre especificar versión exacta (`docx@9.7.1`), no `@latest`.
3. Verificación defensiva: `if (typeof window.docx === 'undefined') { alert('No cargada'); return; }`
4. SPA fallback en servidores: si el servidor sirve index.html para todo, un path de CDN resuelto localmente se serviría como HTML.

---

## 2. AbortController para Timeout en Fetch

**Problema:** APIs externas (CityBikes, etc.) pueden tardar 10-30s o no responder, bloqueando la UI.

**Patrón genérico:**
```javascript
async function fetchWithTimeout(url, options = {}, timeoutMs = 8000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timeoutId);
    return response;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError')
      throw new Error(`Timeout tras ${timeoutMs}ms: ${url}`);
    throw err;
  }
}
```

**Propagación de signal:** Cuando una función wrapper llama a otra interna, pasar `signal` como parámetro:
```javascript
// ❌ No propaga
async function fetchAllNetworks() { return fetch(API_URL); }

// ✅ Propaga
async function fetchAllNetworks(signal) { return fetch(API_URL, { signal }); }
```

**Timeout silencioso para fuentes no esenciales:**
```javascript
async function cargarFuenteSecundaria() {
  try {
    const data = await fetchWithTimeout(API_URL, {}, 8000);
    renderizarDatos(data);
  } catch (err) {
    if (err.name === 'AbortError') {
      console.warn('Timeout — saltando');  // Silencioso
      return;
    }
    mostrarError(err);
  }
}
```

**Cuándo usar:**
- APIs externas gratuitas (sin SLA)
- Fuentes de datos no críticas
- Cuando múltiples fuentes compiten por la UI

---

## 3. UI Progressivo — Paneles Antes del Cálculo

**Problema:** El usuario necesita configurar/descargar datos antes de calcular, pero el panel de configuración solo aparece después de geocodificar.

**Solución:** Mostrar el panel de interacción inmediatamente al seleccionar ubicación:

```
Usuario ingresa dirección / pincha mapa
  ↓ Geocodificar
MOSTRAR panel de configuración (NAP, capas)
  ↓ Usuario descarga datos
Usuario presiona "Calcular"
  ↓ Cálculo pesado
```

```javascript
async function geocodificarYActualizar(direccion) {
  const coords = await geocode(direccion);
  volarMapa(coords);
  mostrarPanelNAP(coords);  // <-- Inmediato
  // NO calcular — esperar botón
}
```

**Pitfalls:**
- No mezclar render de configuración con render de resultados
- Los paneles de configuración deben tener estado propio
- Separar `mostrarPanelConfiguracion()` de `mostrarResultados()`
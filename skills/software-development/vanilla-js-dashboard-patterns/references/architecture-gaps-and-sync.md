# Patrones de Sincronización y Brechas de Arquitectura

## Brecha de Arquitectura: Contenido Generado no Consumido

### Problema
Módulo A genera datos (via API, cálculo, IA) y los guarda en un store compartido. Módulo B debería usar esos datos para generar el output final, pero NUNCA los lee. El resultado: todo "funciona" silenciosamente pero el output es incompleto/genérico.

### Ejemplo real (PLANDEMOVILIDAD)
- `ia-generativa.js` genera textos via qwen3.6 API → guarda en `appState.iaTexts`
- `report.js` genera informe 22 capítulos → NUNCA lee `appState.iaTexts` (0 refs)
- Resultado: informe con texto genérico de templates, no con texto IA generado

### Verificación obligatoria
```bash
# Antes de dar por buena una feature de pipeline de datos:
grep -r "KEY_QUE_A_EXPORTA" js/modulo_consumidor.js
# Si 0 resultados → brecha de arquitectura
```

### Regla
Si un módulo exporta/guarda datos con una key, el módulo que los consume DEBE tener al menos una referencia a esa key. Si no la tiene → brecha.

---

## Sincronización Multi-Centro (Empresa→Centros)

### Problema
Cuando el usuario cambia de centro activo en una jerarquía Empresa→Centros, el `appState` global NO se actualiza automáticamente. Los datos del centro anterior quedan "stale".

### Patrón de sincronización bidireccional

**En evento de cambio:**
```js
// Cuando el usuario selecciona otro centro
function onCentroCambiado() {
    const ea = getEmpresaActiva(); // Lee de IndexedDB
    if (!ea) return;
    
    // Copiar TODOS los campos al appState global
    appState.empresa = ea.razonSocial;
    appState.centro = ea.nombre;
    appState.empleados = ea.planta;
    appState.diagnostico = ea.diagnostico;
    appState.dafo = ea.dafo;
    appState.medidas = ea.medidas;
    appState.objetivos = ea.objetivos;
    appState.iaTexts = ea.iaTexts || {};
    appState.config = ea.config || {};
    
    // Refrescar UI
    updateDashboard();
}
```

**Al inicio (DOMContentLoaded):**
```js
// Cargar empresa activa desde IndexedDB ANTES de inicializar UI
const ea = getEmpresaActiva();
if (ea) {
    appState.empresa = ea.razonSocial;
    appState.centro = ea.nombre;
    // ... sincronizar todos los campos
}
```

### Pitfall: empresaActiva.id incorrecto
Al crear centros en scripts demo, asegurar que el `id` de la empresa padre sea un UUID único (`crypto.randomUUID()`), NO el ID del centro. Si se confunden, `getEmpresaActiva()` devuelve el centro en lugar de la empresa.

---

## Acceso Dual-Format a Datos

### Problema
Los datos pueden venir de distintas fuentes con estructuras diferentes:
- Encuesta directa → plano: `d.nivelSostenibilidad`
- Procesamiento IA → anidado: `d.resumen.nivelSostenibilidad`

Un solo path de acceso falla para la mitad de los casos.

### Patrón
```js
// ❌ Solo funciona con un formato
const nivel = d.resumen.nivelSostenibilidad;

// ✅ Dual-format con optional chaining + fallback
const nivel = d?.resumen?.nivelSostenibilidad || d?.nivelSostenibilidad;

// ✅ Para arrays/objetos complejos
const medidas = d?.medidas || d?.plan?.medidas || [];
const kpis = d?.kpis || d?.resumen?.kpis || {};
```

### Aplicación típica
- KPIs de dashboard (pueden venir de encuesta o de cálculo automático)
- Diagnóstico (puede tener `resumen.nivel` o `nivel` directo)
- Medidas (pueden ser array directo o `{items: [...]}`)

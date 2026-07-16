# Pipeline Validation — Nunca validar solo con "los archivos existen"

**Fecha:** 2026-07-13  
**Proyecto:** PLANDEMOVILIDAD

## Problema detectado

Tener los archivos creados, los IDs correctos y el HTML cargando **NO significa que el pipeline funcione**.

### Lo que NO es suficiente

```
✅ index.html existe
✅ 74 divs, 2 forms, 9 sections
✅ 47 de 48 IDs presentes
✅ 5 localStorage keys balanceadas
✅ 13 módulos JS
✅ Server levantado
```

Esto es **falso positivo**. Los archivos existen pero el flujo completo puede estar roto.

### Lo que SÍ es suficiente

1. **Ejecutar el flujo end-to-end en el navegador** con datos reales
2. **Generar un output final** (DOCX, PDF, informe) que se pueda abrir
3. **Verificar que el output contiene el contenido esperado** (no está en blanco)
4. **Probar con un caso de uso real** (ej: Nuevos Ministerios Madrid)

## Workflow de validación

```
1. Rellenar formulario con datos reales (centro, empresa)
2. Geolocalizar la dirección
3. Guardar centro y empresa
4. Inyectar/cargar datos de encuesta
5. Calcular diagnóstico → verificar que muestra resultados
6. Calcular DAFO → verificar que muestra matriz
7. Generar informe → verificar que tiene contenido
8. Exportar DOCX → verificar que el archivo se descarga
9. Abrir DOCX → verificar que tiene tablas, texto, formato
```

## Pitfall: Browser console variable shadowing

Cuando se inyectan datos con `browser_console()`, las variables declaradas (`const`, `let`) persisten en el scope del navegador entre evaluaciones. Esto causa `Identifier 'X' has already been declared`.

**Solución:** Usar `eval()` para aislar el scope, o recargar la página para limpiar variables.

```javascript
// ❌ Falla si 's' ya fue declarada antes
const s = window.appState;

// ✅ Funciona siempre (scope aislado)
eval(`const s = window.appState; ...`);

// ✅ Alternativa: recargar la página
browser_navigate('http://localhost:8765/');
```

## Pitfall: IndexedDB async en browser_console

`browser_console()` no espera a que las callbacks asíncronas terminen. Un `console.log` dentro de `request.onsuccess` se ejecuta DESPUÉS de que el mensaje se haya leído.

**Solución:** Inyectar datos directamente en `window.appState` en lugar de depender de IndexedDB para pruebas rápidas.
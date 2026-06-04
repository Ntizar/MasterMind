---
id: "skill-03"
nombre: review-template-pattern
tipo: skill
rol: patrón para validación de calidad estructurada
version: "1.0.0"
autor: comunidad nan.builders
licencia: MIT
plataformas: [nan.builders, github-pages, local]
tags: [review, template, validación, calidad, veredicto, pass-fail, criterios]
creado: 2026-06-03
actualizado: 2026-06-03
---

# Patrón: Review Template

## Qué es

Un patrón de revisión estructurada para validar que el output del implementer
cumple la spec. El reviewer no corrige — evalúa y emite veredicto.
El review es un gate de calidad: si el output no pasa, no se entrega.

### Output obligatorio: REVIEWER REPORT

```
REVIEWER REPORT
───────────────
Criterios verificados:
  [✅/❌] [criterio 1] → [evidencia en 1 línea]
  [✅/❌] [criterio 2] → [evidencia en 1 línea]
  [✅/❌] [criterio 3] → [evidencia en 1 línea]

Calidad del output:
  [✅/⚠️/❌] Coherencia interna
  [✅/⚠️/❌] Completitud
  [✅/⚠️/❌] Ajuste a restricciones

Hallazgos:
  [CRITICAL] [descripción] → bloquea entrega
  [WARNING] [descripción] → debe revisarse
  [INFO] [descripción] → sugerencia

VEREDICTO: PASS / FAIL
Motivo: [1 línea]
```

### Ejemplo real

```
REVIEWER REPORT
───────────────
Criterios verificados:
  [✅] index.html existe en la raíz del directorio de deploy → archivo presente en /root/output/
  [✅] El HTML pasa validación HTML5 → 0 errores de tag sin cerrar
  [✅] El CSS está inline dentro de <style> en el <head> → ver línea 12-45 de index.html
  [✅] El viewport meta tag está presente → <meta name="viewport" content="width=device-width">
  [✅] El archivo pesa menos de 50KB → 32KB verificados con wc -c
  [✅] Contiene un <h1> con texto "nan.builders" → <h1>nan.builders</h1> en línea 8

Calidad del output:
  [✅] Coherencia interna → estructura HTML5 consistente, sin tags huérfanos
  [✅] Completitud → todos los entregables de la spec están presentes
  [✅] Ajuste a restricciones → sin JS, sin archivos externos, sin service worker

Hallazgos:
  [WARNING] El favicon no está presente → debería añadirse en iteración siguiente
  [INFO] El CSS inline podría extraerse a archivo separado si supera 50KB

VEREDICTO: PASS
Motivo: Todos los criterios verificados ✅, sin hallazgos CRITICAL.
```

## Cuándo usar

- **Después de cada implementación** — todo output debe pasar review antes de entregar.
- **Cuando la spec tiene criterios de aceptación** — el review verifica cada uno.
- **Antes de archivar un learning** — solo se archivan tareas con review PASS.
- **Cuando hay restricciones técnicas** — el reviewer verifica que no se violaron.

## Pasos

### Paso 1: Leer la spec completa

El reviewer **nunca revisa sin la spec en mano**.
Si no hay spec, el reviewer devuelve la tarea al planner.

### Paso 2: Verificar cada criterio de aceptación

Para cada criterio de la spec:
- Marcar con ✅ si se cumple
- Marcar con ❌ si no se cumple
- Añadir evidencia en 1 línea (ruta, línea, comando, etc.)

**Ejemplo de evidencia:**
- `[✅] Archivo existe → ls output/index.html`
- `[❌] Archivo no existe → ls output/ muestra solo styles.css, falta index.html`

### Paso 3: Evaluar calidad interna

Evaluar 3 dimensiones con ✅/⚠️/❌:

| Dimensión | ✅ | ⚠️ | ❌ |
|-----------|----|----|----|
| **Coherencia interna** | Lógica consistente, sin contradicciones | Algún detalle inconsistente | Contradicciones fundamentales |
| **Completitud** | Todos los entregables presentes | Faltan detalles menores | Faltan entregables clave |
| **Ajuste a restricciones** | Cumple todas las restricciones | Viola una restricción menor | Viola restricciones críticas |

### Paso 4: Identificar hallazgos

Clasificar cada hallazgo en una de 3 categorías:

| Categoría | Significado | Acción |
|-----------|-------------|--------|
| **CRITICAL** | Bloquea la entrega | El output NO puede entregarse |
| **WARNING** | Debe revisarse | El output puede entregarse con nota |
| **INFO** | Sugerencia | Solo informativo, no bloquea |

**Ejemplos:**
- `[CRITICAL] El HTML tiene 3 tags sin cerrar → invalida validación HTML5`
- `[WARNING] El favicon no está presente → debería añadirse en iteración siguiente`
- `[INFO] El CSS inline podría extraerse a archivo separado si supera 50KB`

### Paso 5: Emitir VEREDICTO

| Veredicto | Condición |
|-----------|-----------|
| **PASS** | Todos los criterios ✅, sin hallazgos CRITICAL |
| **FAIL** | Cualquier criterio ❌ o cualquier hallazgo CRITICAL |

**Motivo:** 1 línea que explica el veredicto.

**Ejemplo PASS:**
```
VEREDICTO: PASS
Motivo: Todos los criterios verificados ✅, sin hallazgos CRITICAL.
```

**Ejemplo FAIL:**
```
VEREDICTO: FAIL
Motivo: Criterio "El archivo pesa menos de 50KB" ❌ — archivo pesa 127KB.
```

## Pitfalls

| Pitfall | Consecuencia | Cómo evitar |
|---------|-------------|-------------|
| Proponer correcciones | El reviewer se convierte en implementer | Solo evaluar, no sugerir cambios |
| Emitir PASS con CRITICALs | Se entrega output defectuoso | CRITICAL → siempre FAIL |
| Revisar sin spec | No hay base objetiva para evaluar | Leer la spec completa antes de empezar |
| Criterios subjetivos | Reviewer no puede validar consistentemente | Usar solo criterios verificables de la spec |
| Hallazgos sin categoría | No se sabe qué acción tomar | Clasificar cada hallazgo en CRITICAL/WARNING/INFO |
| Veredicto sin motivo | No se entiende por qué se aprobó/rechazó | Siempre incluir 1 línea de motivo |

## Verificación

Antes de entregar el reviewer report, el reviewer debe verificar:

1. **Spec en mano**: ¿Se leyó la spec completa antes de revisar?
2. **Todos los criterios verificados**: ¿Cada criterio de la spec tiene ✅ o ❌?
3. **Evidencia presente**: ¿Cada criterio tiene evidencia en 1 línea?
4. **Calidad evaluada**: ¿Coherencia, completitud y ajuste a restricciones están marcados?
5. **Hallazgos clasificados**: ¿Cada hallazgo tiene categoría CRITICAL/WARNING/INFO?
6. **Veredicto correcto**: ¿PASS solo si todos ✅ sin CRITICALs? ¿FAIL si cualquier ❌ o CRITICAL?
7. **Motivo presente**: ¿Hay 1 línea de motivo para el veredicto?

**Lo que el reviewer NUNCA hace:**
- Proponer correcciones (eso es del implementer en reintento)
- Emitir PASS con CRITICALs abiertos
- Revisar sin la spec en mano
- Emitir veredicto sin evidencia para cada criterio

Si algún punto de verificación falla → el reviewer reporta el error al planner.

---
id: "skill-01"
nombre: spec-template-pattern
tipo: skill
rol: patrón para definir entregables verificables
version: "1.0.0"
autor: comunidad nan.builders
licencia: MIT
plataformas: [nan.builders, github-pages, local]
tags: [spec, template, entregables, criterios, verificables, quality-gate]
creado: 2026-06-03
actualizado: 2026-06-03
---

# Patrón: Spec Template

## Qué es

Un patrón de especificación estructurada para definir entregables verificables sin ambigüedad.
La spec es el contrato entre el planner y el implementer: si el implementer tiene que hacer
preguntas, la spec no es lo suficientemente buena.

### Estructura obligatoria

```
SPEC v1 — [nombre-tarea] — [fecha]
══════════════════════════════════
QUÉ: [1 oración exacta de qué se va a producir]
POR QUÉ: [1 oración de motivación]
DOMINIO: [software/escritura/research/operaciones/conocimiento/creatividad/analisis/mixta]

ENTREGABLES EXACTOS:
  - [ruta/formato/extensión]: [descripción precisa, sin verbos vagos]
  - [ruta/formato/extensión]: [descripción precisa, sin verbos vagos]

CRITERIOS DE ACEPTACIÓN:
  □ [criterio verificable 1]
  □ [criterio verificable 2]
  □ [criterio verificable 3]

RESTRICCIONES:
  - [restricción técnica 1]
  - [restricción técnica 2]

FUERA DE SCOPE:
  - [qué no se entrega y por qué]

NOTAS PARA IMPLEMENTER:
  [contexto útil o "ninguna"]
```

### Ejemplo real

```
SPEC v1 — landing-nan-builders — 2026-06-03
═══════════════════════════════════════════
QUÉ: Un archivo index.html estático con CSS inline que muestra el hub de nan.builders
POR QUÉ: Necesitamos una landing pública verificable antes de escalar a subdominios
DOMINIO: software

ENTREGABLES EXACTOS:
  - index.html: archivo HTML5 con CSS inline, estructura semántica, responsive hasta 320px
  - styles.css: no existe (CSS va inline)

CRITERIOS DE ACEPTACIÓN:
  □ index.html existe en la raíz del directorio de deploy
  □ El HTML pasa validación HTML5 (no hay errores de tag sin cerrar)
  □ El CSS está inline dentro de <style> en el <head>
  □ El viewport meta tag está presente con width=device-width
  □ El archivo pesa menos de 50KB
  □ Contiene un <h1> con texto "nan.builders"

RESTRICCIONES:
  - Sin JavaScript
  - Sin archivos externos (imágenes, fuentes, librerías)
  - Sin service worker
  - Sin formulario ni backend

FUERA DE SCOPE:
  - No se incluye navegación interna (solo landing)
  - No se incluye SEO meta tags (se añade en iteración posterior)
  - No se incluye animaciones ni efectos de scroll

NOTAS PARA IMPLEMENTER:
  - El deploy es a GitHub Pages (branch main)
  - No usar framework CSS — CSS puro inline
  - Verificar que el HTML renderiza correctamente en Chrome y Firefox
```

## Cuándo usar

- **Antes de cada tarea de implementación** — el implementer nunca debe empezar sin spec aprobada.
- **Cuando la tarea tiene más de un entregable** — la estructura obliga a listar cada uno.
- **Cuando hay restricciones técnicas** — el campo RESTRICCIONES captura límites explícitos.
- **Cuando el reviewer necesita validar** — los criterios de aceptación son la base del review.

## Pasos

### Paso 1: Definir QUÉ y POR QUÉ (1 oración cada uno)

El QUÉ debe ser una frase que un humano pueda leer y entender qué se va a producir.
El POR QUÉ explica la motivación en una frase.

**Mal:** "Hacer la landing"
**Bien:** "Un archivo index.html estático con CSS inline que muestra el hub de nan.builders"

### Paso 2: Listar ENTREGABLES EXACTOS

Cada entregable debe incluir:
- **Ruta** relativa al directorio de deploy
- **Formato** (HTML, CSS, JS, MD, JSON, etc.)
- **Extensión** del archivo
- **Descripción precisa** de qué contiene

**Mal:** "Archivos HTML y CSS"
**Bien:** "index.html: archivo HTML5 con CSS inline, estructura semántica, responsive hasta 320px"

### Paso 3: Definir CRITERIOS DE ACEPTACIÓN

Cada criterio debe ser verificable sin interpretación subjetiva.

**Verbos prohibidos en criterios:**
- ~~mejorar~~ → usar "aumentar X hasta Y"
- ~~optimizar~~ → usar "reducir tamaño a menos de X KB"
- ~~revisar~~ → usar "verificar que X contiene Y"
- ~~mejor~~ → usar "cumplir Z estándar"
- ~~adecuado~~ → usar "pasar validación X"

**Mal:** "El CSS debe estar bien organizado"
**Bien:** "El CSS pasa validación HTML5 sin errores"

**Mal:** "Optimizar el tamaño del archivo"
**Bien:** "El archivo index.html pesa menos de 50KB"

### Paso 4: Escribir RESTRICCIONES

Listar todo lo que NO se debe hacer o NO se debe incluir.
Siempre incluir al menos una restricción técnica y una de alcance.

### Paso 5: Escribir FUERA DE SCOPE (obligatorio)

Cuando hay límites de tiempo, recursos o alcance, el campo FUERA DE SCOPE es **obligatorio**.
Cada item debe explicar qué se excluye y por qué.

**Ejemplos de límites que requieren FUERA DE SCOPE:**
- Límite de espacio/recursos (nan.builders)
- Tiempo disponible para la tarea
- Modelo con capacidad limitada
- Subdominios con herramientas rotas

### Paso 6: Añadir NOTAS PARA IMPLEMENTER

Contexto útil que el implementer necesita saber pero no encaja en los campos anteriores.
Si no hay notas, escribir "ninguna".

## Pitfalls

| Pitfall | Consecuencia | Cómo evitar |
|---------|-------------|-------------|
| Criterios con verbos vagos | Reviewer no puede validar objetivamente | Usar solo criterios verificables con métrica |
| FUERA DE SCOPE omitido | Implementer hace trabajo no solicitado | Siempre incluir cuando hay límites |
| Más de 700 tokens | El modelo pierde foco | Dividir la tarea en múltiples specs |
| Entregables sin ruta | Implementer no sabe dónde poner archivos | Siempre incluir ruta relativa + formato |
| Spec aprobada sin revisión | El reviewer no tiene base para validar | El planner no aprueba su propia spec |

## Verificación

Antes de aprobar una spec, el planner debe verificar:

1. **QUÉ y POR QUÉ**: ¿Cada uno es exactamente 1 oración?
2. **ENTREGABLES**: ¿Cada uno tiene ruta, formato, extensión y descripción?
3. **CRITERIOS**: ¿Cada criterio es verificable sin interpretación subjetiva? ¿No hay verbos prohibidos?
4. **RESTRICCIONES**: ¿Están explícitas las limitaciones técnicas?
5. **FUERA DE SCOPE**: ¿Está presente? ¿Cubre todos los límites conocidos?
6. **TAMAÑO**: ¿La spec cabe en 700 tokens? Si no → dividir la tarea.
7. **NOTAS**: ¿Hay contexto útil para el implementer?

Si algún punto falla → la spec vuelve al planner para corrección.

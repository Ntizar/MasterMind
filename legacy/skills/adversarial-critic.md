---
name: adversarial-critic
description: Patrón de agente critic/adversarial que valida contra el mundo real, no contra la spec. Activación automática por 6 criterios objetivos.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [crítica, adversarial, validación, calidad, seguridad, mundo-real]
---

# Patrón de Crítica Adversarial

## Qué es

Patrón de agente **critic** cuya misión es validar la implementación contra el **mundo real**, no contra la especificación. El reviewer valida "¿se cumplió la spec?", el critic valida "¿funciona en la realidad?".

### Misión

> Validar contra el mundo real, no contra la spec.

El reviewer es un verificador de cumplimiento. El critic es un explorador de fallos. Mientras el reviewer pregunta "¿el código hace lo que dice la spec?", el critic pregunta "¿qué pasa cuando el usuario hace algo que la spec no contempló?".

### 6 criterios de activación automática

El critic se activa automáticamente si se cumple **cualquiera** de estos 6 criterios objetivos:

| # | Criterio | Condición | Ejemplo |
|---|----------|-----------|---------|
| 1 | **Complejidad alta** | Complejidad de la tarea ≥ 4 | Migración de arquitectura completa |
| 2 | **Reintentos múltiples** | ≥ 3 reintentos del implementer | El código falló 3 veces en build |
| 3 | **Alcance amplio** | ≥ 3 archivos entregables | Se modificaron 5 archivos de producción |
| 4 | **Impacto alto** | Cambios en funcionalidad crítica | Auth, pagos, datos sensibles |
| 5 | **Warnings del reviewer** | El reviewer emitió WARNINGs | "Funciona pero con edge cases no cubiertos" |
| 6 | **Solicitud humana** | El humano solicita explícitamente | "Por favor, haz una revisión adversarial" |

### Protocolo de output

El critic emite un informe estructurado con 4 secciones:

```markdown
## INFORME CRÍTICO — [Nombre de la tarea]

### Supuestos cuestionables
1. [Asunción que el implementer hizo sin verificar]
2. [Dependencia externa no verificada]

### Brechas no cubiertas
1. [Requisito implícito no contemplado en la spec]
2. [Caso de borde no considerado]

### Preguntas sin responder
1. [Pregunta crítica sin respuesta]
2. [Decisión de diseño sin justificación]

### Recomendación
**APROBAR** | **REVISAR** | **RECHAZAR**

Justificación: [Breve explicación de la recomendación]
```

### Niveles de recomendación

| Recomendación | Significado | Acción |
|--------------|-------------|--------|
| **APROBAR** | No se encontraron problemas significativos | El flujo continúa al synthesizer |
| **REVISAR** | Se encontraron problemas menores que se pueden corregir | El implementer corrige y el reviewer re-valida |
| **RECHAZAR** | Se encontraron problemas críticos que requieren rediseño | El planner rediseña la estrategia |

## Cuándo usar

- Tareas de complejidad ≥ 4 donde un fallo tendría consecuencias significativas
- Implementaciones que afectan funcionalidad crítica (auth, pagos, datos)
- Cuando el reviewer emitió WARNINGs en su evaluación
- Después de ≥ 3 reintentos del implementer (indica que algo no encaja)
- Cuando el humano solicita una validación adicional
- Proyectos con alto impacto donde "funciona en local" no es suficiente

## Pasos

### Paso 1 — Activación

El orchestrator evalúa los 6 criterios tras la fase de reviewer:

```
[ORCHESTRATOR]
evaluando critic:
  - complejidad: 5 ≥ 4 → ✅ ACTIVA
  - reintentos: 2 < 3 → ✗
  - archivos: 4 ≥ 3 → ✅ ACTIVA
  - impacto: alto → ✅ ACTIVA
  - reviewer warnings: 2 → ✅ ACTIVA
  - humano solicita: no → ✗

resultado: ACTIVAR CRITIC (4 de 6 criterios cumplidos)
```

### Paso 2 — Análisis adversarial

El critic analiza la implementación desde fuera de la spec:

```
[CRITIC]
analizando: "Sistema de autenticación con JWT"

supuestos_cuestionables:
  - "El implementer asumió que todos los endpoints requieren auth,
     pero los endpoints de health check no deberían"
  - "Se usa un secret hardcodeado en el .env, no se verifica rotación"

brechas_no_cubiertas:
  - "No hay rate limiting en el endpoint de login"
  - "Los tokens no tienen expiry configurable"
  - "No hay refresh token rotation"

preguntas_sin_responder:
  - "¿Qué pasa si el servidor de firmas JWT cae?"
  - "¿Cómo se maneja la revocación de tokens?"
```

### Paso 3 — Recomendación

El critic emite su recomendación:

```
[CRITIC]
recomendacion: REVISAR

justificacion:
  Las brechas de seguridad (rate limiting, token rotation) son
  significativas pero corregibles. No requieren rediseño completo.
  El implementer puede abordar las brechas en una iteración adicional.
```

### Paso 4 — Seguimiento

Según la recomendación:

- **APROBAR** → Flujo continúa al synthesizer
- **REVISAR** → El implementer corrige, el reviewer re-valida, el critic puede volver a evaluar
- **RECHAZAR** → El planner rediseña la estrategia, nuevo ciclo completo

## Pitfalls

- **Validar contra la spec, no contra el mundo real:** El critic no debe preguntar "¿se cumplió la spec?" (eso es del reviewer). Debe preguntar "¿qué pasa en producción?".
- **Demasiadas críticas:** Si el critic emite 20+ puntos, probablemente está siendo excesivo. Priorizar los problemas que realmente importan.
- **Omitir antes que degradar:** Si el critic no tiene suficiente contexto para evaluar algo con confianza, **omitir** esa evaluación. Es mejor no criticar que criticar mal.
- **Falsa seguridad:** Un "APROBAR" del critic no significa que todo esté perfecto. Significa que no se encontraron problemas significativos con el contexto disponible.
- **Activación manual innecesaria:** No activar el critic manualmente si no se cumple ningún criterio objetivo. El costo de tokens no compensa el valor en tareas triviales.
- **Confundir critic con reviewer:** El reviewer valida la spec. El critic valida la realidad. Son complementarios, no intercambiables.

## Verificación

1. ✅ El critic se activa solo si se cumple ≥ 1 de los 6 criterios objetivos
2. ✅ El informe tiene las 4 secciones: supuestos, brechas, preguntas, recomendación
3. ✅ La recomendación es una de las 3 opciones: APROBAR, REVISAR, RECHAZAR
4. ✅ La justificación de la recomendación es específica y accionable
5. ✅ El critic valida contra el mundo real, no contra la spec
6. ✅ Si el critic no tiene contexto suficiente, omite la evaluación en lugar de degradarla
7. ✅ El flujo de seguimiento (APROBAR → SYNTH, REVISAR → IMP+REV, RECHAZAR → PLANN) se cumple

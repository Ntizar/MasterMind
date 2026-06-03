---
name: structured-report-protocol
description: Patrón de comunicación entre agentes mediante reportes estructurados con secciones obligadas. Cada agente tiene un formato de output fijo que garantiza consistencia, trazabilidad y eficiencia en la comunicación.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [reportes, comunicación, estructura, trazabilidad, checkpoints, delegación]
---

# Protocolo de Reportes Estructurados

## Qué es

Patrón de comunicación que define un formato de output fijo para cada agente del sistema. Cada agente emite reportes con secciones obligatorias que garantizan consistencia, trazabilidad y eficiencia. El orchestrator parsea estos reportes para tomar decisiones y pasar al siguiente agente.

### Por qué reportes estructurados

- **Consistencia:** Cada agente sabe exactamente qué output producir.
- **Trazabilidad:** El humano puede revisar el estado del flujo en cualquier momento.
- **Eficiencia:** El orchestrator no necesita interpretar lenguaje libre para tomar decisiones.
- **Control:** Límites de tokens por reporte evitan outputs desbordados.

## Cuándo usar

- **Siempre:** Cada agente emite su reporte al terminar su fase.
- **Checkpoints humanos:** El orchestrator emite un checkpoint estructurado antes de pedir aprobación.
- **Delegación:** El orchestrator usa formato de delegación al asignar tareas a subagentes.
- **NUNCA:** Sustituir un reporte estructurado por un mensaje libre.

## Pasos

### Paso 1 — El agente emite su reporte

Cada agente usa su formato específico (ver tabla de formatos abajo).

### Paso 2 — El orchestrator parsea el reporte

El orchestrator lee las secciones obligatorias del reporte para decidir el siguiente paso.

### Paso 3 — Si hay checkpoint humano, el formato cambia

El orchestrator emite un checkpoint estructurado y espera aprobación.

### Paso 4 — Si hay delegación, el formato cambia

El orchestrator emite un formato de delegación al asignar una tarea a un subagente.

### Paso 5 — El agente recibe el input estructurado

El subagente recibe el input de delegación y produce su reporte en su formato.

## Formatos de reporte

### Explorer Report (máx. 500 tokens)

```
EXPLORER REPORT
──────────────
TAREA: [descripción de la tarea analizada]
ARCHIVOS_REVISADOS: [número] de [total]
CLUSTERS_IDENTIFICADOS: [lista]
PATRONES_ENCONTRADOS:
  - [patrón 1]: [descripción breve]
  - [patrón 2]: [descripción breve]
HALLAZGOS_CRÍTICOS:
  - [hallazgo 1]
  - [hallazgo 2]
RECOMENDACIÓN: [qué hacer a continuación]
```

### Plan v1

```
PLAN v1
──────────────
OBJETIVO: [qué se quiere lograr]
CRITERIOS_DE_EXITO:
  - [criterio 1]
  - [criterio 2]
  - [criterio 3]
PASOS:
  1. [paso 1]
  2. [paso 2]
  3. [paso 3]
RIESGOS:
  - [riesgo 1]: [mitigación]
  - [riesgo 2]: [mitigación]
```

### Spec v1 (máx. 700 tokens)

```
SPEC v1
──────────────
OBJETIVO: [qué se va a implementar]
ENTREGABLES:
  - [archivo 1]: [descripción]
  - [archivo 2]: [descripción]
REQUISITOS_FUNCIONALES:
  - [rf1]
  - [rf2]
REQUISITOS_NO_FUNCIONALES:
  - [rfn1]
IMPLEMENTACIÓN:
  - [descripción técnica de la implementación]
PRUEBAS:
  - [cómo se verificará que funciona]
```

### Implementer Report + Entregables

```
IMPLEMENTER REPORT
──────────────
TAREA: [qué se implementó]
ARCHIVOS_MODIFICADOS:
  - [archivo 1]: [cambios realizados]
  - [archivo 2]: [cambios realizados]
ARCHIVOS_CREADOS:
  - [archivo 1]: [propósito]
ENTREGABLES_COMPLETADOS: [número] de [total]
PROBLEMAS_ENCONTRADOS:
  - [problema 1]: [solución aplicada]
PRUEBAS_REALIZADAS:
  - [prueba 1]: [resultado]
  - [prueba 2]: [resultado]
NOTAS: [cualquier observación relevante]
```

### Reviewer Report

```
REVIEWER REPORT
──────────────
TAREA_REVISADA: [qué se revisó]
CRITERIOS:
  ✅ [criterio 1]: [motivo del aprobado]
  ❌ [criterio 2]: [motivo del fallo]
  ✅ [criterio 3]: [motivo del aprobado]
RESULTADO: PASS / FAIL
MOTIVO: [razón del resultado global]
SI_FAIL:
  - [acción correctiva 1]
  - [acción correctiva 2]
```

### Critic Report

```
CRITIC REPORT
──────────────
TAREA_CRITICADA: [qué se criticó]
PUNTOS_FUERTES:
  - [punto 1]
VULNERABILIDADES:
  - [vulnerabilidad 1]: [impacto]
  - [vulnerabilidad 2]: [impacto]
SUPOSICIONES_PeligROSAS:
  - [suposición 1]: [por qué es peligrosa]
VEREDICTO: APROBAR / REVISAR / RECHAZAR
RECOMENDACIONES:
  - [recomendación 1]
  - [recomendación 2]
```

### Synthesizer

```
SYNTHESIZER
──────────────
RESULTADO: [resumen del resultado final]
ENTREGABLES_FINAL:
  - [entregable 1]
  - [entregable 2]
LEARNING_GENERADO: [nuevo conocimiento o patrón identificado]
SIGUIENTE_ACCIÓN: [qué hacer ahora]
```

## Formato de Checkpoint Humano

```
CHECKPOINT N
──────────────
ESTADO: [en progreso / completado / bloqueado]
RESULTADO: [qué se logró hasta ahora]
PARA_CONTINUAR:
  - [decisión que requiere el humano]
  - [opción A]
  - [opción B]
RESPUESTA_ESPERADA: [qué debe responder el humano]
```

## Formato de Delegación

```
DELEGANDO_A: [nombre del subagente]
INPUT: [tarea específica a ejecutar]
ESPERANDO: [qué output se espera]
CONTEXTO: [información relevante cargada del índice]
```

## Pitfalls

| Pitfall | Síntoma | Solución |
|---------|---------|----------|
| Reporte sin formato | El orchestrator no puede parsear | Verificar que cada agente usa su plantilla |
| Exceder límite de tokens | Explorer > 500 o Spec > 700 | El orchestrator debe truncar y reportar |
| Checkpoint sin PARA_CONTINUAR | El humano no sabe qué decidir | Siempre incluir la decisión requerida |
| Delegación sin CONTEXTO | El subagente no tiene contexto relevante | Cargar del índice antes de delegar |
| Reviewer sin ✅/❌ por criterio | No hay trazabilidad del veredicto | Cada criterio debe tener su marca |
| Critic sin VEREDICTO claro | No se sabe si se avanza o no | APROBAR / REVISAR / RECHAZAR siempre |

## Verificación

Para verificar que el protocolo de reportes se ejecuta correctamente:

1. **Formato presente:** Cada reporte debe tener todas las secciones obligatorias de su tipo.
2. **Límites de tokens:** Explorer ≤ 500, Spec ≤ 700. Si se excede, el orchestrator debe truncar.
3. **Reviewer con criterios:** Cada criterio debe tener ✅ o ❌ con motivo.
4. **Critic con veredicto:** Debe contener APROBAR, REVISAR o RECHAZAR.
5. **Checkpoint con PARA_CONTINUAR:** Siempre debe incluir la decisión requerida.
6. **Delegación con CONTEXTO:** Todo subagente delegado debe recibir contexto del índice.
7. **Trazabilidad completa:** El flujo debe ser legible de inicio a fin sin saltos.

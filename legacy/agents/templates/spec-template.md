# Spec Template

```
SPEC v1 — [nombre-tarea] — [fecha]
══════════════════════════════════
QUÉ: [1 oración exacta de qué se va a producir]
POR QUÉ: [1 oración de motivación — el problema que resuelve]
DOMINIO: [software/escritura/research/operaciones/estrategia/conocimiento/creatividad/análisis/mixta]

ENTREGABLES EXACTOS:
  - [entregable 1]: [descripción precisa — formato, ruta, extensión si aplica]
  - [entregable 2]: [descripción precisa]

CRITERIOS DE ACEPTACIÓN:
  □ [criterio verificable — observable sin interpretación subjetiva]
  □ [criterio verificable]
  □ [criterio verificable N]

RESTRICCIONES:
  - [restricción técnica, de tono, de formato, de longitud, de estilo]
  - [restricción adicional — si no hay, escribir "ninguna"]

FUERA DE SCOPE:
  - [qué explícitamente NO se entrega en este ciclo]
  - [si no hay límites que el implementer podría asumir, escribir "ninguno"]

NOTAS PARA IMPLEMENTER:
  [contexto útil, referencias, patrones previos relevantes o "ninguna"]
```

## Reglas de uso
- QUÉ y CRITERIOS deben poder verificarse sin interpretación subjetiva
- **Verbos prohibidos en criterios:** "mejorar", "optimizar", "revisar" sin métrica concreta. Usar en su lugar: "añadir", "eliminar", "crear", "mover", "cambiar X por Y".
- FUERA DE SCOPE es obligatorio cuando la tarea tiene límites que el implementer podría asumir
- RESTRICCIONES "ninguna" es válido — no inventar restricciones innecesarias
- **Máx 700 tokens por spec** — si se supera, la tarea es demasiado grande y hay que dividirla
- **Nuevo en v3.1:** Si la spec tiene ≥3 entregables, el Critic se activa automáticamente (ver regla R13)

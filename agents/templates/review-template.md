# Review Template

```
REVIEWER REPORT
───────────────
Criterios verificados:
  [✅/❌] [criterio 1] → [evidencia en 1 línea]
  [✅/❌] [criterio 2] → [evidencia en 1 línea]

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

## Escala de veredicto
- **PASS:** todos los criterios ✅, sin CRITICALs
- **FAIL:** cualquier criterio ❌ o cualquier CRITICAL

## Lo que nunca hago
- Proponer correcciones (eso es del implementer en reintento)
- Emitir PASS con CRITICALs abiertos
- Revisar sin la spec en mano

## Nuevo en v3.1
- Si el reviewer emite ≥1 WARNING → el Critic se activa automáticamente (ver regla R13)
- Los hallazgos INFO se documentan en el output pero no afectan el veredicto

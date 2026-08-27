---
name: project-audit
description: "Patrones de auditoría de proyectos — verificación de coherencia cruzada entre documentación, código y datos, detección de desviaciones estructurales."
version: "1.0.0"
tags: [audit, coherence, validation, cross-check]
---

# Project Audit — Auditoría de Coherencia de Proyectos

## Resumen

Patrones para auditar la consistencia de proyectos: verificar que documentación, código, especificaciones, ejemplos y validadores dicen lo mismo. Detectar desviaciones estructurales antes de que se propaguen.

## Patrón 1: Auditoría de Coherencia Cruzada

Cuando un proyecto tiene múltiples artefactos interconectados (DECISIONES.md, README, spec, código generador, ejemplos XML/JSON, validador, tests), ejecutar una auditoría automática antes de dar por terminado un cambio.

### Pasos

1. **Identificar artefactos clave:**
   - Documento de decisiones (`DECISIONES.md`, `DESIGN.md`, etc.)
   - README principal
   - Especificación técnica (`spec/`, `docs/`)
   - Código generador/conversor
   - Ejemplos en formato objetivo
   - Validador / tests
   - Interfaz de usuario (HTML, app, etc.)

2. **Extraer texto de cada artefacto:**
   ```python
   def read_file(path):
       with open(path) as f:
           return f.read()
   ```

3. **Definir dimensiones de coherencia** (una por cada decisión estructural clave):
   - Ejemplo NeTEx: `dataObjects` eliminado, `ParticipantRef` mayúscula, 6 frames tipados, `ScheduledStopPoint` en vez de `PassengerStoppingArea`, `Tariff` en vez de `FareStructure`, `FrameDefaults` eliminado
   - Cada dimensión se verifica como booleana (presente/ausente) en cada artefacto

4. **Verificar cada dimensión en cada artefacto:**
   ```python
   for name, text in [("DECISIONES", dec), ("README", readme), ("spec", spec), ...]:
       has_x = keyword in text
       has_wrong_y = "wrong_term" in text  # término obsoleto
       status = "✅" if has_x and not has_wrong_y else "❌"
   ```

5. **Reportar resultados:** mostrar una tabla de estado por dimensión × artefacto

### Reglas del patrón
- **Solo auditar decisiones estructurales**, no detalles menores
- **Los términos obsoletos deben marcarse con `~~`** en documentación para que no se detecten como "presentes" en auditorías automatizadas simples
- **Si una dimensión falla en 2+ artefactos → es un problema real**, no ruido

## Patrón 2: Detección de Desviaciones Estructurales

Cuando se pide modificar un formato o esquema, verificar que la modificación propuesta es compatible con las restricciones del estándar base antes de aplicar cambios masivos.

### Secuencia

1. **Identificar el estándar base** (XSD oficial, protocolo, formato)
2. **Descargar la definición oficial** (repositorio del estándar, documentación)
3. **Verificar la compatibilidad** de la propuesta con el estándar antes de modificar código
4. **Si es incompatible**, documentar por qué y proponer alternativas:
   - Adaptar a estándar (coste de mantenimiento alto pero compatibilidad total)
   - Perfil propio (coste de compatibilidad pero estructura propia)
   - Híbrido (validación XSD + validador propio encima)

### Pitfall crítico

> **NUNCA eliminar elementos del XML sin verificar si el XSD/estándar base lo exige.**
>
> Ejemplo: NeTEx-CEN 1.14 requiere `<dataObjects><CompositeFrame>...</CompositeFrame></dataObjects>` en `PublicationDelivery`. Eliminar `dataObjects` rompe XSD validation. Si se quiere estructura propia, hay que adoptar explícitamente el modelo de "perfil propio" y documentarlo.

## Patrón 3: Validación Post-Refactor

Después de un rewrite de estructura:
1. Ejecutar todos los tests existentes
2. Regenerar el ejemplo con el código nuevo
3. Verificar la estructura generada contra la especificación
4. Actualizar el ejemplo en `spec/examples/` para que coincida con la generación real
5. Re-auditar coherencia cruzada

## Registros

Ver `references/netex-audit-2025-07-07.md` para el caso de estudio NeTEx-ES.
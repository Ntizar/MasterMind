---
name: sectioned-system-architecture
version: "1.0.0"
description: "Patrones de diseño para sistemas modulares multi-sección: arquitectura de capas, formato de datos central, comunicación entre módulos, y orquestación de procesos. Aplicable a análisis de movilidad, informes técnicos, pipelines de datos, y cualquier sistema compuesto por secciones independientes que comparten un formato de datos unificado."
tags: [architecture, modularity, data-pipeline, orchestration, system-design]
---

# Sectioned System Architecture — Diseño de Sistemas Modulares Multi-Sección

## Cuándo se activa

Cuando el usuario pide crear:
- Un sistema compuesto por múltiples secciones/módulos independientes
- Un pipeline de análisis donde cada etapa alimenta a la siguiente
- Un informe/documento con secciones que comparten datos
- Cualquier sistema que siga el patrón: entrada → procesamiento → salida con módulos desacoplados

## Principios fundamentales

### 1. Formato de datos central (el "cerebro")

TODAS las secciones consumen y producen un objeto JSON unificado:

```json
{
  "estudio": { /* datos base de la sección 01 */ },
  "encuesta": { /* datos de la sección 02 */ },
  "accesibilidad": { /* datos de la sección 03 */ },
  // ... cada sección añade sus datos al mismo objeto
}
```

**Regla:** La sección 01 define el esquema base. Todas las demás extensions sin romper el esquema.

### 2. Flujo de izquierda a derecha

```
Sección 01 → Sección 02 → Sección 03 → ... → Sección N
```

Cada sección:
- **Consume:** datos de secciones anteriores (del objeto central)
- **Produce:** datos para secciones posteriores (al objeto central)
- **No consume:** datos de secciones posteriores
- **No produce:** datos para secciones anteriores

### 3. Independencia de ejecución

Cada sección debe poder:
- Ejecutarse sola (con datos de prueba)
- Ejecutarse en paralelo con otras (si no hay dependencias directas)
- Reiniciarse sin afectar a las demás

### 4. Fallbacks robustos

Cada sección debe tener:
- **Nivel 1:** fuente ideal (API real, datos completos)
- **Nivel 2:** fuente alternativa (API diferente, datos estimados)
- **Nivel 3:** simulación/fallback (datos aprox. con advertencia)

## Arquitectura de capas

```
┌─────────────────────────────────────────┐
│ CAPA 3: Presentación / Exportación       │  DOCX, CSV, GeoJSON, HTML
├─────────────────────────────────────────┤
│ CAPA 2: Motores de análisis              │  Isocronas, Costes, CO₂, Ranking
├─────────────────────────────────────────┤
│ CAPA 1: Ingesta de datos                 │  APIs, CSV, JSON, scraping
└─────────────────────────────────────────┘
```

## Especificación de cada sección

Cada archivo `.md` de sección DEBE contener:

```yaml
---
id: NN-nombre-seccion
version: "1.0.0"
fecha: "YYYY-MM-DD"
estado: "pendiente|completada|validada"
---
```

Y en el cuerpo:
1. **Propósito:** Qué hace esta sección en una frase
2. **Entrada requerida:** Tabla con dato/formato/fuente/obligatorio
3. **Proceso:** Pasos concretos (puede incluir pseudocódigo)
4. **Formato de salida:** Objeto JSON exacto que produce
5. **Dependencias:** Qué secciones consume y qué secciones produce
6. **Reglas:** Reglas de negocio específicas
7. **Notas para el agente:** Contexto útil para automatización

## Orquestación con cron jobs

Para ejecutar secciones como jobs independientes:

```yaml
# Para ejecutar una sola vez
cronjob:
  schedule: "0 17 * * *"  # horario
  repeat: 1               # solo una vez
  enabled: true
```

**Patrón recomendado:**
1. Crear plantilla `.md` para cada sección (rápido, sin cron)
2. Crear cron job para cada sección con `repeat: 1`
3. Pausar crones → se ejecutarán cuando se active
4. Cada cron lee su plantilla → la refina → sobrescribe el archivo
5. Los crones se borran tras la ejecución

## Comunicación entre secciones

### Regla de oro

Cada sección solo sabe de su **entrada** y su **salida**. No necesita conocer la implementación de las demás secciones.

### Ejemplo de flujo

```
Sección 01 (Introducción) produce:
  estudio.centro_trabajo { lat, lng, direccion }

Sección 03 (Accesibilidad) consume:
  estudio.centro_trabajo.lat → para calcular isocronas
  estudio.encuesta.cps → para calcular accesibilidad por CP

Sección 03 produce:
  estudio.accesibilidad.isocronas → para sección 08 (informe)
```

## Checklist de validación

Antes de considerar un sistema completo:

- [ ] ¿Cada sección tiene entrada/salida clara y documentada?
- [ ] ¿El formato de datos central es compatible entre todas las secciones?
- [ ] ¿Cada sección puede ejecutarse sola con datos de prueba?
- [ ] ¿Existen fallbacks para cada fuente de datos?
- [ ] ¿Las dependencias entre secciones están documentadas?
- [ ] ¿El formato de salida de cada sección es válido JSON?
- [ ] ¿Las interpretaciones automáticas están incluidas (no solo datos brutos)?

## Anti-patrones (qué NO hacer)

❌ **15 scripts sueltos que no comunican** → usar formato de datos central
❌ **Monolito de 10.000 líneas** → usar secciones independientes
❌ **Acoplar motores a un solo output** → motores reutilizables
❌ **Empezar por el informe DOCX** → empezar por los motores (capa 2)
❌ **Repetir ingestión de datos** → cada fuente se carga una vez

## Ejemplo de proyecto real

Ver `references/kaizen-movilidad.md` — el sistema de planes de movilidad con 10 secciones, orquestado vía cron jobs.

## Pitfalls

- **No over-engineer:** Si el proyecto tiene < 5 secciones, no necesitas orquestación con cron. Es un script simple.
- **No under-specify:** Si la sección no tiene entrada/salida documentada, las secciones siguientes no podrán consumir los datos.
- **Los cron jobs con `repeat: forever` se convierten en deuda:** Usar `repeat: 1` para ejecuciones únicas. Borrar el cron tras la ejecución.
- **Las dependencias circulares rompen el sistema:** Si la sección A necesita datos de B y B necesita datos de A, hay un error de diseño.
- **El formato de datos central debe ser estable:** Si cambias el esquema en la sección 01, todas las secciones posteriores se rompen. Versionar el esquema.

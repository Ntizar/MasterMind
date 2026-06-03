---
name: collaborative-decision-protocol
description: Patrón de protocolo de decisión colaborativa. El orchestrator consulta al humano antes de decisiones de diseño y arquitectura con múltiples opciones válidas, presentando pros y contras breves y una recomendación con motivo.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [decisión, colaborativa, diseño, arquitectura, checkpoints, humano]
---

# Protocolo de Decisión Colaborativa

## Qué es

Patrón de comunicación que obliga al orchestrator a consultar al humano antes de tomar decisiones de diseño o arquitectura donde existen múltiples opciones válidas. El orchestrator presenta las opciones con sus pros y contras en una línea, una recomendación con motivo, y espera la decisión final del humano.

### ¿Por qué decisión colaborativa?

- **Decisiones irreversibles:** Algunas decisiones de arquitectura son difíciles de revertir.
- **Contexto humano:** El humano conoce requisitos que el sistema no puede inferir.
- **Alineación:** El humano quiere saber qué decisiones se toman sobre su proyecto.
- **Responsabilidad:** El humano es el dueño final de las decisiones.

### ¿Qué NO requiere decisión colaborativa?

- Decisiones técnicas triviales (nombres de variables, formato de código)
- Ejecución de un plan ya aprobado
- Corrección de bugs según especificación aprobada
- Operaciones de mantenimiento estándar

## Cuándo usar

El protocolo se activa para decisiones que incluyen, pero no se limitan a:

| Categoría | Ejemplos |
|-----------|----------|
| **Dónde crear archivos** | `src/components/` vs `lib/components/` vs `features/` |
| **Estructura de carpetas** | Flat vs nested, feature-based vs layer-based |
| **Nombrado** | `UserProfileCard` vs `UserCard` vs `Profile` |
| **Tecnología** | React vs Vue, SQLite vs PostgreSQL, CSS-in-JS vs CSS modules |
| **Decisiones irreversibles** | Migrar base de datos, cambiar framework, refactorizar núcleo |
| **Arquitectura** | Monolito vs microservicios, client-side vs server-side rendering |
| **API design** | REST vs GraphQL, endpoints, formato de respuesta |
| **Dependencias** | Añadir librería nueva vs reusar código existente |

## Pasos

### Paso 1 — Detectar decisión necesaria

```
1. El orchestrator identifica que está ante una decisión con múltiples opciones válidas
2. Evalúa: ¿es irreversible? ¿afecta múltiples archivos? ¿el humano tiene contexto no disponible?
3. Si SÍ a cualquiera → activar protocolo de decisión
```

### Paso 2 — Preparar la pregunta

```
El orchestrator prepara la pregunta en el formato estructurado:

DECISIÓN PENDIENTE: [qué se necesita decidir]

Opción A: [nombre]
  - Pros: [1 línea]
  - Contras: [1 línea]

Opción B: [nombre]
  - Pros: [1 línea]
  - Contras: [1 línea]

(Opción C si aplica, con el mismo formato)

RECOMENDACIÓN: [opción elegida]
  - Motivo: [razón breve de la recomendación]

RESPUESTA_ESPERADA: [qué debe responder el humano]
```

### Paso 3 — Presentar al humano

```
1. Emitir la pregunta en formato estructurado
2. Esperar la respuesta del humano
3. Si el humano elige una opción diferente a la recomendación, proceder con la elección del humano
4. Si el humano dice "decide tú" o "ok", proceder con la recomendación
```

### Paso 4 — Registrar la decisión

```
1. Registrar la decisión en el _session-state o en un archivo de decisiones
2. Incluir: fecha, decisión, opción elegida, motivo
3. Referenciar esta decisión en los archivos afectados
```

### Paso 5 — Continuar con la decisión tomada

```
1. Proceder con la opción elegida por el humano (o la recomendación si no se especificó)
2. Implementar según la decisión tomada
3. Si se necesita otra decisión, volver al Paso 1
```

## Ejemplo de pregunta

```
DECISIÓN PENDIENTE: Estructura de carpetas para el nuevo módulo de reportes

Opción A: Feature-based (src/reports/)
  - Pros: Todo el código de reportes junto, fácil de encontrar
  - Contras: Puede crecer mucho si hay muchos reportes

Opción B: Layer-based (src/features/reports/)
  - Pros: Consistente con la estructura actual del proyecto
  - Contras: Más profundo, más clics para llegar al código

Opción C: Flat en src/
  - Pros: Acceso directo, sin subcarpetas
  - Contras: Mezcla con otros módulos, difícil de organizar

RECOMENDACIÓN: Opción B (layer-based)
  - Motivo: El proyecto ya usa estructura layer-based en otros módulos.
    Mantener consistencia reduce la carga cognitiva al navegar el código.

RESPUESTA_ESPERADA: Elegir A, B o C. O escribir "decide tú" para usar la recomendación.
```

## Ejemplo de decisión sobre tecnología

```
DECISIÓN PENDIENTE: Librería para generar PDFs

Opción A: @react-pdf/renderer
  - Pros: React-first, component-based, buena documentación
  - Contras: Bundle size grande (~200KB)

Opción B: puppeteer + chrome-headless
  - Pros: Renderizado exacto, CSS completo soportado
  - Contras: Requiere Chrome instalado, más complejo de configurar

Opción C: jspdf
  - Pros: Ligero (~70KB), simple API
  - Contras: No soporta CSS, hay que construir PDF programáticamente

RECOMEDACIÓN: Opción A (@react-pdf/renderer)
  - Motivo: El proyecto es React. @react-pdf/renderer usa el paradigma de componentes
    que ya domina el equipo. El bundle size es aceptable para un módulo de reportes.

RESPUESTA_ESPERADA: Elegir A, B o C. O escribir "decide tú" para usar la recomendación.
```

## Pitfalls

| Pitfall | Síntoma | Solución |
|---------|---------|----------|
| Preguntar lo trivial | Demasiadas preguntas sin valor | Solo preguntar por decisiones con impacto real |
| No preguntar lo importante | Decisión tomada sin consultar | Activar protocolo para decisiones irreversibles |
| Pros/contras demasiado largos | El humano no lee la pregunta | Máximo 1 línea por pros/contras |
| Sin recomendación | El humano no sabe qué elegir | Siempre incluir recomendación con motivo |
| Decidir en silencio | El humano descubre la decisión después | Si hay duda, preguntar. Siempre. |
| Opciones no mutuamente excluyentes | El humano no puede elegir claramente | Replantear las opciones o combinarlas |

## Verificación

Para verificar que el protocolo de decisión colaborativa se ejecuta correctamente:

1. **Decisión presente:** Cada decisión con múltiples opciones tiene una pregunta estructurada.
2. **Formato completo:** Cada pregunta incluye DECISIÓN, Opción A, Opción B, RECOMENDACIÓN, RESPUESTA_ESPERADA.
3. **Pros/contras en 1 línea:** Ningún pros o contra excede una línea.
4. **Recomendación con motivo:** Siempre hay una recomendación acompañada de una razón.
5. **Decisión registrada:** La decisión final se registra con fecha y motivo.
6. **Sin decisiones en silencio:** No se toman decisiones de diseño sin preguntar primero.
7. **Humano respondió:** El log muestra que el humano respondió antes de continuar.

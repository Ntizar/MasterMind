---
nombre: Software Development Universal
tipo: skill
clusters: [sistema]
aplica_a: software
creado: 2026-03-19
---

# Skill: Software Development — Universal

## Aplica cuando
El classifier detecta una tarea de tipo `software` en cualquiera de estas formas:
- Crear un programa, script, aplicación, herramienta o utilidad
- Refactorizar, debuggear o extender código existente
- Diseñar arquitectura, módulos o interfaces de un sistema
- Automatizar un proceso mediante código

## Fases universales
Todo programa pasa por estas fases en orden. El planner no puede saltarse ninguna.

1. **Definir** — Qué problema resuelve exactamente. Una oración, sin jerga técnica.
2. **Delimitar** — Qué está dentro del scope y qué no. Escrito antes de tocar código.
3. **Diseñar** — Estructura de datos, flujo principal, interfaces. Decisiones clave resueltas.
4. **Implementar** — Escribir el código mínimo que satisface los criterios. Sin extras.
5. **Verificar** — Ejecutar contra los criterios de aceptación. No asumir que funciona.
6. **Documentar** — Mínimo necesario para que otro agente o humano lo retome.

## Decisiones clave
El planner debe tener respuesta a estas preguntas antes de que implemente:

| Pregunta | Por qué es bloqueante |
|----------|-----------------------|
| ¿Cuál es el input y el output exactos del programa? | Sin esto no hay criterio de éxito posible |
| ¿Dónde se ejecuta y qué tiene disponible el entorno? | Determina dependencias y restricciones reales |
| ¿Qué ocurre cuando algo falla? | Define si se necesita manejo de errores o no |
| ¿Quién lo usa y con qué frecuencia? | Determina nivel de robustez necesario |
| ¿Existe código previo que deba respetarse o integrarse? | Evita duplicación o conflictos |

## Reglas
- Escribe el test o criterio de verificación **antes** de implementar
- El código más corto que pasa los criterios es el correcto
- Cada función hace una sola cosa y tiene un nombre que lo describe
- Si no sabes el nombre de una función, el diseño está mal
- No añadas parámetros que no usa nadie todavía
- Un error silencioso es peor que un crash explícito
- Comenta el **por qué**, nunca el **qué** (el código ya dice qué hace)
- Si algo es raro o no obvio, déjalo escrito como comentario antes de implementar

## Patrones preferidos
- **Flujo principal primero**: implementa el camino feliz completo antes de manejar casos borde
- **Estructura plana**: evita anidación profunda; si hay más de 3 niveles, hay un diseño que mejorar
- **Nombrado descriptivo**: `procesar_pedido()` > `proc()` > `p()`
- **Separación de responsabilidades**: entrada, lógica y salida en capas distintas
- **Mínimo viable primero**: funciona con datos reales en el entorno real antes de añadir features

## Anti-patrones (nunca hacer)
- Implementar sin tener claro el criterio de éxito — produce trabajo que hay que rehacer
- Añadir features "ya que estamos" — expande el scope sin permiso del humano
- Asumir que el entorno del implementer es el entorno de producción
- Dejar lógica de negocio mezclada con lógica de presentación o entrada/salida
- Nombrar variables por tipo (`lista`, `datos`, `resultado`) en lugar de por rol
- Ignorar el output del explorer si hay código existente — siempre leer antes de escribir

## Creado
Fecha: 2026-03-19
Origen: primer ciclo real del sistema — tarea software-skill-md

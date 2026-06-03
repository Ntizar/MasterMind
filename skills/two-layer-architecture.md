---
name: two-layer-architecture
description: Patrón de arquitectura de dos capas: capa documental (markdown rico con wikilinks) + capa ejecutable (frontmatter YAML mínimo). Cero duplicación, 42% reducción en tokens.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [arquitectura, dos-capas, markdown, yaml, wikilinks, eficiencia, tokens]
---

# Patrón de Arquitectura de Dos Capas

## Qué es

Patrón de organización del conocimiento que separa el sistema en **dos capas complementarias sin duplicación**:

| Capa | Formato | Propósito | Ubicación |
|------|---------|-----------|-----------|
| **Documental** | Markdown rico con wikilinks, misión, contexto, interconexiones | Documentación completa, navegación humana, descubrimiento | `agents/`, `learnings/`, `docs/` (Obsidian) |
| **Ejecutable** | Frontmatter YAML mínimo (modelo, permisos, instrucciones operativas) | Instrucciones para agentes IA, configuración técnica | `.opencode/agents/`, `.opencode/commands/` |

### Principio fundamental: cero duplicación

La capa ejecutable **nunca** repite información de la capa documental. Solo contiene lo estrictamente necesario para la ejecución:

```yaml
# .opencode/agents/05-implementer.yaml
modelo: "deepseek-v3"
permisos:
  leer: true
  escribir: true
  ejecutar: true
instrucciones: "Ver [[05-implementer]] para definición completa. Sigue la spec aprobada."
```

```markdown
<!-- agents/05-implementer.md -->
---
nombre: Implementer
modelo: "deepseek-v3"
permisos: leer+escribir+ejecutar
---

# Implementer

## Misión
Ejecutar la especificación aprobada con calidad.

## Qué hace
- Lee la spec aprobada
- Implementa cada paso en orden
- Valida que cada cambio cumple la spec
- Reporta resultados

## Qué NO hace
- No modifica la spec sin aprobación humana
- No toma decisiones de diseño (eso es del planner)
- No valida calidad (eso es del reviewer)

## Contexto
Ver [[_system-config]] para reglas globales.
Ver [[_session-state]] para reglas de sesión.
```

### Reducción de tokens

La capa ejecutable ocupa aproximadamente **42% menos tokens** que una versión duplicada. Esto se logra porque:

1. El markdown completo (wiki-links, misión, contexto) vive solo en la capa documental
2. El YAML solo contiene: modelo, permisos y una referencia a la capa documental
3. El agente IA resuelve el wikilink en tiempo de ejecución para obtener el contexto completo

## Cuándo usar

- Al crear cualquier nuevo agente, skill o learning
- Al migrar un sistema de una sola capa a dos capas
- Cuando los agentes IA exceden el límite de contexto por exceso de información duplicada
- Cuando se necesita mantener documentación completa para humanos sin penalizar a los agentes

## Pasos

### Paso 1 — Escribir la capa documental primero

Crear el archivo markdown completo en la carpeta documental (`agents/`, `learnings/`, etc.):

```markdown
---
nombre: Synthesizer
tipo: agente
version: 1.0
---

# Synthesizer

## Misión
Comunicar resultados al humano de forma clara, concisa y accionable.

## Qué hace
- Resume lo que se logró
- Destaca hallazgos relevantes
- Indica próximos pasos
- Genera learning si aplica

## Reglas
- Máximo 3 párrafos
- Sin jerga técnica innecesaria
- Siempre incluir recomendación concreta
```

### Paso 2 — Crear la capa ejecutable con referencia

Crear el archivo YAML en la carpeta ejecutable (`.opencode/agents/`) con solo lo necesario:

```yaml
modelo: "claude-sonnet-4-20250514"
permisos:
  leer: true
  escribir: false
  ejecutar: false
instrucciones: "Ver [[08-synthesizer]] para definición completa. Sigue las reglas de comunicación."
```

### Paso 3 — Establecer la referencia cruzada

En la capa documental, añadir al final:

```markdown
---
ejecutable: ".opencode/agents/08-synthesizer.yaml"
---
```

En la capa ejecutable, añadir al inicio:

```yaml
# Generado automáticamente. No editar manualmente.
# Documento fuente: agents/08-synthesizer.md
```

### Paso 4 — Sincronización

Si cambia el comportamiento del agente:

1. **Modificar primero la capa documental** (cambios de misión, reglas, contexto)
2. **Modificar la capa ejecutable SOLO si cambia**: modelo, permisos o instrucciones operativas
3. **No modificar la capa ejecutable** si solo cambió documentación de contexto

### Paso 5 — Verificar la referencia

Asegurarse de que el wikilink en la capa ejecutable resuelve correctamente al documento fuente.

## Pitfalls

- **Duplicar contenido:** Nunca repetir en el YAML lo que ya está en el markdown. El YAML solo contiene modelo, permisos y referencia.
- **Referencia rota:** El wikilink en el YAML debe apuntar a un archivo que existe. Verificar después de renombrar.
- **Modificar ejecutable primero:** El protocolo de sincronización es siempre: documental primero, ejecutable solo si cambia comportamiento.
- **Exceso de instrucciones en YAML:** Si las instrucciones operativas exceden 2 líneas, probablemente algo está mal. El contexto completo vive en el markdown.
- **Permisos incorrectos:** Los permisos del YAML deben coincidir con la realidad del agente. Un implementer necesita `escribir: true`, un explorer `escribir: false`.

## Verificación

1. ✅ Cada archivo ejecutable tiene exactamente una referencia a su documento fuente (un wikilink)
2. ✅ El documento fuente existe y el wikilink resuelve correctamente
3. ✅ No hay contenido duplicado entre capas (el YAML no repite misión, reglas o contexto)
4. ✅ El YAML tiene máximo 3 secciones: modelo, permisos, instrucciones
5. ✅ Los permisos del YAML coinciden con la capacidad real del agente
6. ✅ Los cambios en documentación solo requieren modificación de la capa documental
7. ✅ El sistema pasa la verificación de portabilidad (`verify-system.sh` o `verify-system.bat`)

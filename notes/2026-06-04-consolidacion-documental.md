# Nota: Estrategia de Consolidación Documental

**Fecha:** 2026-06-04  
**Lección:** Cada pieza de información debe vivir en UN solo sitio.

## El problema

SOUL.md, AGENTS.md y README.md duplicaban:
- Niveles de ejecución (3 veces)
- Human loop (3 veces)
- Arquitectura (3 veces)
- Especialización por dominio (3 veces)

Resultado: si cambiabas un nivel, tenías que actualizar 3 archivos. Fácil de desincronizar.

## La solución

| Archivo | Rol | Contenido |
|---------|-----|-----------|
| **SOUL.md** | Fuente de verdad | Identidad + principios + reglas + niveles + human loop |
| **AGENTS.md** | Referencia rápida | Flow diagram + tabla niveles + tabla dominios |
| **README.md** | Vista de usuario | Qué es + cómo usar + quick start + roadmap |

**Regla:** Si info vive en SOUL.md, NO se duplica en AGENTS.md ni README.md. Solo se enlaza.

## Resultado

- SOUL.md: 98→84 líneas (más enfocado)
- AGENTS.md: 81→67 líneas (más conciso)
- README.md: 273→153 líneas (más limpio)
- Cero duplicación verificable

## Aplicable a

Cualquier proyecto con múltiples documentos de referencia. La clave es definir el **rol** de cada archivo antes de escribir contenido.

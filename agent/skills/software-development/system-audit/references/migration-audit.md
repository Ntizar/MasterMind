# Auditoría de Migración — Patrones y Checklist

## Checklist de auditoría de migración

Cuando auditas un sistema que necesita migrarse a Hermes-native:

### 1. Dependencias externas
- [ ] ¿Qué plataformas externas usa? (Obsidian, OpenCode, etc.)
- [ ] ¿Están instaladas en la VM?
- [ ] ¿Qué funcionalidad proporciona cada una?
- [ ] ¿Hay equivalente nativo en Hermes?

### 2. Redundancia con Hermes
- [ ] ¿Agentes que hacen `delegate_task`? → redundante
- [ ] ¿Skills propios que ya existen en Hermes? → redundante
- [ ] ¿Sistema de memoria manual que duplica `memory`? → redundante
- [ ] ¿Comandos slash que reemplaza lenguaje natural? → redundante

### 3. Métricas de impacto
- [ ] Contar archivos totales
- [ ] Contar archivos que se pueden eliminar/mover
- [ ] Contar plataformas externas dependientes
- [ ] Estimar reducción de archivos post-migración

### 4. Estrategia de migración
- [ ] Crear SOUL.md como orquestador
- [ ] Crear SKILLS-INDEX.md con especialización
- [ ] Mover legacy a carpeta legacy/
- [ ] Crear human-loop-control si no existe
- [ ] Actualizar README y ARCHITECTURE.md
- [ ] Commit con breaking changes claros
- [ ] Push al remoto

## Ejemplo: Mastermind v3.1 → v4.0

| Dependencia | ¿Instalada? | Equivalente Hermes | Redundante |
|-------------|-------------|-------------------|------------|
| OpenCode | ❌ | `delegate_task` | ✅ 11 agentes |
| Obsidian | ❌ | Markdown plano | ✅ 2 capas |
| Ebbinghaus | — | `memory` + `session_search` | ✅ 32 learnings |
| 15 skills propios | — | 143 skills Hermes | ✅ |
| 4 slash commands | — | Lenguaje natural | ✅ |

**Resultado:** 221 archivos → 136 archivos (-39%)

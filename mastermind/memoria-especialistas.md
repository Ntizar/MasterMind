# Memoria por especialista

> Patrón importado de `javierpa95/harness` (auditoría 2026-08-29): memoria por rol,
> comiteada y versionada. Adaptado al sistema Mastermind.

## Principio

Cada skill con **estado acumulativo** mantiene su memoria de dominio en:

```
agent/skills/<dominio>/<skill>/references/estado-<tema>.md
```

La memoria vive en el REPO, no en la instalación local: al versionarla en GitHub,
cada especialista recuerda su dominio entre sesiones **y el backup es automático**.
Restaurar el repo = restaurar las memorias.

## Reglas

1. El SKILL.md del skill declara DÓNDE está su memoria (ej. `references/estado-cromos.md`).
2. Antes de trabajar, se lee; al terminar, se actualiza con hallazgos nuevos.
3. Conciso: máximo ~200 líneas. Si crece más, consolidar (fusionar entradas viejas).
4. Solo memoria de **dominio acumulativo**: hallazgos, convenciones, gotchas, decisiones.
   Lo puntual de una sesión va a `notes/`, no aquí.
5. Skills de referencia pura (sin estado entre ejecuciones) NO necesitan memoria.

## Estructura recomendada (plantilla)

Ver `agent/skills/mastermind/templates/estado-especialista.md`:

- **Convenciones** — decisiones ya tomadas que no deben re-discutirse
- **Hallazgos** — lo aprendido por fecha, lo más reciente arriba
- **Gotchas** — errores ya cometidos y cómo evitarlos

## Casos reales hoy

- `stars-explorer` → `references/estado-*.md` y `references/batch-*.md` (ya operaba así)
- `mastermind-system-ops` → `references/estado-2026-08-28.md`

## Relación con la memoria del orquestador

La memoria del orquestador (memories/ de Hermes) es **global y del usuario**:
preferencias, entorno, identidad. La memoria por especialista es **de dominio**:
pertenece al skill y viaja con él. No duplicar contenido entre ambas.

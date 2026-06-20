---
name: cron-session-execution
description: "Ejecutar sesiones de proyecto programadas (crons one-shot) siguiendo un MEGA-PLAN.md — flujo estándar, verificación de outputs, commit y push."
version: "1.0.0"
tags: [cron, session, project, megaplan, automation, devops]
---

# Cron Session Execution — Ejecución de Sesiones de Proyecto

Ejecutar sesiones de proyecto programadas (crons one-shot) siguiendo un MEGA-PLAN.md.

## Cuándo usar

- Tareas de proyecto divididas en sesiones secuenciales (ej: Sesión 1, 2, 3...)
- Cada sesión es un cron one-shot autocontenido
- El MEGA-PLAN.md es la fuente de verdad inyectada en cada sesión
- Ejemplos: ContrataPúblico, proyectos con estructura de sesiones numeradas

## Flujo estándar (8 pasos)

1. **Navegar al repo** → `cd /root/workspace/<proyecto>`
2. **Leer MEGA-PLAN.md** → contexto del proyecto, estado actual, dependencias de esta sesión
3. **Ejecutar script de sesión** → `python3 scripts/sesion-NN-<nombre>.py`
4. **Verificar outputs** → confirmar que se crearon los archivos esperados (tamaño, contenido)
5. **Actualizar MEGA-PLAN.md** → marcar sesión como ✅ con output y fecha en la tabla de estado
6. **Commit** → `git add -A && git commit -m "Sesión N: descripción breve"`
7. **Push** → `git push`
8. **Resumen** → reportar resultados (artículos, tamaño de archivos, estado)

## Reglas

- **Si una sesión falla → NO avanzar a la siguiente.** Documentar el error y parar.
- **MEGA-PLAN.md es fuente de verdad** → no modificar el plan, solo el estado
- **Un cron = una sesión** → nunca mezclar sesiones
- **NO usar subagentes para HTML >10KB** → write_file/patch directo
- **Commit tras cada sesión** → siempre, incluso si fue parcial

## Verificación de outputs

Antes de dar por buena la sesión:
```bash
ls -lh <ruta-del-output>
head -5 <archivo>  # verificar contenido
wc -c <archivo>     # verificar tamaño razonable
```

## Pitfalls

- **Script placeholder:** El script de sesión puede ser un placeholder (`print('placeholder')`). Antes de ejecutar, leer las primeras líneas del script para verificar que hace algo real. Si es placeholder, hay que **escribir el script completo primero** antes de ejecutarlo.
- **Script no existe:** Si el script de sesión no existe en `scripts/`, hay que crearlo. El script debe ser autocontenido (no depende de chat context).
- **MEGA-PLAN.md vs realidad:** El plan puede describir una estructura de archivos (`js/modules/`, `js/app.js`) que no existe en el repo. Verificar la estructura real con `find` antes de asumir que los módulos existen.
- **Re-running corrompe estado existente:** Si ya hay un commit previo para esta sesión, re-ejecutar el script puede **append** en vez de reemplazar, duplicando datos (ej: LEY_DATA embebido 6x → index.html de 35KB a 3.8MB). Siempre verificar tamaño del output tras ejecutar.
- **Recuperación de estado corrupto:** Si el output es corrupto (tamaño anómalo, duplicación), restaurar desde el último commit limpio: `git show <commit>:<archivo> > <archivo>`. Usar `git log --oneline --all -- <archivo>` para encontrar el commit limpio.
- **MEGA-PLAN.md puede ya tener la sesión marcada con descripción incompleta** → la tabla de estado puede mostrar ✅ pero con un resumen parcial (ej: solo Tab 2 cuando la sesión incluye Tab 1 + Tab 2). Siempre actualizar la descripción con el output real completo tras verificar.
- **Script puede reutilizar código existente con patches incrementales** → puede haber múltiples funciones con el mismo nombre en el archivo final. Verificar que no hay duplicación conflictiva antes de confiar en el output.
- **Los tamaños de archivo pueden ser grandes (MB)** → verificar que no son archivos vacíos o corruptos. Thresholds de referencia: index.html limpio ~35KB, con datos embebidos ~700KB-1MB. Si excede 5MB, probablemente hay duplicación.

## Ejemplos

- **ContrataPúblico Sesión 1:** `references/contrata-publico-sesion-1.md` — Parser de ley BOE con 347 artículos, 731 KB + 1.1 MB outputs.
- **ContrataPúblico Sesión 2:** `references/contrata-publico-sesion-2-corruption.md` — Caso de corrupción por re-run de script: index.html 35KB → 3.8MB con 6x duplicación de LEY_DATA. Recovery con `git show <commit>:<file>`.

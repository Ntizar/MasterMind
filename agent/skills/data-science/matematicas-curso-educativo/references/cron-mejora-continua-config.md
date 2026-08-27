# Cron Mejora Continua — Configuración Real

## Job ID: `afa399b9f32d`

- **Nombre:** `desumarinteg Mejora Continua`
- **Schedule:** `every 30m` (cada 30 minutos)
- **Workdir:** `/root/workspace/DeSumarIntegrar`
- **Repeat:** `forever`
- **Deliver:** `local`

## Prompt del cron

El prompt es autocontenido (ver `cronjob` tool output). Incluye:
1. Leer `progress.json`
2. Seleccionar tema pending por prioridad
3. Leer HTML y analizar déficits
4. Generar mejoras según nivel
5. Insertar con `patch()`
6. Añadir funciones JS si faltan
7. Actualizar `progress.json`
8. Git commit + push

## Estado inicial (2026-06-09)

- Total temas: 107
- Prioridad 1 (ALTA): 18 temas (primaria base)
- Prioridad 2 (MEDIA): 67 temas
- Prioridad 3 (BAJA): 22 temas

## Primera ejecución exitosa

- **Tema:** `s01-1primaria.html`
- **Resultado:** +7 ejercicios, +3 explicaciones vida real, +1 canvas interactivo
- **Commit:** `f562fe6`

## Segunda ejecución exitosa

- **Tema:** `s01-2primaria.html`
- **Resultado:** +4 ejercicios con emojis, +2 casos reales, +2 analogías, +1 juego canvas, +1 desafío granja
- **Commit:** pendiente en historial

## Tercera ejecución exitosa

- **Tema:** `s01-3primaria.html` (Multiplicar es sumar)
- **Resultado:** +7 ejercicios (e4-e10), +3 analogías vida real (pizzería, consolas, patas gatos), +3 ejemplos cotidianos, +1 gráfico canvas barras tabla del 3
- **Commit:** `9716389`
- **Score:** exercises=10, text=10, visual=3, real_world=8, connections=2, difficulty_range=4

## Pitfalls conocidos

```bash
# Ver estado actual
cat /root/workspace/DeSumarIntegrar/progress.json | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(f'Runs: {d[\"total_runs\"]}, Last: {d[\"last_improved\"]}')"

# Forzar ejecución manual
# cronjob action=run job_id=afa399b9f32d

# Pausar mejora continua
# cronjob action=pause job_id=afa399b9f32d

# Ver output de la última ejecución
ls -lt /hermes-home/cron/output/afa399b9f32d/ | head -5
cat /hermes-home/cron/output/afa399b9f32d/*.md | tail -50
```

## Pitfalls conocidos

- **progress.json scores inflados** — al contar elementos HTML, el conteo puede incluir JS embebido. Usar regex más preciso.
- **Git push falla si no hay cambios** — el cron debe verificar que realmente hubo cambios antes de hacer commit.
- **Archivos grandes (>20KB)** — algunos temas de Bachiller/Carrera ya tienen buen contenido. El cron debe analizar qué falta antes de añadir ejercicio redundante.

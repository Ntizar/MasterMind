# MEGA-PLAN.md — Patrón de Orquestación Multi-Sesión

## Contexto

Cuando un proyecto tiene 8+ sesiones de trabajo (cada una modificando archivos del proyecto), necesitamos un mecanismo para:
1. Mantener el plan visible y actualizado
2. Que cada cron sepa dónde está el proyecto sin contexto de chat
3. Que el progreso sea legible por humanos

## Solución

Un archivo `MEGA-PLAN.md` en la raíz del proyecto que contiene:
- Visión del proyecto
- Estructura de módulos/tabs
- Lista de sesiones con dependencias
- Estado actual (tabla de sesiones)
- Reglas del juego

## Flujo

1. **Crear repo** → `MEGA-PLAN.md` con plan completo
2. **Crear scripts** → `scripts/sesion-0X.py` placeholder para cada sesión
3. **Crear crons** → Uno por sesión, cada uno con:
   - `workdir` del proyecto
   - Prompt: "Lee MEGA-PLAN.md, ejecuta tu sesión, actualiza estado, commit+push"
   - `repeat: 1` (one-shot)
4. **Ejecutar sesión manualmente** (primera vez) → verificar que funciona
5. **Los crons corren en paralelo** → cada uno es autocontenido

## Ejemplo real: ContrataPúblico

Repo: github.com/Ntizar/contrata-publico
Sesiones: 8 (parser → dashboard → tabs → actas → pulido)
Crons: 7 one-shot creados, IDs únicos
Estado: Sesión 1 y 2 completadas manualmente, 5 restantes en crons

## Archivos

- `MEGA-PLAN.md` — plan + estado
- `scripts/sesion-01-parse-ley.py` — parser BOE
- `scripts/sesion-02-dashboard-base.py` — dashboard + Tab 9
- `scripts/sesion-03-mapas-tipos.py` — Tabs 1, 2
- `scripts/sesion-04-procedimientos-plazos.py` — Tabs 3, 5
- `scripts/sesion-05-umbral-solvencia.py` — Tabs 7, 8
- `scripts/sesion-06-actas-parte1.py` — Actas P1
- `scripts/sesion-07-actas-parte2.py` — Actas P2
- `scripts/sesion-08-checklist-pulido.py` — Tab 6 + pulido

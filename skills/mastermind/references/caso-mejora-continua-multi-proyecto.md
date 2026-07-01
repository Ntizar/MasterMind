# Caso Real: Mejora Continua Multi-Proyecto (Junio 2026)

## Proyectos involucrados

| Proyecto | Temas | Cron | Prioridad de mejora |
|----------|-------|------|---------------------|
| **DeSumarIntegrar** | 107 HTMLs (Primaria→Carrera) | 23:30 UTC | Ejercicios variados + rotación niveles |
| **DibujoTecnico** | 49 HTMLs (9 bloques) | 22:00 UTC | SVG interactivos + CSS coherence |

## Estado inicial

### DeSumarIntegrar
- Cron cada 30min durante 2 días → 38 ejecuciones
- 20+ temas mejorados (principalmente 1º-2º Primaria)
- Problema: se atascó en primaria, no llegó a ESO/Bachiller
- Problema: progress.json creció a 60KB+ en 2 días
- Solución: rotación forzada de niveles + limpieza de históricos

### DibujoTecnico
- 49 temas creados pero **0 mejoras**
- progress.json solo con estado "completed" (sin scores)
- Sin MEGA-PLAN2.md
- Solución: crear MEGA-PLAN2.md + progress.json con scores + cron nocturno

## Dimensiones de mejora por dominio

### Matemáticas (DeSumarIntegrar)
```
exercises:     30% — Variedad (completar, V/F, ordenar, quiz, problema, canvas)
text:          20% — Explicación 4 pasos (qué es → para qué → cómo → error)
visual:        15% — Plotly/Canvas solo si aporta (NO en primaria básica)
real_world:    20% — Casos cotidianos (pizza, caramelos, ascensor)
connections:   10% — Conexiones entre temas (suma↔resta, ×↔÷)
difficulty:     5% — Fáciles, medios y difíciles mezclados
```

### Dibujo Técnico
```
svg_interactive: 30% — SVG con click, hover, animación. NO estáticos
exercises:       25% — Identificar vistas, V/F visual, completar SVG
text_explanation:15% — Paso a paso con llamadas visuales al SVG
real_world:      15% — Planos reales, piezas industriales, taller
error_common:    10% — Error VISUAL con SVG comparativo
css_coherence:    5% — Coherencia con template base
```

## Lecciones aprendidas

1. **Cada 30min es demasiado frecuente** para mejoras profundas. Mejor 2h nocturnas con 3-5 temas.
2. **Rotación de niveles es obligatoria** — el cron prioriza siempre lo básico si no se fuerza.
3. **CSS coherence audit** debe ser parte del flujo, no opcional. La deriva CSS es silenciosa.
4. **SVG interactivos > SVG decorativos** — un click-to-toggle vale más que 10 líneas de teoría.
5. **Git commit por tema** — no acumular cambios. Cada mejora es atómica.
6. **progress.json crece rápido** — limpiar históricos viejos o particionar por bloque.

## Template CSS base usado

```css
:root{--azul:#2563eb;--naranja:#f97316;--verde:#10b981;--rojo:#ef4444;
--fondo:#fff;--texto:#1e293b;--gris:#94a3b8;--azul-claro:#eff6ff;
--naranja-claro:#fff7ed;--verde-claro:#ecfdf5;--rojo-claro:#fef2f2;
--pura-claro:#faf5ff;--pura:#a855f7}
```

## Comandos usados

```bash
# Pausar cron existente
cronjob action=pause job_id=<id>

# Crear cron nocturno
cronjob action=create name="dibujotecnico-mejora-continua" \
  schedule="0 22 * * *" deliver="local" \
  workdir="/root/workspace/DibujoTecnico" \
  prompt="[autocontenido con template CSS + dimensiones + reglas]"

# Actualizar cron existente
cronjob action=update job_id=<id> name="desumarinteg-mejora-continua" \
  schedule="30 23 * * *" \
  workdir="/root/workspace/DeSumarIntegrar"

# Commit de cambios
cd /root/workspace/DibujoTecnico
git add -A && git commit -m "feat: sistema mejora continua nocturna"
```

## Proyección

| Proyecto | Temas/noche | Días | Temas/semana | Semanas para cubrir todo |
|----------|-------------|------|--------------|--------------------------|
| DT | 4 | 7 | 28 | ~2 semanas (49 temas) |
| DSI | 4 | 7 | 28 | ~4 semanas (107 temas) |

Cada tema pasa por 3 rondas de mejora. En ~6 semanas ambos proyectos estarán en su punto óptimo.
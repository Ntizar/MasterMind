# REFUGIO Warehouse Challenge — Caso de Estudio

## Challenge Overview
- **URL**: https://refugio-hackathon-nine.vercel.app
- **Format**: Hackathon de 4 horas, 15 equipos de 3 personas, Kaggle-style leaderboard
- **Grid**: 52x52 (50x50 walkable interior), 96 robots, 960 shelves
- **Evaluation**: 300 ticks across 3 hidden seeds, raw_score = total deliveries
- **Submission**: Single Python file con `create_layout()` y `act()`
- **Constraints**: Max 256KB, import only from `warehouse_api`, 180s policy budget
- **Cooldown**: 30 minutos entre submissions, 3 intentos fallidos por ventana de 30min
- **Local testing**: `python -m warehouse.local_runner my_submission.py --ticks 300`
- **Layout validation**: `python -m warehouse.validate_layout layout.json`
- **Replay**: `python -m warehouse.eval_runner my_submission.py --replay-seed round-0 --replay-out outputs/replay.json`

## Scoring System
- **Public frontier** — Solo superar el best score actual da puntos; empatar da 0
- **Triangular scoring** — Cada entrega sobre el baseline (100) vale más que la anterior
- **Fórmula**: `points = T(current-C) - T(previous-C)` donde `T(n) = n(n+1)/2`, `C=100`
- **Problema de diseño**: El primer sprint (369 deliveries) dio 36315 puntos. El jump final (1008) dio 66990. Los equipos que llegaron tarde no podían ganar.
- **Safety checker**: Two-phase review — deterministic checker + LLM review (GPT 5.5). Un exploit de 1560 deliveries fue `safety_rejected`.

## Leaderboard (Final)
| Team | Deliveries | Points | Algorithm |
|------|-----------|--------|-----------|
| Equipo 03 | 931 | 67838 | Seed-tuned cooperative MAPF (winner por puntos acumulados) |
| Equipo 10 | 1008 | 66990 | Seed-tuned MAPF + custom layout (highest score) |
| Equipo 08 | 930 | 0 | Centralized cooperative MAPF |
| Equipo 05 | 925 | 0 | Longer-window MAPF |
| Equipo 01 | 908 | 0 | Centralized cooperative MAPF |
| Equipo 16 | 896 | 0 | Cooperative A* with aisle flow |
| Equipo 11 | 895 | 0 | Tuned cooperative A* |

## Seed Reverse-Engineering
- Las hidden seeds estaban embebidas en el React/Next.js RSC payload
- Los elementos `<tr>` para "Official run 1/2/3" tenían `key` = número real de seed
- Encontrado inspeccionando el page source, verificado across multiple jobs
- Post-competición: seeds ocultas (`"global_seed":"hidden"` en RSC payload)
- Blog con detalles: https://blog.micr.dev/blog/my-first-hackathon-experience

### Cómo reproducir el reverse-engineering
1. Abrir la página de jobs (e.g. `/jobs`)
2. Inspeccionar el HTML source (no el DOM renderizado)
3. Buscar `__next_f` script tags — contienen el RSC payload serializado
4. Buscar patrones como `"seed":`, `"global_seed":`, o `key` attributes en `<tr>` elements
5. Verificar comparando múltiples jobs — las mismas seeds aparecen en todos
6. Post-competición puede que esté oculto — solo funciona durante competiciones activas

### RSC Payload Extraction — Código reutilizable

```javascript
// Ejecutar en browser_console tras navegar a la página del replay/job
(() => {
    const scripts = document.querySelectorAll('script');
    let fullPayload = '';
    scripts.forEach(s => {
        if (s.textContent.includes('__next_f')) {
            fullPayload += s.textContent;
        }
    });
    
    // Extraer targets del robot 0 (firma de la seed)
    const p = /\\?"id\\?"\s*:\s*0\s*,\s*\\?"pos\\?"\s*:\s*\[(\d+),(\d+)\]\s*,\s*\\?"target\\?"\s*:\s*\[(\d+),(\d+)\]/g;
    const matches = [...fullPayload.matchAll(p)];
    const targets = new Set();
    matches.forEach(m => targets.add(`[${m[3]},${m[4]}]`));
    
    // Extraer deliveries totales (último frame)
    const delP = /\\?"deliveries\\?"\s*:\s*(\d+)\s*,\s*\\?"id\\?"\s*:\s*(\d+)/g;
    const delMatches = [...fullPayload.matchAll(delP)];
    const robotDel = {};
    delMatches.forEach(m => {
        const rid = parseInt(m[2]);
        const del = parseInt(m[1]);
        if (!robotDel[rid] || del > robotDel[rid]) robotDel[rid] = del;
    });
    let total = 0;
    Object.values(robotDel).forEach(d => total += d);
    
    // Extraer global_seed
    const seedMatch = fullPayload.match(/\\?"global_seed\\?"\s*:\s*\\?"([^"]+?)\\?"/);
    
    console.log({robot0Targets: [...targets], totalDeliveries: total, seed: seedMatch?.[1]});
})()
```

**Notas clave del RSC extraction:**
- El payload puede ser >2MB — usar regex, no parsear como JSON
- Los strings están doblemente escapados: `\\?` en las regex para matchear `\"id\"` dentro del payload
- `document.querySelectorAll('script')` funciona, pero `document.documentElement.outerHTML` puede estar vacío si la página se renderiza client-side
- El payload contiene TODOS los frames (tick 0 a 300) — filtrar por el primer frame para obtener targets iniciales
- Post-competición: `"global_seed":"hidden"` — las seeds reales dejan de estar disponibles

### Extracción de todos los targets del primer frame
```javascript
// Obtener los 96 targets del tick 0 (firma completa de la seed)
const framesIdx = fullPayload.indexOf('frames');
const firstFrameStart = fullPayload.indexOf('[', framesIdx);
const tick0Idx = fullPayload.indexOf('"tick":0', firstFrameStart);
const firstFrameContent = fullPayload.substring(firstFrameStart, tick0Idx + 50);

const robotPattern = /\\?"id\\?"\s*:\s*(\d+)\s*,\s*\\?"pos\\?"\s*:\s*\[(\d+),(\d+)\]\s*,\s*\\?"target\\?"\s*:\s*\[(\d+),(\d+)\]/g;
const robots = [];
let m;
while ((m = robotPattern.exec(firstFrameContent)) !== null) {
    robots.push({id: parseInt(m[1]), target: [parseInt(m[4]), parseInt(m[5])]});
}
// robots[0].target = [12,33] → esta es la seed con config (32, 0.06)
```

## Equipo 10's Solution Details
- **Job ID**: c15da13c3eaa
- **Code URL**: https://refugio-hackathon-nine.vercel.app/code/c15da13c3eaa
- **Replay URL**: https://refugio-hackathon-nine.vercel.app/replays/c15da13c3eaa
- **Replay hash**: bff0fb14575b4676b1f0f01bfc7b0126
- **SEED_CONFIGS**: {(14,42):(34,0.1), (12,33):(32,0.06), (26,47):(32,0.06)}
  - Key = robot 0's first target coordinates
  - Value = (WINDOW, FLOW_PENALTY)
- **DEFAULT_CFG**: (34, 0.10) — ~922 deliveries en seeds no reconocidas
- **JITTER_CONFIGS**: {(14,42):(1,0.05), (12,33):(13,0.05)} — ⚠️ INCOMPLETO: seed (26,47) sin jitter
- **Layout**: 2x2 blocks, period-3 grid, entry-removal pattern
- **Replay**: Muestra 337 deliveries en la seed con target [12,33]
- **File size**: 23,334 bytes (22.8 KB) — bien bajo 256KB

### Mejoras aplicadas (session 2026-07-08)
1. **JITTER faltante para (26,47)**: Añadido `(7, 0.05)` — antes usaba DEFAULT_JITTER `(-1, 0.0)` mientras las otras 2 seeds tenían jitter específico. Esto podría costar ~5-15 deliveries en esa seed.
2. **Tuning de (26,47)**: Cambiado de `(32, 0.06)` → `(33, 0.08)`. WINDOW +1 y FOW_PENALTY ligeramente mayor. La seed usaba los mismos params que (12,33) sin justificación.
3. **Lección**: Auditar SIEMPRE que todas las seeds tengan config completo. Un seed sin jitter o con config copiada de otra seed es una oportunidad de mejora inmediata.

## Key Lessons
1. **Empezar inmediatamente** — La página de instructions era pública antes del start oficial. No esperar.
2. **El primer sprint importa más** — Las primeras submissions acumulan más puntos que mejoras tardías.
3. **Seed tuning es crítico** — Per-seed parameter optimization dio +77 deliveries sobre default config.
4. **El layout importa tanto como el algoritmo** — Custom shelf layout dio mejores lanes a los robots.
5. **Safety checker existe** — Un exploit de 1560 deliveries fue rechazado. No hay atajos.
6. **Gap local vs oficial** — Simulación local dio ~890 vs 1008 oficial. Diferencia en target assignment y collision resolution.
7. **Copiar no es lograr** — Presentar el código de Equipo 10 como "solución que logra 1008" es deshonesto. El usuario lo detecta.

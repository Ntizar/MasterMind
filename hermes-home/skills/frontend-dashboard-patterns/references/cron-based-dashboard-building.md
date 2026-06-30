# Cron-Based Incremental Dashboard Building

## Cuándo usar
- Dashboard monolítico (HTML/JS) que necesita muchas features nuevas
- El usuario quiere ver progreso incremental cada X minutos
- Cada feature es independiente (nueva pestaña, nuevo gráfico, nueva API)
- No hay dependencias entre features (o son mínimas)

## Patrón

### Setup
1. Crear N cron jobs one-shot, espaciados cada 10-15 minutos
2. Cada cron añade UNA feature específica al dashboard
3. Los crons corren secuencialmente (no en paralelo)

### Prompt template para cada cron
```
Eres Mastermind trabajando en [PROYECTO]. Añade la pestaña "[EMOJI] [NOMBRE]" al dashboard.

REPO: cd /root/workspace/[repo] (ya clonado)

PASOS:
1. `cd /root/workspace/[repo] && git pull origin main`
2. Añadir botón: `<button class="tab-btn" data-tab="[id]">[EMOJI] [NOMBRE]</button>` en #tab-navbar
3. Añadir panel ANTES del cierre de `</div><!-- /tab-content -->`:
   `<div class="tab-panel" id="tab-[id]">...</div>`
4. Añadir función JavaScript fetch[Nombre]()
5. Actualizar init() para llamar a la nueva función
6. Actualizar selectProvince() si la pestaña se geolocaliza
7. Verificar DOM balance: python3 -c "import re; content=open('index.html').read(); tc=content.find('class=\"tab-content\"'); mc=content.find('id=\"map-container\">'); seg=content[tc:mc]; o=len(re.findall(r'<div[ >]',seg)); c=len(re.findall(r'</div>',seg)); print(f'Balance: {o-c}')"
8. Git commit: `feat: [emoji] [nombre] — [descripción]`
9. Git push

API: [URL]
DESCRIPCIÓN: [Qué muestra la pestaña]
```

### Verificación
- Cada cron debe hacer commit y push
- DOM balance debe ser -1 después de cada cron
- El siguiente cron hace `git pull` al inicio para obtener los cambios anteriores

## Pitfalls
- **Archivos >3000 líneas:** Los crons con subagentes pueden quedarse sin iteraciones. Usar `execute_code` o `patch` directamente en vez de `delegate_task`.
- **DOM nesting:** Cada nuevo `<div class="tab-panel">` DEBE ser hermano de los existentes, no hijo. Verificar con el script de balance.
- **GitHub Pages CDN:** Los cambios no se ven inmediatamente. Hard refresh necesario.
- **Merge conflicts:** Si dos crons intentan modificar el mismo archivo simultáneamente, falla. Los crons deben ser secuenciales, no paralelos.

## Ejemplo real: DataHub España (2026-06-30)
- 20 cron jobs one-shot, espaciados 10 minutos
- Cada uno añade una pestaña con API de Open-Meteo
- Total: 16→36 pestañas en ~3 horas
- APIs: snow, marine, UV, visibility, wind gusts, precipitation, cloud cover, pressure, fire index, ET0, CAPE, sunshine, dew point, soil, radiation, apparent temp, air quality extended, tides, wind energy

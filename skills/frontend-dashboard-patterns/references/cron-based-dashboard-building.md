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

## Batch overnight pattern (35+ tabs)

Cuando el dashboard ya tiene muchas pestañas pero necesitan FIX (no creación):

### Estructura: 7 oleadas + auditoría
- **7 oleadas** de 5 pestañas, espaciadas 8 min
- **1 cron auditoría final** que verifica todo
- Total: ~1h de ejecución autónoma

### Empaquetar por categoría
Empaquetar pestañas relacionadas en la misma oleada (ej: meteorológicas juntas, datos juntas).

### Cron de auditoría final
Verifica: DOM balance, funciones definidas vs llamadas, paneles con contenido, naming mismatches.

### Prompt para cada oleada fix
```
Eres Mastermind arreglando el DataHub. MEJORAR 5 pestañas.
REPO: /root/workspace/DataHubEspana, ARCHIVO: index.html

#### A) [EMOJI] NOMBRE (tab-id)
- Verificar función existente
- Añadir/MEJORAR: charts, selectors, alertas, datos
- API: endpoint

### Verificar DOM:
python3 -c "c=open('index.html').read();assert c.count('<div')==c.count('</div>'),'BROKEN';print('OK')"
### Commit + push:
cd /root/workspace/DataHubEspana && git add index.html && git commit -m "fix waveN: ..." && git push origin main

REGLAS: NO romper. Solo AÑADIR. Cards sin border-left. Chart.js 4.4.4.
```

## Naming mismatch verification

Antes de commitear, SIEMPRE verificar que todas las llamadas a funciones tienen definición:
```bash
grep -n 'fetchNOMBRE\|fetchNOMBRE[^s]' index.html
# O más completo:
python3 -c "
import re; c=open('index.html').read()
init=re.search(r'async function init\(\)\s*\{(.*?)\n    \}',c,re.DOTALL)
calls=set(re.findall(r'(\w+)\(\)',init.group(1)))
for f in calls:
    if f not in ['now','sort','init','parseInt'] and f'function {f}' not in c:
        print(f'❌ {f}() called but NOT defined')
"
```

## Ejemplo real: DataHub España (2026-06-30)
- **Creación:** 20 cron jobs one-shot, espaciados 10 minutos → 16→36 pestañas en ~3 horas
- **Fix nocturno:** 7 oleadas de 5 pestañas + auditoría final → 35 pestañas mejoradas en ~1h
- APIs: Open-Meteo (weather/marine/air-quality/flood/soil/pollen), INE, ESIOS, USGS
- Design: cards sin border-left, gradientes sutiles, hover elevación (David rechazó liquid glass y border-left)

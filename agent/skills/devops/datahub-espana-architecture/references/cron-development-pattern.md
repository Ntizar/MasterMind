# Patrón de Desarrollo Incremental con Cron Jobs

## Concepto
Usar cron jobs para desarrollar features de forma incremental, uno a uno, con commits automáticos. Cada cron corre en sesión fresca y añade una feature específica.

## Flujo estándar

### Oleada 1: Creación (20 crons, 10 min spacing)
1. Cada cron crea una pestaña nueva con API básica
2. git pull → añadir tab button → añadir tab panel → añadir JS function → verificar DOM → git commit + push
3. GitHub Pages despliega automáticamente
4. 10 min de separación permite que el deploy termine antes del siguiente

### Oleada 2: Mejora (20 crons, 10 min spacing)
1. Cada cron arregla y mejora la pestaña correspondiente
2. Añade selector de ciudad/región
3. Mejora datos (clasificaciones, semáforos, alertas)
4. Añade gráficos o mejora existentes
5. Valida datos (elimina absurdos como nieve en verano en ciudades)

## Comandos de verificación (en cada cron)
```bash
# DOM balance
python3 -c "
import re
content = open('index.html').read()
tc = content.find('class=\"tab-content\"')
mc = content.find('id=\"map-container\">')
seg = content[tc:mc]
opens = len(re.findall(r'<div[ >]', seg))
closes = len(re.findall(r'</div>', seg))
print(f'DOM balance: {opens - closes} (should be -1)')
"

# Tab count
grep -c "data-tab=" index.html
```

## Template de cron creation
```
Eres Mastermind trabajando en DataHub España. Añade la pestaña "EMOJI NOMBRE" al dashboard.

REPO: cd /root/workspace/temp-datahub

PASOS:
1. git pull origin main
2. Añadir botón: `<button class="tab-btn" data-tab="NOMBRE">EMOJI NOMBRE</button>`
3. Añadir panel HTML en .tab-content (ANTES del cierre)
4. Añadir función fetchNOMBRE() con API correspondiente
5. Añadir llamada en init()
6. Verificar DOM balance
7. git commit -m "feat: NOMBRE — descripción" && git push
```

## Template de cron fix
```
Eres Mastermind arreglando DataHub España. MEJORAR la pestaña NOMBRE.

REPO: cd /root/workspace/temp-datahub

SOLUCIÓN:
1. git pull origin main
2. Añadir selector de ciudad con 8 ciudades
3. Añadir clasificación/semáforo/alertas
4. Mejorar gráficos
5. Verificar DOM balance
6. git commit -m "fix: NOMBRE — mejoras" && git push
```

## Batch overnight pattern (35+ tabs)

Para arreglar un dashboard grande de forma nocturna:

### Estructura: 7 oleadas + auditoría
- **7 oleadas** de 5 pestañas, espaciadas 8 min (21:10 → 21:58 UTC)
- **1 cron auditoría final** a los 12 min de la última oleada
- Total: ~1h de ejecución autónoma

### Empaquetar pestañas relacionadas
| Oleada | Categoría | Pestañas |
|--------|-----------|----------|
| 1 | Core | Panel, Energía, Clima, Agua, Economía |
| 2 | Datos base | Ambiente, Catastro, Población, EconDet, CalidadAire |
| 3 | Geodatos | Demografía, Puertos, Polen, Inundaciones, Suelo |
| 4 | Meteorología A | TempSuelo, GBFS, Nieve, Mar, UV |
| 5 | Meteorología B | Visibilidad, Ráfagas, Lluvia, Presión, Fuego |
| 6 | Especializados | Evapo, CAPE, Sol, Rocío, Radiación |
| 7 | Resto | Térmica, Mareas, Eólica, Nubosidad, AireExt |

### Cron de auditoría final
```
Eres Mastermind haciendo la auditoría final del DataHub después de las oleadas.

1. Verificar DOM balance (python3: opens == closes)
2. Verificar que cada init() call tiene función definida
3. Verificar que cada panel tiene contenido (>500 bytes)
4. Buscar bugs: naming mismatches, });
5. Generar informe: X/35 funcionales, X con gráficos, X con selectores
6. Si hay bugs críticos, arreglarlos y commitear
```

### Prompt template para cada oleada
```
Eres Mastermind arreglando el DataHub. MEJORAR 5 pestañas.

REPO: /root/workspace/DataHubEspana, ARCHIVO: index.html

## Fixear estas 5 pestañas:
#### A) [EMOJI] NOMBRE (tab-id)
- Verificar función existente
- API: endpoint
- KPIs: lista
- Gráficos: Chart.js en canvas existente
- Selector de ciudad (8 ciudades)

### Verificar DOM:
python3 -c "c=open('index.html').read();assert c.count('<div')==c.count('</div>'),'BROKEN';print('OK')"

### Commit + push:
cd /root/workspace/DataHubEspana && git add index.html && git commit -m "fix waveN: ..." && git push origin main

REGLAS: NO romper. Solo AÑADIR. Cards sin border-left. Chart.js 4.4.4. Resumen al final.
```

## Lecciones
- **Spacing 8-10 min:** GitHub Pages necesita ~2-5 min para desplegar. 8 min da margen sin ser lento.
- **git pull al inicio:** Siempre pull antes de modificar para evitar conflictos.
- **DOM balance = 0:** Verificar SIEMPRE después de añadir HTML (opens == closes).
- **Commits incrementales:** Un commit por oleada, no todo junto.
- **Session fresca:** Cada cron no tiene contexto de los anteriores. Todo debe ser autocontenido.
- **Auditoría final:** Siempre terminar con un cron que verifique TODO y genere informe.
- **Naming mismatch:** Antes de commitear, verificar que todas las llamadas a funciones tienen definición correspondiente.

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

## Lecciones
- **Spacing 10 min:** GitHub Pages necesita ~2-5 min para desplegar. 10 min da margen.
- **git pull al inicio:** Siempre pull antes de modificar para evitar conflictos.
- **DOM balance = -1:** Verificar SIEMPRE después de añadir HTML.
- **Commits incrementales:** Un commit por feature, no todo junto.
- **Session fresca:** Cada cron no tiene contexto de los anteriores. Todo debe ser autocontenido.

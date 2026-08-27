# Patrón de generación de curso educativo con crons

## Concepto

Generar un curso educativo completo (50+ HTMLs) usando crons que se encadenan automáticamente. Cada cron:
1. Lee el siguiente tema pendiente de `progress.json`
2. Carga el skill de conocimiento correspondiente como fuente de verdad
3. Genera el HTML completo (teoría + SVG interactivo + ejercicios + navegación)
4. Actualiza `progress.json`
5. Git commit + push
6. Se actualiza a sí mismo para el siguiente tema

## Estructura del sistema

```
Mega-plan.md          # Define estructura completa, template, progresión
progress.json         # Tracking de estado de cada tema (pending/completed)
generate_template.py  # Template HTML base con CSS + JS
INDEX.html            # Navegación principal
├── tema-01.html
├── tema-02.html
├── ...
└── tema-53.html
```

## Componentes del cron

### Cron generador
- **Trigger:** recurrente (cada 5-10 min)
- **Prompt:** incluye el ID del tema actual + el template HTML
- **Acciones:**
  1. `skill_view(name='stem/td/<skill>')` para cargar conocimiento
  2. `read_file()` para template
  3. `write_file()` para generar HTML completo
  4. `cronjob(action='update')` para actualizar prompt con siguiente tema
  5. Git commit + push

### Cron verificador
- **Trigger:** diario (02:00 UTC)
- **Acciones:**
  1. Listar HTMLs generados
  2. Verificar: SVG presente, ≥3 ejercicios, navegación, atribución
  3. Reporte de errores
  4. Git push

## Reglas de diseño

1. **Cada tema tiene su skill fuente** — el cron lee el skill como referencia
2. **Progresión estricta** — no saltar temas, cada uno construye sobre el anterior
3. **SVG interactivo SIEMPRE** — no imágenes estáticas, elementos clicables
4. **Variedad de ejercicios** — quiz, completar hueco, V/F, identificar en SVG
5. **Un solo archivo HTML** — CSS y JS inline
6. **Atribución** — "Hecho con ❤️ por David Antizar"

## Cuándo usar este patrón

- Curso educativo con 20+ temas
- Cada tema tiene contenido bien definido en un skill
- Se quiere generar contenido masivo sin intervención manual
- El template HTML es consistente entre temas

## Cuándo NO usarlo

- Tema con contenido muy heterogéneo (no hay template único)
- Temas que necesitan revisión humana significativa
- Menos de 10 temas (mejor generar manualmente)
- El skill fuente no tiene estructura clara

## Lecciones aprendidas (2026-06-10)

- **El template debe ser flexible** — debe soportar diferentes tipos de SVG y ejercicios
- **progress.json es el cerebro** — sin tracking de estado, el cron no sabe qué hacer
- **El cron se auto-actualiza** — se actualiza a sí mismo con el siguiente tema, creando una cadena
- **El verificador diario es esencial** — detecta problemas que el generador puede pasar por alto
- **Mega-plan antes de crons** — definir toda la estructura antes de generar cualquier tema

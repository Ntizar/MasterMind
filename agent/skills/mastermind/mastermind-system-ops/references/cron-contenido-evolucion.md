# Crons de contenido generativo que se repiten → continuidad y evolución

**Problema:** un cron diario que hace escribir a un LLM un "capítulo"/escena/artículo seriado (p.ej. el *Café informal entre ministros* de Gobierno IA, job `0f0a44af121e`) tiende a **repetir el mismo tema central, las mismas voces y la misma escena** día tras día. La causa raíz NO es el modelo: es que el prompt arranca de cero cada día y no lee lo ya escrito. Un LLM no "recuerda" entre runs de cron — solo ve lo que el prompt le pasa.

## Señales de que el cron repite
- Mismo tema central (p.ej. "presupuestos inviables", "sequía", "guardias") en escenas consecutivas.
- Mismas frases/ambientación ("una cafetería de barrio lejos de Moncloa", "pagan con dos tarjetas y una moneda").
- El modelo **re-summariza o re-escribe un archivo antiguo** en vez de producir un día nuevo (síntoma: la salida cita una fecha vieja y el archivo de esa fecha aparece con mtime de hoy).

## El fix: 3 piezas
1. **Archivo de estado de trama** (`hilo.md` o similar): hilos abiertos, temas YA tratados (últimos N días), evolución de personajes, fechas clave próximas. Se lee al empezar y se ACTUALIZA al final de cada run.
2. **Prompt que obliga a avanzar.** ANTES de escribir, leer: el estado + los N últimos outputs + el "arco maestro" si lo hay (p.ej. `constitution/mision-30-sesiones.md`). Reglas explícitas en el prompt:
   - **NO repetir el tema central** de la escena anterior → solo *callback* en una frase.
   - **Avanzar al menos UNA trama y UN rasgo de personaje** por escena (una relación, un gesto recurrente, un cambio de humor, algo que se insinúa).
   - **Variar ambientación/estructura** (no siempre el mismo sitio a la misma hora: terraza, bar de estación, banco de parque, cocina, paseo).
   - Cerrar con **UNA verdad incómoda distinta** de la de ayer.
3. **Seguridad de archivo.** Fecha = `date +%F` (la REAL del día, no la del ejemplo). Escribir SIEMPRE en `<fecha-hoy>-cafe.md`; **NUNCA sobreescribir** un archivo existente ni pisar fechas antiguas (si `<fecha-hoy>` ya existe, sufijo `-2`/`-3`). Este es el fallo que pisó `2025-09-30-cafe.md` en 2026-09-07.

## Por qué funciona
Leer los outputs previos (ground truth real, lo más fiable) + un estado explícito (`hilo.md`) le da al modelo contexto para producir algo claramente más adelantado. El estado explícito es un acelerador; los outputs leídos son la fuente de verdad.

## Dónde vive el prompt de un cron
En `%LOCALAPPDATA%\hermes\cron\jobs.json`, campo `prompt` del job por su `id` (no `job_id`). Leer/editar el prompt completo con python json:

```python
import json
d = json.load(open(r'C:\Users\d_ant\AppData\Local\hermes\cron\jobs.json', encoding='utf-8'))
for j in d['jobs']:
    if j.get('id') == '<job_id>':
        print(j.get('prompt'))
```

Editar vía `cronjob action=update` (acepta `prompt` y `model`/`provider`...). Tras editar, **verificar el fix lanzando el cron** (`cronjob action=run` en background; el resultado re-entra en la conversación) y comprobar que escribe el archivo de la fecha de HOY y que el tema central difiere del día anterior.

## Aplicación verificada
- Gobierno IA *Café informal entre ministros* (2026-09-07): creado `ministerios/cafe/hilo.md` y reescrito el prompt. Antes: repetía "parálisis presupuestaria" y re-summarizaba la escena de 2025-09-30; después: escena nueva en `2026-09-07-cafe.md`.

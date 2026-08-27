---
name: hub-skill-discovery
description: "Descubrir, comparar y planificar la instalación de skills del hub oficial de Hermes Agent — escaneo del catálogo, comparación con skills instalados, priorización por relevancia y planificación de cron de aprendizaje."
version: "1.1.0"
tags: [hermes, skills, hub, discovery, learning, cron, automation]
---

# Hub Skill Discovery

Descubrir skills del hub oficial de Hermes Agent que no tenemos instalados, priorizarlos por relevancia y planificar su aprendizaje automático.

## Cuándo usar

- Cuando el usuario quiere expandir el conocimiento de Mastermind
- Cuando se actualiza Hermes y hay nuevos skills disponibles
- Para mantener el ecosistema de skills actualizado
- Cuando se pregunta "¿qué skills puedo instalar?"

## Pasos

### 1. Escanear skills instalados

```bash
/opt/hermes/.venv/bin/hermes skills list
```

Parsear la salida para obtener la lista de nombres de skills instalados.

### 2. Escanear hub oficial

```bash
# Page 1
/opt/hermes/.venv/bin/hermes skills browse --page 1
# Pages 2-5
/opt/hermes/.venv/bin/hermes skills browse --page 2
# ... hasta page 5
```

El hub tiene **89 skills opcionales** oficiales de Nous Research.

También consultar el catálogo bundled:
```bash
curl -s "https://hermes-agent.nousresearch.com/docs/reference/skills-catalog"
```

### 3. Comparar y calcular diferencia

```python
# Comparar listas:
# - Installed: lista de nombres de skills locales
# - Hub: lista de nombres del catálogo oficial
# - Missing = Hub - Installed
```

**Nota:** Los nombres pueden truncarse con `…` en la salida TUI. Normalizar comparando sin los puntos suspensivos.

### 4. Priorizar por relevancia

Clasificar los skills faltantes en 3 niveles:

- **🔥 Alta prioridad:** Skills que complementan directamente el stack actual (web dev, data, ESIOS, creative, MLOps, GitHub, automation)
- **📦 Media prioridad:** Skills útiles pero menos críticos (productividad, investigación, herramientas específicas)
- **🗄️ Baja prioridad:** Skills muy nicho (blockchain, gaming, bioinformática, hardware específico)

### 5. Planificar cron de aprendizaje

Crear un cron job que instale 1 skill cada 6h (NO cada hora — saturación de contexto):

```bash
hermes cron create "every 6h"  # cada 6 horas
```

El cron debe usar `no_agent=False` con script `skill-learning.sh` + prompt de resumen.

#### Script `skill-learning.sh` — estado persistente

El script de instalación está en `scripts/skill-learning.sh`. **Reglas críticas de estado:**

1. **NUNCA usar redirección a `/dev/null` en `save_state`** — el bug clásico es `echo "$state" > "$tmpfile" 2>/dev/null` que pierde el stdout. Usar redirección directa: `echo "$state" > "$STATE_FILE"`.
2. **Escribir JSON atómicamente** — usar `tmpfile + mv` para evitar lecturas de estado corrupto.
3. **Usar `python3 -c "import json"` para parsear/guardar** — el bash puro no tiene JSON nativo y falla silenciosamente.
4. **Siempre avanzar `current_index` tras cada ejecución** (éxito o fallo) — evitar bucles infinitos.
5. **Estado en `agent/skills/.skill-learning-state.json`** con campos: `current_index`, `learned[]`, `skipped[]`, `last_error`.

#### Prompt del cron

Tras instalar, el cron debe generar un resumen breve del skill (qué hace, por qué es relevante para David). No repetir el mismo skill.

### 6. Guardar referencia

Documentar en `references/hub-skill-audit-YYYY-MM-DD.md`:
- Skills totales del hub
- Skills instalados
- Skills faltantes
- Priorización aplicada
- Decisiones tomadas

## Pitfalls

- **NUNCA instalar todos de golpe** — saturaría el contexto y no hay tiempo de aprenderlos
- **Priorizar siempre por relevancia** — no instalar por instalar
- **El path del CLI de Hermes puede variar** — verificar con `find / -name "hermes" -type f 2>/dev/null`
- **`hermes` puede no estar en PATH** — usar `/opt/hermes/.venv/bin/hermes` o `$HERMES_HOME`
- **Los nombres truncados con `…`** — normalizar antes de comparar
- **Skills bundled vs optional** — los bundled ya vienen con Hermes, los optional hay que instalarlos
- **Script `skill-learning.sh` con estado persistente corrupto** — el bug clásico era usar `2>/dev/null` en `save_state` perdiendo el JSON, lo que causaba bucle infinito reinstalando el mismo skill. Fix: escribir atómicamente con `tmpfile + mv`, usar `python3` para JSON, siempre avanzar `current_index`. Script actualizado en `scripts/skill-learning.sh` v2.
- **Timeout del script deja skills en `.hub/quarantine/` sin instalar Y NO avanza el índice** — si el script timeout (120s), ni el path de éxito ni el de error se ejecutan: el skill se descarga pero no se mueve, Y el `current_index` NO se incrementa. Resultado: bucle infinito reintentando el mismo skill. **2026-06-09 confirmado:** el skill `fastmcp` quedó en cuarentena y el cron saltó el siguiente. Verificar con `ls agent/skills/.hub/quarantine/` y si hay un skill en cuarentena, forzar avance del índice manualmente: editar `agent/skills/.skill-learning-state.json` → `current_index` += 1. O mover manualmente el skill desde quarantine a su destino.
- **Reinstalación infinita del mismo skill** — si un skill se reinstala >3 veces en el mismo índice, revisar el estado en `.skill-learning-state.json`. El bug de `duckduckgo-search` (20 reinstalaciones antes de avanzar) se resolvió con el fix de estado atómico, pero hay que monitorizar que el `current_index` avance en cada tick del cron.
- **El script usa `no_agent=False` con `context_from`** — cada tick del cron es una sesión aislada sin contexto de chat. El prompt debe ser autocontenido. Si el script depende de variables de sesión, fallará silenciosamente.
- **2026-06-09: Saltar skills problemáticos** — si un skill causa timeout repetidamente, marcarlo como `skipped` en el estado y saltarlo. No vale la pena reintentar un skill que consistently falla — mejor documentarlo y avanzar.

## Diagnóstico y reparación de skills atascados

Cuando un cron tick timeout (120s) deja un skill en `.hub/quarantine/` sin avanzar el índice, se produce un bucle infinito. **Procedimiento de reparación:**

1. **Ejecutar diagnóstico:** `bash agent/skills/hub-skill-discovery/scripts/diagnose-stalled-skill.sh`
2. **Limpiar cuarentena:** `rm -rf agent/skills/.hub/quarantine/<skill>`
3. **Avanzar índice:** editar `agent/skills/.skill-learning-state.json` → `current_index += 1`
4. **Marcar como skipped:** añadir el nombre a `skipped[]` en el estado

**Comando rápido para saltar el skill actual:**
```bash
python3 -c "import json; d=json.load(open('agent/skills/.skill-learning-state.json')); d['skipped'].append('SKILL_NAME'); d['current_index']+=1; json.dump(d,open('agent/skills/.skill-learning-state.json','w'),indent=2)"
```

## Recursos

- Script de aprendizaje: `references/skill-learning-script.md` — documentación del script `skill-learning.sh`, patrón de estado persistente atómico, pitfalls y versionado
- Catálogo bundled: `references/bundled-skills-catalog.md`
- Catálogo optional: `references/optional-skills-catalog.md`
- Audit de cada sesión: `references/hub-skill-audit-YYYY-MM-DD.md`
- Skill atascado: `references/stalled-rest-graphql-debug.md` — rest-graphql-debug en cuarentena, 4 intentos fallidos, fix manual
- **Script diagnóstico:** `scripts/diagnose-stalled-skill.sh` — detecta skills estancados, cuarentena, y reintentos repetidos en las últimas 48h

## Sistema de Índice de Skills (Skill Index Pattern)

Sistema de búsqueda eficiente de skills mediante índice JSON + script de búsqueda. Reemplaza el escaneo manual de todas las skills con un índice indexado por tags.

### Problema que resuelve

Antes del índice, el agente recibía las descripciones de TODAS las skills (143+) en el prompt, consumiendo ~50KB de contexto. Con el índice:
- Índice de solo ~2KB en el prompt
- Búsqueda por tags con script dedicado
- Solo se cargan las skills relevantes

### Estructura

```
agent/skills/
├── index.json              ← Índice generado automáticamente
├── scripts/
│   ├── generate-skill-index.sh  ← Genera el índice
│   └── find-skills.sh           ← Busca por tag/palabra clave
```

### Uso

**Generar índice:**
```bash
bash scripts/generate-skill-index.sh
```
Genera `agent/skills/index.json` con: total_skills, categories, tags, skills (name, description, tags, category, path, size_bytes).

**Buscar skills:**
```bash
bash scripts/find-skills.sh "esios deploy"
bash scripts/find-skills.sh "dashboard"
```

**Algoritmo de búsqueda:** Cada palabra del query se evalúa por separado con scoring:
- Exact match en nombre: 100 puntos
- Partial match en nombre: 50 puntos
- Exact match en tag: 80 puntos
- Partial match en tag: 40 puntos
- Partial match en descripción: 20 puntos
- Partial match en categoría: 15 puntos

### Pitfalls
- **Heredoc bash vs variables Python:** Cuando usas `<< PYEOF` (sin comillas), bash expande `$VARIABLES`. Usa `<< 'PYEOF'` (con comillas) para deshabilitar expansión.
- **Índice desactualizado:** Si instalas nuevas skills, regenera el índice.
- **61 de 143 skills sin tags manuales:** Las skills sin tags manuales reciben tags automáticos: `[categoria, nombre_skill]`. Idealmente, todas deberían tener tags manuales.

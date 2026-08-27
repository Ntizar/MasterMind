# Auditoría Mensual del Ecosistema de Skills — 2026-07-01

## 📊 Panorama General

| Métrica | Valor |
|---------|-------|
| **Total skills** | 238 |
| **Categorías** | 44 |
| **Tamaño total** | 2.54 MB (SKILL.md files) |
| **Con versión** | 189 (79%) |
| **Sin versión** | 49 (21%) |
| **Con tags manuales** | 0 (0%) |
| **Sin tags** | 238 (100%) |
| **>30KB** | 17 skills |
| **>50KB** | 6 skills |
| **>100KB** | 1 skill |

## ✅ Lo que está MUY BIEN

1. **Índice regenerado** — El index.json estaba stale (143 skills vs 238 reales, delta 95). Se ha regenerado con los 238 skills y 44 categorías.
2. **Sin duplicados de contenido** — Los 238 skills tienen descripciones únicas. No hay skills que cubran exactamente lo mismo.
3. **Sin CLI wrappers** — No se detectaron skills con >3 curl commands y <5KB (los que deberían eliminarse).
4. **Sin skills near-empty** — Todos los skills tienen contenido sustancial (>1KB mínimo).
5. **Sin secrets expuestos** — Los únicos "sk-" encontrados son placeholders de ejemplo en native-mcp (sk-xxx...xxxx), no credenciales reales.
6. **Sin duplicados de nombre** — Solo 1 duplicado: `static-digest-pipeline` (frontend-dashboard-patterns + devops).

## ⚠️ Problemas detectados

### 🔴 Críticos

1. **Index.json stale (95 skills sin indexar)**
   - El índice tenía 143 skills cuando había 238 en disco
   - 11 categorías faltaban en el índice
   - **Acción tomada:** ✅ Regenerado con los 238 skills y 44 categorías

### 🟡 Importantes

2. **100% de skills sin tags manuales**
   - Los 238 skills carecen de tags manuales
   - Reciben auto-tags `[categoria, nombre]` que son poco útiles para búsqueda semántica
   - ChromaDB depende de tags para scoring
   - **Recomendación:** Añadir tags manuales a los 20+ skills más usados

3. **49 skills sin versión** (21%)
   - Principalmente en `stem/` (matemáticas, física, TD, ingeniería)
   - También en `mastermind/` y `ia/`
   - Sin versionado es difícil trackear evolución

4. **1 duplicado de nombre: `static-digest-pipeline`**
   - `frontend-dashboard-patterns/static-digest-pipeline` (2.5KB, versión 1.0.0, descripción corta)
   - `devops/static-digest-pipeline` (5.4KB, versión 1.0.0, descripción completa)
   - El de `frontend-dashboard-patterns` es una versión simplificada/derivada
   - **Recomendación:** Fusionar o eliminar el duplicado

5. **Quarantine stale: `fastmcp` (21 días)**
   - Llevaba 21 días en cuarentena sin resolución
   - **Acción tomada:** ✅ Eliminado

6. **Curator backups acumulados (14 MB)**
   - 5 backups, de los cuales 3 tenían >15 días
   - **Acción tomada:** ✅ Mantener solo los 2 más recientes (8 y 1 días)

7. **Index-cache huérfano (38 MB)**
   - `hermes-index.json` en `.hub/index-cache/` sin referencias
   - **Acción tomada:** ✅ Eliminado

### 🟢 Menores

8. **17 skills >30KB** (deberían usar refs pattern)
   - `frontend-dashboard-patterns` (101KB) — el más grande
   - `audit-html-project` (64KB)
   - `routing-isochrones` (62KB)
   - `government-data-pipelines` (59KB)
   - `esios/esios-nan-deploy` (57KB)
   - **Recomendación:** Mover contenido extenso a `references/` y referenciarlo

9. **18 skills con >5 paths absolutos** (project-readme suspects)
   - `devops/mastermind-setup` (106 paths absolutos) — el más severo
   - `mastermind/stars-explorer` (31 paths)
   - **Recomendación:** Revisar si los paths absolutos son necesarios o pueden ser relativos

10. **Script `generate-skill-index.sh` inexistente**
    - La documentación referencia un script que no existe en `agent/skills/scripts/`
    - El índice se generaba manualmente antes
    - **Recomendación:** Crear el script de generación automatizada

11. **23 categorías sin sub-skills** (directory-level skills)
    - Skills como `frontend-dashboard-patterns`, `mastermind`, `github-workflow`
    - Son skills monolíticos que podrían dividirse
    - **Recomendación:** No urgente, pero considerar fragmentación

## 💡 Acciones correctivas ejecutadas

| # | Acción | Impacto |
|---|--------|---------|
| 1 | ✅ Regenerar index.json | 143→238 skills indexados, 33→44 categorías |
| 2 | ✅ Eliminar quarantine fastmcp | Limpieza de 21 días de datos obsoletos |
| 3 | ✅ Limpiar curator backups | 14 MB → 6.5 MB (mantener 2 recientes) |
| 4 | ✅ Eliminar index-cache huérfano | 38 MB eliminados |
| 5 | **⏳ Fusionar static-digest-pipeline** | Requiere decisión manual |
| 6 | **⏳ Añadir tags a top-20 skills** | Mejora búsqueda semántica |

## 📈 Delta de limpieza

| Componente | Antes | Después | Ahorro |
|------------|-------|---------|--------|
| .hub/ | ~38 MB | 24 KB | **38 MB** |
| .curator_backups/ | ~14 MB | ~6.5 MB | **7.5 MB** |
| index.json | stale (143) | actualizado (238) | — |
| Total ahorrado | | | **~45.5 MB** |

## 📈 Veredicto global

**Puntuación: 6.5/10**

El ecosistema de skills creció de forma saludable: 238 skills en 44 categorías, sin duplicados de contenido y sin problemas de seguridad. Los problemas principales son de mantenimiento (index stale, tags ausentes, backups acumulados) que se han corregido en esta auditoría. El mayor trabajo pendiente es añadir tags manuales a los skills más usados para mejorar la búsqueda semántica de ChromaDB.

## 📋 Próximos pasos recomendados

1. **Alta:** Añadir tags manuales a los 20 skills más frecuentemente cargados
2. **Media:** Fusionar o eliminar `static-digest-pipeline` duplicado
3. **Media:** Crear script `generate-skill-index.sh` para automatización
4. **Baja:** Revisar 18 skills con paths absolutos excesivos
5. **Baja:** Añadir versión a los 49 skills sin versionar

---
*Generado automáticamente por Mastermind — 2026-07-01 00:00 UTC*

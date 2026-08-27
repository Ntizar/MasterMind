# Post-Migration Cleanup — Mastermind v3.1 → v4.0

**Fecha:** 2026-06-04
**Repo:** Ntizar/NtizarBrainMasterMind
**Migración:** v3.1 (OpenCode+Obsidian) → v4.0 (Hermes Agent+GitHub)

## Contexto

El proyecto NtizarBrainMasterMind migró de v3.1 a v4.0 el 2026-06-03 (commit `bc93756`). La migración movió 108 archivos legacy a `legacy/` y creó 28 nuevos. PERO quedaron **referencias residuales** en los archivos activos:

- `index.html` seguía mostrando v3.0 (11 agentes, Ebbinghaus, OpenCode)
- `CONTRIBUTING.md` instruía abrir como vault de Obsidian
- `README_EN.md` era documentación completa v3.1 en inglés
- `verify-system.sh` y `verify-system.bat` verificaban estructura v3.1
- `pages.yml` excluía paths de learning-platform y design-system
- `CHANGELOG.md` tenía contenido en inglés

## Escaneo

Se usó `os.walk()` en Python para buscar estos patrones en todos los archivos activos (excluyendo `.git/`, `legacy/`, `learning-platform/`):

```
patrones: ['obsidian', 'opencode', 'ebbinghaus', 'wikilink', '[[', 'slash command']
```

**Resultado:** 69 referencias en 11 archivos activos.

## Clasificación

| Archivo | Tipo | Acción |
|---------|------|--------|
| `index.html` | Landing page desactualizada | ✍️ Reescribir entera |
| `CONTRIBUTING.md` | Instrucciones activas obsoletas | ✍️ Reescribir entero |
| `CHANGELOG.md` | Contenido en inglés + referencias legacy | 🔄 Traducir y limpiar |
| `README_EN.md` | Documentación v3.1 en inglés | ✍️ Reescribir (redirigir al README español) |
| `verify-system.sh` | Script de verificación v3.1 | 🔄 Reescribir para v4.0 |
| `verify-system.bat` | Script Windows obsoleto | 🗑️ Eliminar |
| `.github/workflows/pages.yml` | Excluía paths v3.1 | 🔄 Actualizar excludes |
| `SOUL.md` | Contexto de migración en tabla | ✅ Mantener |
| `AGENTS.md` | Contexto de migración en tabla | ✅ Mantener |
| `README.md` | Contexto de migración en tabla | ✅ Mantener |
| `docs/ARCHITECTURE.md` | Contexto de migración en tablas | ✅ Mantener |

## Ejecución

### index.html (reescritura completa)

Cambios clave:
- **Hero**: de "11 agentes especializados" a "1 orquestador + 143 skills especializados"
- **Stats**: de "11 agentes" a "1 orquestador"
- **Sección de agentes**: reemplazada por grid de 8 dominios de skills
- **Arquitectura**: de "dos capas (Obsidian+OpenCode)" a "una capa (GitHub Markdown)"
- **Stack**: añadida sección Hermes + NaN.builders + GitHub
- **Badge**: de v3.0 a v4.0
- **Comparativa**: simplificada, sin referencia a versiones anteriores como sistema activo

### CONTRIBUTING.md (reescritura completa)

- Eliminadas instrucciones de Obsidian vault y OpenCode
- Nuevo formato: explicar que el proyecto es Hermes-native
- Secciones: cómo añadir skills, mejorar documentación, reportar bugs
- TODO en castellano

### CHANGELOG.md (traducción + limpieza)

- Cabecera "Keep a Changelog" → "Keep a Changelog" (versión en español)
- Todas las descripciones a castellano
- Se añadió entrada del index.html en "Cambiado"
- Sección v3.1 mantenida como histórico

### README_EN.md

- Reescribir completamente: solo un redirect a README.md
- Badges y contenido extenso eliminados (proyecto es español-only)

### verify-system.sh

- De verificar 11 agentes + .opencode/commands/ a verificar core files
- Nuevos checks: SOUL.md, AGENTS.md, docs/, index.html
- Eliminadas referencias a agents/, .opencode/

### verify-system.bat

- Eliminado completamente (obsoleto, solo Windows)

### pages.yml

- Excluidos: legacy/, docs/, assets/ en vez de agentes individuales
- Simplificado

## Commit

```
feat: v4.0 limpieza completa del proyecto

- index.html: landing reescrita para v4.0 Hermes-native (1 orquestador + 143 skills)
- CHANGELOG.md: traducido a castellano
- CONTRIBUTING.md: actualizado a v4.0 (sin Obsidian/OpenCode)
- README_EN.md: simplificado, redirige al README en español
- verify-system.sh: actualizado para v4.0
- verify-system.bat: eliminado (obsoleto para v4.0)
- pages.yml: actualizado excludes para v4.0
- Eliminadas todas las referencias activas a Obsidian/OpenCode/Ebbinghaus
```

**Stats:** 7 archivos cambiados, 332 líneas añadidas, 984 eliminadas.

## Lecciones

1. **El escaneo es lo más importante** — sin buscar sistemáticamente, te saltas archivos
2. **No todo hay que eliminarlo** — las referencias en tablas de migración dan contexto valioso
3. **Los scripts de verificación son los que más se olvidan** — suelen quedar apuntando a estructura antigua
4. **Landing pages y archivos de contribución son los que más daño hacen** — son la cara del proyecto
5. **Siempre hacer escaneo post-commit** para confirmar que no quedan residuales
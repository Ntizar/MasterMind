---
name: system-verification-portability
description: Patrón de verificación y portabilidad del sistema. Script cross-platform que verifica 8 capas. .gitignore categorizado. Instalación en 6 pasos.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [verificación, portabilidad, cross-platform, instalación, script, gitignore]
---

# Patrón de Verificación y Portabilidad del Sistema

## Qué es

Patrón que asegura que el sistema funciona de forma idéntica en cualquier plataforma (Linux, macOS, WSL, Windows) mediante:

1. **Script de verificación cross-platform** que comprueba 8 capas del sistema
2. **`.gitignore` categorizado** que funciona en todos los entornos
3. **Reglas de portabilidad** que garantizan que todo el sistema use rutas relativas
4. **Procedimiento de instalación en 6 pasos** para configurar el sistema en un nuevo ordenador

### Las 8 capas verificadas

| # | Capa | Qué verifica | Herramienta |
|---|------|-------------|-------------|
| 1 | **Estructura** | Carpetas y archivos esenciales existen | `test -d` / `Test-Path` |
| 2 | **Agentes** | Todos los agentes tienen ejecutable correspondiente | Comparación de listas |
| 3 | **Skills** | Todos los skills referenciados existen | Búsqueda de wikilinks |
| 4 | **Clusters** | `_clusters.md` referencia clusters existentes | Validación de frontmatter |
| 5 | **Learnings** | Cada learning tiene decay y clusters | Validación de frontmatter |
| 6 | **Configuración** | `.opencode/` tiene configuración válida | Parseo YAML |
| 7 | **Comandos** | Todos los comandos existen y son ejecutables | `test -x` / `Test-Path` |
| 8 | **Portabilidad** | No hay rutas absolutas en el sistema | Búsqueda de `/` y `C:\` |

## Cuándo usar

- Antes de compartir el sistema en un nuevo ordenador
- Después de migrar el sistema a una nueva plataforma
- Antes de hacer un commit importante (verificar que todo está en orden)
- Cuando un agente reporta errores de rutas o archivos no encontrados
- Como parte del proceso de instalación en un nuevo entorno

## Pasos

### Paso 1 — Ejecutar el script de verificación

**En Linux/macOS/WSL:**

```bash
./verify-system.sh
```

**En Windows (CMD):**

```cmd
verify-system.bat
```

El script verifica las 8 capas y reporta errores:

```
═══════════════════════════════════════
  VERIFICACIÓN DEL SISTEMA — Ntizar Brain
═══════════════════════════════════════

[1/8] Estructura ............ ✅ OK
[2/8] Agentes ............... ✅ OK (11/11)
[3/8] Skills ................ ✅ OK (6/6)
[4/8] Clusters .............. ✅ OK (12/12)
[5/8] Learnings ............. ⚠️  WARNING (32/33)
      - learnings/old-pattern.md: sin clusters en frontmatter
[6/8] Configuración ......... ✅ OK
[7/8] Comandos .............. ✅ OK (4/4)
[8/8] Portabilidad .......... ✅ OK

Resultado: 7/8 OK, 1 WARNING
```

### Paso 2 — Corregir errores

Si el script reporta errores, corregirlos antes de continuar:

```bash
# Ejemplo: learning sin clusters
# Añadir clusters al frontmatter del learning
---
clusters: [frontend, css, layout]
---
```

### Paso 3 — Verificar reglas de portabilidad

Asegurar que **solo se usan rutas relativas** en todo el sistema:

```
✅ Correcto: "../learnings/auth-patterns"
✅ Correcto: "agents/05-implementer.md"
✅ Correcto: "learnings/_index.md"

❌ Incorrecto: "/home/user/project/learnings/auth-patterns"
❌ Incorrecto: "C:\Users\user\project\agents\05-implementer.md"
❌ Incorrecto: "C:\Users\user\project\learnings\_index.md"
```

El script de verificación (capa 8) busca automáticamente rutas absolutas.

### Paso 4 — Revisar el .gitignore

El `.gitignore` está categorizado por tipo de archivo:

```gitignore
# ── Obsidian ─────────────────────────────
.obsidian/
*.obsidian/
__pycache__/

# ── OpenCode ─────────────────────────────
.opencode/
!.opencode/.gitkeep

# ── Sistema Operativo ────────────────────
.DS_Store
Thumbs.db
desktop.ini

# ── IDEs ─────────────────────────────────
.vscode/
.idea/
*.swp
*.swo

# ── Build ────────────────────────────────
dist/
build/
*.min.js
*.min.css

# ── Variables de entorno ─────────────────
.env
.env.local
.env.*.local

# ── Logs ─────────────────────────────────
*.log
logs/

# ── Temp ─────────────────────────────────
*.tmp
*.temp
*.bak
```

### Paso 5 — Verificar instalación

Después de clonar en un nuevo ordenador, ejecutar:

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd NtizarBrainMasterMind

# 2. Verificar estructura
./verify-system.sh  # o verify-system.bat en Windows

# 3. Corregir cualquier warning

# 4. Configurar el modelo por defecto en .opencode/config.yaml

# 5. Probar con una tarea pequeña

# 6. Verificar que todo funciona
./verify-system.sh
```

### Paso 6 — Instalación en nuevo ordenador (6 pasos)

| Paso | Acción | Comando |
|------|--------|---------|
| **1** | Clonar repositorio | `git clone <url>` |
| **2** | Entrar al directorio | `cd NtizarBrainMasterMind` |
| **3** | Verificar sistema | `./verify-system.sh` (Linux/macOS) o `verify-system.bat` (Windows) |
| **4** | Corregir warnings | Editar archivos según reporte del script |
| **5** | Configurar modelo | Editar `.opencode/config.yaml` con el modelo deseado |
| **6** | Primera ejecución | Abrir OpenCode y probar con una tarea simple |

## Pitfalls

- **Rutas absolutas en wikilinks:** Nunca usar rutas absolutas en wikilinks o referencias. Siempre rutas relativas desde la ubicación del archivo.
- **Rutas con backslashes:** En Windows, usar siempre `/` en wikilinks, no `\`. Obsidian y OpenCode resuelven `/` correctamente en Windows.
- **Ignorar warnings del script:** Un warning en la capa de learnings (learning sin clusters) puede causar que el learning no se cargue en la memoria. Siempre corregir.
- **.gitignore incompleto:** No añadir archivos de configuración personales al repo. Si un archivo funciona en tu máquina pero no en otra, probablemente está siendo versionado por error.
- **Script no ejecutable en Linux/macOS:** Después de clonar, asegurar que el script es ejecutable: `chmod +x verify-system.sh`.
- **Diferencias de línea:** No usar `CRLF` en Linux o `LF` en Windows. Configurar Git con `core.autocrlf=true` en Windows y `core.autocrlf=input` en Linux/macOS.

## Verificación

1. ✅ El script de verificación pasa las 8 capas sin errores (warnings corregidos)
2. ✅ No hay rutas absolutas en ningún archivo del sistema
3. ✅ El `.gitignore` cubre todas las categorías: Obsidian, OpenCode, OS, IDE, Build, Env, Logs, Temp
4. ✅ El script funciona en la plataforma actual (Linux, macOS, WSL o Windows)
5. ✅ La instalación en un nuevo ordenador se completa en 6 pasos sin errores
6. ✅ Todos los agentes tienen ejecutable correspondiente en `.opencode/agents/`
7. ✅ Todos los skills referenciados existen en `skills/`

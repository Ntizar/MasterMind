---
name: open-source-release
version: "1.0.0"
description: "Procedimiento para preparar un proyecto personal para publicación open-source — sanitizar datos personales, limpiar referencias, crear template genérico, y generar guía de instalación."
tags: [open-source, template, sanitization, privacy, release, public-repo]
---

# Open Source Release — Preparar Proyecto para Público

## Resumen

Procedimiento sistemático para tomar un proyecto personal con datos reales y convertirlo en un template público seguro, sin fugas de datos personales ni credentials.

## Cuándo usar

- Usuario quiere compartir un proyecto personal como template open-source
- Convertir un proyecto privado en público sin exponer datos personales
- Crear un "fork template" de un proyecto propio
- Generar guía de instalación para la comunidad

## Flujo de Trabajo (7 pasos)

### Paso 1: Inventario del proyecto

Identificar TODOS los archivos que pueden contener datos sensibles:
- `.env` — API keys, tokens, passwords
- `database.json` / `.sqlite` / `.db` — datos personales del usuario
- `README.md` — puede contener nombres, datos personales, URLs privadas
- `server.js` / backend — referencias a repos privados, endpoints internos
- `dashboard.html` / frontend — nombres hardcodeados, datos en HTML
- Archivos de config — `config.yaml`, `settings.json`

### Paso 2: Crear directorio template

```bash
mkdir -p /root/workspace/NOMBRE-template/data /root/workspace/NOMBRE-template/scripts
```

**NUNCA modificar el proyecto original** — trabajar siempre en copia.

### Paso 3: Sanitizar datos personales

#### 3a. Base de datos → estructura vacía

Crear `database.json` con la misma estructura pero:
- Campos vacíos o valores placeholder (`"Tu Nombre"`, `90`, `80`)
- Arrays vacíos (`"peso": []`, `"comidas": []`)
- Mantener la misma forma JSON para que el frontend funcione

#### 3b. Backend (server.js)

Reemplazar:
- Referencias a repos privados → genéricos o configurables
- Nombres de personas → genéricos ("Usuario", "Coach IA")
- Endpoints internos → eliminar o hacer opcionales
- Nombres de proyecto → genéricos ("FitTrack" en vez de "KoldoFit")

#### 3c. Frontend (dashboard.html)

Reemplazar:
- Nombres de personas → genéricos
- Referencias a APIs privadas → genéricas
- Textos personalizados → placeholders
- Footer de atribución → genérico

#### 3d. Documentación (README.md)

Reescribir completamente:
- Título genérico
- Descripción del proyecto sin datos personales
- Guía de instalación paso a paso
- Instrucciones de configuración
- Ejemplos con valores placeholder

### Paso 4: Verificación de seguridad (CRÍTICO)

Escaneo automático con regex para detectar fugas:

```python
import os, re

checks = {
    'Nombres personales': [r'David', r'Ntizar', r'Antizar', r'Amadeo'],
    'API Keys reales': [r'sk-[a-zA-Z0-9]{20,}'],
    'Emails': [r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'],
}

for root, dirs, files in os.walk(template_dir):
    if 'node_modules' in root: continue
    for fname in files:
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', errors='ignore') as f:
            content = f.read()
        for category, patterns in checks.items():
            for pat in patterns:
                matches = re.findall(pat, content, re.IGNORECASE)
                for m in matches:
                    # Filtrar falsos positivos (CDN público, .env.example)
                    if 'Ntizar/Aurora' in str(m): continue
                    if '.env.example' in fpath: continue
                    print(f"🔴 {category}: {m} en {fpath}")
```

### Falsos positivos aceptados:
- CDN de Aurora (`Ntizar/Aurora`) — es público, no es dato personal
- `NTIZAR_API` como nombre de variable de entorno — no contiene el token
- Referencias al autor original en créditos del README — es atribución, no fuga

## 6. Platform Migration — Migración entre Plataformas

Procedimiento para migrar un proyecto de una plataforma a otra (Obsidian→GitHub, OpenCode→Hermes, etc.): limpiar referencias legacy, actualizar documentación, verificar funcionalidad.

### Flujo de migración (6 pasos)
1. **Inventario**: identificar TODAS las referencias a la plataforma antigua
2. **Clasificar**: contexto histórico (mantener), instrucciones activas (reescribir), landing pages (reescribir), scripts (actualizar), config (migrar)
3. **Ejecutar cambios**: landing pages, docs contribución, CHANGELOG, scripts, workflows CI, SOUL.md
4. **Escaneo post-cambios**: `search_files` por todos los nombres de la plataforma antigua
5. **Verificación funcional**: confirmar que funciona con el nuevo stack
6. **Commit y push**

### Reglas
1. **NUNCA borrar el repo antiguo** — mover a `legacy/` con contexto
2. **SIEMPRE mantener contexto de migración** — tablas comparativas en SOUL.md
3. **Escaneo post-migración obligatorio** — `search_files` por residuales
4. **Documentación en castellano** — TODO en castellano, NUNCA inglés

### Pitfalls
- Las referencias residuales son silenciosas — un `grep` simple no basta
- Los scripts de verificación son los que más se olvidan
- Landing pages y CONTRIBUTING son los que más daño hacen

## 4b. Sanitización Avanzada — Escaneo Completo

Procedimiento extendido para sanitización profunda (absorbido de `open-source-sanitization`).

### Escaneo de datos sensibles
```bash
# Referencias personales
grep -rni -E '(nombre_real|apellidos|email|teléfono|dirección|DNI)' --include='*.js' --include='*.py' --include='*.md' --include='*.json' --include='*.html' --include='*.css' .

# API keys y tokens
grep -rni -E '(sk-[a-zA-Z0-9]{20,}|Bearer|api_key|token|secret)' --include='*.js' --include='*.py' --include='*.json' --include='*.html' .

# Credenciales hardcodeadas
grep -rni -E '(password|passwd|pwd|auth)' --include='*.js' --include='*.py' --include='*.json' .

# URLs privadas
grep -rni -E '(apps\.nan\.builders|internal\.|private\.|localhost:\d+)' --include='*.js' --include='*.html' .
```

### Archivos críticos a revisar uno por uno
| Archivo | Qué limpiar |
|---------|-------------|
| `data/database.json` | **CRÍTICO**: eliminar TODOS los datos personales. Dejar solo estructura vacía con valores placeholder |
| `server.js` / backend | Quitar nombres propios, referencias a personas, repos privados, endpoints hardcodeados |
| `dashboard.html` / frontend | Quitar nombres, fotos, datos personales, mensajes personalizados |
| `README.md` | Reescribir como guía de instalación genérica, no como diario personal |
| `.env` | **NUNCA** incluir. Crear `.env.example` con instrucciones |
| `package.json` | Verificar que no hay autores/personal |
| `Dockerfile` | Genérico, sin rutas absolutas |

### Patrón de limpieza por tipo de dato

#### Datos personales en JSON
```json
// ANTES (personal):
{"meta": {"nombre": "David Antizar", "altura_cm": 174, "peso_inicial_kg": 98.6}}
// DESPUÉS (template):
{"meta": {"nombre": "Tu Nombre", "altura_cm": 174, "peso_inicial_kg": 90}}
```

#### Endpoints hardcodeados
```javascript
// ANTES:
const getRes = await fetch('https://api.github.com/repos/Ntizar/dieta/contents/data/database.json', ...);
// DESPUÉS:
const repoOwner = process.env.GITHUB_REPO_OWNER || 'TU_USUARIO';
```

### CRÍTICO: Verificar historial de git
Si hay commits previos con datos personales en el historial, hacer `git filter-branch` o crear repo desde cero.

### Archivos que SIEMPRE incluir
| Archivo | Propósito |
|---------|-----------|
| `.gitignore` | Excluye `.env`, `node_modules/`, archivos de build |
| `.env.example` | Plantilla con instrucciones, **sin tokens reales** |
| `README.md` | Guía de instalación paso a paso, NO diario personal |
| `LICENSE` | Licencia del proyecto (MIT recomendado) |

### Archivos que NUNCA incluir
| Archivo | Por qué |
|---------|---------|
| `.env` | Contiene tokens/API keys reales |
| `data/database.json` (con datos) | Datos personales del usuario |
| `node_modules/` | Se regenera con `npm install` |

### Paso 5: Crear archivos de configuración

#### `.gitignore` robusto

```
node_modules/
npm-debug.log*
package-lock.json
# Variables de entorno — NUNCA subir a git
.env
```

#### `.env.example` con instrucciones

```
NAN_API=tu_token_aqui
GITHUB_REPO_OWNER=tu_usuario_github
GITHUB_REPO_NAME=tu_repo
```

**NUNCA incluir tokens reales en `.env.example`**.

#### `Dockerfile` genérico

Mismo que el original pero sin referencias a nombres específicos.

### Paso 6: Crear repositorio público

```bash
# Crear repo vía API GitHub
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"name":"NOMBRE","description":"Descripción genérica","public":true}'

# Clonar y subir archivos
git clone https://TOKEN@github.com/OWNER/NOMBRE.git
cd NOMBRE
# Copiar archivos del template
git add -A
git commit -m "Initial commit: NOMBRE template"
git push origin main
```

**Opcional:** Hacer squash de commits individuales:
```bash
git reset --soft $(git rev-list --max-parents=0 HEAD)
git commit -m "mensaje descriptivo"
git push --force origin main
```

### Paso 7: Generar guía de presentación

Crear texto para compartir con:
- Descripción del proyecto
- Lista de features
- Guía rápida de instalación (paso a paso)
- Link al repo
- Imagen/screenshot del dashboard

---

## Reglas de Seguridad

1. **NUNCA modificar el proyecto original** — siempre trabajar en copia
2. **NUNCA incluir API keys reales** en ningún archivo público
3. **`.env` SIEMPRE en `.gitignore`** — verificar antes de subir
4. **Base de datos vacía** — estructura pero sin datos
5. **Escaneo post-sanitización obligatorio** — regex por nombres, tokens, emails
6. **Atribución permitida** — referencias al autor original en créditos son OK
7. **CDN públicos OK** — referencias a `Ntizar/Aurora` en CSS/JS son OK (público)

## Pitfalls

- **Los nombres en el HTML son invisibles en el snapshot** — hay que buscar con regex, no confiar en la vista textual
- **El dashboard puede hardcodear datos en el `<script>`** — buscar JSON inline, no solo en `database.json`
- **`.env.example` no debe contener tokens** — solo el formato con `tu_token_aqui`
- **Las variables de entorno alternativas (`NTIZAR_API`) no son fugas** — son nombres de variable, no valores
- **Los commits individuales crean ruido** — hacer squash a un commit limpio antes de push
- **Los directorios `data/` y `scripts/` no se crean con la API de repos** — hay que subir los archivos con sus rutas completas (`data/database.json`, `scripts/registro.py`)

## Linked Files

- `references/open-source-release-dietan.md` — Caso real: sanitización de DietaNan para comunidad NaN.builders (checklist de datos sensibles, falsos positivos, comandos clave)

## 5. Plantilla Proyecto Público — Landing Page y Screenshot

Extensión de open-source-release: crear una landing page de presentación y screenshot del dashboard para la página del template.

### Flujo adicional
1. **Crear landing page** (`index.html`) con hero, feature cards, screenshot, CTA
2. **Generar screenshot**: levantar servidor local, capturar con `browser_vision`
3. **README como guía de instalación** con 10+ pasos, estructura del proyecto, solución de problemas

### Archivos mínimos del template
| Archivo | Propósito |
|---------|-----------|
| `index.html` | Landing page de presentación |
| `screenshot.png` | Captura del dashboard |
| `dashboard.html` | Dashboard principal |
| `server.js` | Backend genérico |
| `data/database.json` | Estructura vacía con placeholders |
| `.gitignore` | Protege .env |
| `.env.example` | Plantilla de config |
| `README.md` | Guía de instalación completa |

### Pitfalls
- Landing page con screenshot mejora la percepción de calidad enormemente
- El README debe ser autocontenido — alguien sin contexto debe poder instalarlo solo
- NO olvidar sanitizar prompts IA y dashboard.html (placeholders de texto)
- Verificar DOS VECES antes de subir: grep por nombre, email, API keys

# Validación de Sintaxis JS Inline en HTML Grandes

Técnicas para diagnosticar errores de sintaxis en archivos HTML con scripts inline masivos (>5000 líneas).

## 1. `vm.Script` — Validación de Sintaxis Completa

La herramienta más potente. Compila el script como si fuera un módulo JS y reporta el error exacto con línea y mensaje.

```javascript
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (scriptMatch) {
  try {
    new vm.Script(scriptMatch[1], { filename: 'index.html' });
    console.log('✅ SYNTAX OK');
  } catch(e) {
    console.log('❌ ERROR:', e.message);
    // El stack trace incluye la línea exacta del script inline
    console.log(e.stack.split('\n').slice(0, 3).join('\n'));
  }
}
```

**Ventaja sobre `node --check`:** `node --check` no puede validar scripts inline porque el escaping está diseñado para contexto HTML. `vm.Script` sí puede.

**Ventaja sobre brace counting:** Detecta TODOS los errores de sintaxis (no solo braces): `const` suelto, paréntesis desbalanceados, strings mal cerrados, etc.

## 2. Comparación de Brace/Paren Balance entre Versiones

Cuando un commit corrompe un archivo grande y no sabes DÓNDE empezó la divergencia, comparar el balance acumulado de `{`, `}`, `(`, `)` entre la versión vieja y la nueva localiza el punto exacto.

```javascript
const { execSync } = require('child_process');
const oldHtml = execSync('git show HEAD~1:index.html', { maxBuffer: 10*1024*1024 }).toString();
const newHtml = fs.readFileSync('index.html', 'utf8');

function getScript(html) {
  return html.match(/<script>([\s\S]*?)<\/script>/)[1].split('\n');
}

const oldS = getScript(oldHtml);
const newS = getScript(newHtml);

let ob = 0, nb = 0;
for (let i = 0; i < Math.max(oldS.length, newS.length); i++) {
  const ol = oldS[i] || '';
  const nl = newS[i] || '';
  for (const ch of ol) { if (ch === '{') ob++; if (ch === '}') ob--; }
  for (const ch of nl) { if (ch === '{') nb++; if (ch === '}') nb--; }
  
  if (ob !== nb) {
    console.log(`DIVERGENCE at line ${i+1}: old=${ob} new=${nb}`);
    console.log(`  OLD: ${ol.trim().substring(0, 100)}`);
    console.log(`  NEW: ${nl.trim().substring(0, 100)}`);
    break; // Primera divergencia
  }
}
```

**Uso:** Ejecutar y seguir las divergencias. La primera divergencia es donde el commit empezó a corromper. Las siguientes muestran el efecto cascada.

## 3. Búsqueda Binaria de Errores de Sintaxis

Cuando `vm.Script` reporta un error pero la línea no es obvia (porque el error es acumulativo), buscar binariamente la línea exacta:

```javascript
const script = scriptMatch[1];
const lines = script.split('\n');

let low = 1, high = lines.length;
while (low <= high) {
  const mid = Math.floor((low + high) / 2);
  const partial = lines.slice(0, mid).join('\n');
  try {
    new Function(partial);
    low = mid + 1;
  } catch(e) {
    if (low === high) {
      console.log(`ERROR at line ${mid}: ${lines[mid-1].substring(0, 120)}`);
      break;
    }
    high = mid;
  }
}
```

**⚠️ Trampa:** `new Function()` envuelve el código en una función, así que `const` a nivel de script puede dar falsos positivos. Usar `vm.Script` para la validación final.

## 4. Detección de Líneas Corrompidas por Merge/Patch

Patrón reconocible: dos líneas se fusionaron durante un `patch` o merge conflict resolution.

**Síntomas:**
- `const         // ===== SECTION NAME =====` — un `const` suelto antes de un comentario
- `});getElementById('xxx');` — cierre de callback + inicio de nueva declaración
- `// ===== NAME =====getElementById('xxx');` — comentario + variable sin declarar

**Detección:**
```bash
# Buscar líneas con // seguidas de código válido
grep -n "// ====.*[a-zA-Z]('.*');" index.html

# Buscar const/let/var seguidos de //
grep -n "const.*// ====" index.html
grep -n "let.*// ====" index.html
```

**Corrección:** Restaurar la línea original desde el commit anterior:
```bash
git show HEAD~1:index.html | sed -n 'NLp'  # ver línea original
```

## 5. Decisión: Revert vs Fix

Cuando un commit introduce corrupción masiva (>10 líneas corruptas, divergencia de brace balance en múltiples funciones):

| Criterio | Fix manual | Revert |
|----------|-----------|--------|
| Líneas corruptas | < 5 | > 5 |
| Funciones afectadas | 1-2 | 3+ |
| Brace balance diff | < 2 | ≥ 2 |
| Tiempo estimado fix | < 10 min | > 30 min |
| Riesgo de introducir nuevos bugs | Bajo | Ninguno |

**Regla:** Si el diff de brace balance entre versiones es ≥ 2, revert es más seguro. Cada `{` sin cerrar potencialmente rompe múltiples funciones.

```bash
# Revert seguro
git stash  # guardar cambios locales
git revert <commit-sha> --no-edit
git push origin main
```

## Checklist de Diagnóstico Rápido

Cuando un sitio HTML no carga (spinning, blank, errores en consola):

1. **Consola del navegador** → ¿Qué error muestra?
2. **`vm.Script`** → ¿Compila el script inline?
3. **`git log --oneline -5`** → ¿Qué cambió recientemente?
4. **`git diff HEAD~1 -- index.html | grep '^+'`** → ¿Qué se añadió?
5. **Comparación brace balance** → ¿Dónde empieza la divergencia?
6. **Decisión** → ¿Fix o revert?

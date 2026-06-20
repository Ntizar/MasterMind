# Patch Safety - Fuzzy Matching Pitfall

## El problema

La herramienta `skill_manage(action='patch')` y `patch()` usan **fuzzy matching** por texto. Si el `old_string` coincide con un bloque similar pero equivocado, el patch se aplica al bloque incorrecto **sin error de validación**.

## Caso real (2026-06-12, dieta-masterfit)

### Qué pasó

Un patch intentó reemplazar el cuerpo de `registrarDeporte` (función de ejercicio) pero el fuzzy match coincidió con el bloque de `registrarPasos` (función de pasos) que tenía una estructura similar (ambas eran handlers de eventos con `fetch`).

### Consecuencias

1. **`registrarDeporte` corrupto**: Ahora contenía código de pasos → el formulario de ejercicio enviaba datos incorrectos al endpoint `/api/pasos`
2. **`registrarPasos` ausente**: La función desapareció del archivo → el formulario de pasos fallaba al submit porque `onsubmit="return registrarPasos(event)"` llamaba a una función inexistente
3. **Ningún error de sintaxis**: El código era válido JavaScript pero semánticamente roto
4. **Silencioso**: El dashboard cargaba, los KPIs se mostraban, pero los formularios no funcionaban

## Reglas de seguridad

1. **NUNCA parchear sin leer el contexto ANTES del old_string** — verificar con `read_file` que el bloque es exactamente el correcto
2. **Incluir contexto suficiente en `old_string`** — al menos 3-5 líneas de código real, no solo el nombre de la función. Incluir el comentario anterior y las líneas de cierre
3. **Después de cada patch en HTML/JS grande, validar**:
   - `node -c server.js` para backend
   - `grep -c "function registrarPasos" dashboard.html` para verificar funciones clave
   - Contar braces `{` vs `}` para detectar desequilibrios
   - Contar event listeners duplicados
4. **Si el fuzzy match podría coincidir con múltiples bloques**, verificar que solo se modificó el bloque esperado
5. **Para archivos >100KB con cambios en múltiples ubicaciones**, preferir `write_file` con el contenido completo

## Verificación post-patch

```bash
# Validar JS backend
node -c server.js

# Verificar funciones clave existen
grep -c "function registrarPasos" dashboard.html
grep -c "function registrarDeporte" dashboard.html

# Verificar braces balanceados
python3 -c "c=open('dashboard.html').read(); print('OK' if c.count('{')==c.count('}') else 'MISMATCH')"

# Verificar event listeners únicos
grep -c "tab.addEventListener('click'" dashboard.html

# Verificar patrón charts
grep "var charts = window.charts" dashboard.html
```
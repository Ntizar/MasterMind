# Bulk HTML Insertion via Python `.replace()`

## Cuándo usarlo

- Archivo HTML > 20KB (write_file demasiado grande para copiar todo)
- Necesitas insertar 3+ bloques en posiciones distintas del archivo
- `patch()` sería propenso a errores de escape de newlines en JS
- Quieres hacer todos los cambios en un solo paso

## Patrón

```python
with open(file, 'r') as f:
    html = f.read()

# Definir cada bloque como string
block1 = '''
<div class="card"><h3>🧠 Ejercicios</h3>
...contenido...
</div>
'''

block2 = '''
<div class="teoria">🌍 Caso real: ...</div>
'''

# Insertar en posiciones específicas usando .replace()
html = html.replace(
    'texto_único_que_aparece_solo_antes_del_punto_1',
    'texto_único_que_aparece_solo_antes_del_punto_1' + block1
)
html = html.replace(
    'texto_único_que_aparece_solo_antes_del_punto_2',
    'texto_único_que_aparece_solo_antes_del_punto_2' + block2
)

# Escribir resultado
with open(file, 'w') as f:
    f.write(html)
```

## Claves

1. **Texto de anclaje único:** cada `.replace()` debe buscar un string que aparezca EXACTAMENTE una vez en el archivo (ej: el cierre `</div></div>\n\n<div class="chapter" id="ch1"`).
2. **Bloques con triple comilla:** usar `'''` para bloques multi-línea, no `"` (evita problemas de escape).
3. **Verificar post-insertión:** contar elementos clave (ejercicios, feedbacks, quiz-opt) para confirmar que todo se insertó.

## Pitfall: duplicación por anclaje auto-referencial (2026-06-10)

**Problema:** Si el bloque insertado contiene el mismo texto de anclaje que busca un `.replace()` posterior, ese anclaje aparecerá DOS veces (el original + el insertado). El `.replace()` posterior reemplazará la PRIMERA ocurrencia, que ahora está dentro del bloque insertado, duplicando contenido.

**Causa común:** Insertar un bloque que contiene `<div class="chapter">` y luego hacer `.replace('<div class="chapter">\n<h2 class="chapter-title">🌟 ¡Desafío final!</h2>', ...)` donde el nuevo bloque ya contiene esa misma estructura.

**Soluciones:**
1. **Insertar de abajo hacia arriba:** hacer primero el `.replace()` del anclaje más cercano al final del archivo, y así sucesivamente hacia el inicio. Así los bloques insertados no afectan los anclajes anteriores.
2. **Anclajes ultra-específicos:** usar strings que incluyan contenido único del bloque insertado (ej: el ID del ejercicio específico) para que no puedan aparecer accidentalmente en bloques insertados.
3. **Verificar duplicados post-insersión:** tras los `.replace()`, buscar `re.findall(r'Ejercicio 10', html)` y si hay más de 1, eliminar el duplicado.

## Ejemplo real (s03-3primaria.html, 2026-06-10)

Archivo de 30KB con 6 capítulos y 0 ejercicios. Se insertaron 15 ejercicios + 6 casos reales + 6 errores comunes usando 6 `.replace()` encadenados, cada uno insertando un bloque completo de ejercicios tras el resumen-card de su capítulo.

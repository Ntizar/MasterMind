# Verificación de contenido educativo HTML

Patrón para verificar automáticamente que las sesiones educativas cumplen los criterios de calidad.

## Script de verificación

```python
import os
import re

base = "/path/to/project"
html_files = [f for f in os.listdir(base) if f.endswith('.html') and f not in ('INDEX.html', 'index.html')]

latex_count = 0
plotly_count = 0
attribution_count = 0
errors = []

for f in sorted(html_files):
    path = os.path.join(base, f)
    with open(path, 'r') as fh:
        content = fh.read()
    
    has_katex = 'katex' in content.lower()
    has_plotly = 'plotly' in content.lower()
    has_attr = 'David Antizar' in content
    
    if has_katex: latex_count += 1
    if has_plotly: plotly_count += 1
    if has_attr: attribution_count += 1
    
    # Errores
    if re.search(r'href="#">\s*Siguiente', content):
        errors.append(f"  ❌ {f}: Siguiente → #")
    if re.search(r'href="#">\s*Anterior', content):
        errors.append(f"  ❌ {f}: Anterior → #")

print(f"Total archivos: {len(html_files)}")
print(f"Con KaTeX: {latex_count}")
print(f"Con Plotly: {plotly_count}")
print(f"Con atribución: {attribution_count}")
if errors:
    print(f"\n❌ ERRORES ({len(errors)}):")
    for e in errors:
        print(e)
else:
    print("\n✅ ¡TODOS CORRECTOS!")
```

## Criterios de "hecho"

Una sesión está completa cuando:

1. ✅ Tiene KaTeX para fórmulas LaTeX
2. ✅ Tiene al menos 1 gráfico interactivo con Plotly.js
3. ✅ Tiene al menos 3 ejercicios interactivos con feedback
4. ✅ Tiene un caso de uso real explicado
5. ✅ Tiene resumen final con los puntos clave
6. ✅ Tiene navegación Anterior/Siguiente funcional
7. ✅ Tiene atribución "Hecho con ❤️ por David Antizar"
8. ✅ Funciona en móvil y escritorio (responsive)
9. ✅ El contenido matemático es correcto y claro
10. ✅ La intuición viene antes que la fórmula

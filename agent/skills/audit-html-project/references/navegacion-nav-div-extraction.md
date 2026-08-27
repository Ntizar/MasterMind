# Navegación: extracción segura de `<div class="nav">`

## Problema

Los generadores de contenido educativo crean navegación en bloques como:

```html
<div class="nav">
  <a href="archivo-anterior.html">← Anterior</a>
  <a href="archivo-siguiente.html">Siguiente →</a>
</div>
```

Los scripts de auditoría que usan regex parciales fallan porque:
1. El orden de `<a>` en el HTML puede no coincidir con el orden textual
2. El texto "Anterior" puede aparecer DESPUÉS del href en algunos generadores
3. `href="#"` con texto "Anterior" puede confundirse con enlaces válidos

## Patrón seguro de extracción

```python
import re

def extract_nav_links(content):
    """Extraer enlaces Anterior/Siguiente de div.nav de forma segura."""
    nav_match = re.search(
        r'<div class="nav">\s*'
        r'<a href="([^"]+)"[^>]*>(.*?)</a>\s*'
        r'<a href="([^"]+)"[^>]*>(.*?)</a>\s*'
        r'</div>',
        content, re.DOTALL
    )
    
    if not nav_match:
        return None, None  # Sin navegación
    
    # Determinar cuál es Anterior y cuál Siguiente con ←/→
    link1 = nav_match.group(1)
    text1 = nav_match.group(2)
    link2 = nav_match.group(3)
    text2 = nav_match.group(4)
    
    if '←' in text1 or 'anterior' in text1.lower():
        return link1, link2  # link1 = Anterior, link2 = Siguiente
    else:
        return link2, link1  # link1 = Siguiente, link2 = Anterior
```

## Verificación de targets

```python
def verify_nav_links(src_file, prev_file, next_file, all_set):
    """Verificar que los targets de navegación existen."""
    issues = []
    if prev_file and prev_file not in all_set:
        issues.append(f"Anterior → {prev_file} (NO EXISTE)")
    if next_file and next_file not in all_set:
        issues.append(f"Siguiente → {next_file} (NO EXISTE)")
    return issues
```

## Casos especiales

### Primer archivo (sin Anterior)
```html
<div class="nav">
  <a href="#" class="disabled">← Anterior</a>
  <a href="siguiente.html">Siguiente →</a>
</div>
```
→ prev=None, next="siguiente.html"

### Último archivo (sin Siguiente)
```html
<div class="nav">
  <a href="anterior.html">← Anterior</a>
  <a href="INDEX.html">🏠 Volver al índice</a>
</div>
```
→ prev="anterior.html", next="INDEX.html" (o None si no hay "Siguiente")

### Navegación con 3 enlaces
```html
<div class="nav">
  <a href="anterior.html">← Anterior</a>
  <a href="INDEX.html">🏠 Índice</a>
  <a href="siguiente.html">Siguiente →</a>
</div>
```
→ Regex de 2 enlaces no captura esto. Usar patrón alternativo:
```python
nav_match = re.search(r'<div class="nav">(.*?)</div>', content, re.DOTALL)
if nav_match:
    links = re.findall(r'href="([^"]+\.html)"', nav_match.group(1))
    text = nav_match.group(1)
    # Determinar roles con ←/→/Índice
```

## Casos reales detectados

- **b03-04-caballera.html**: tiene `b03-05-piezas-caballera.html` (incorrecto) en vez de `b03-05-perspectivas-piezas.html`
- **b03-05-perspectivas-piezas.html**: tiene `b03-06-perspectivas-piezas.html` (incorrecto) en vez de `b03-06-perspectivas-resumen.html`
- **b05-01-cortes.html**: tiene `b05-02-corte-total.html` (incorrecto) en vez de `b05-02-corte-tipos.html`
- **b05-02-corte-tipos.html**: tiene `b05-03-semicorte-parcial.html` (incorrecto) en vez de `b05-03-corte-escalonado.html`

Todos son nombres de archivo incorrectos en enlaces "Siguiente", bien formados HTML pero apuntando a archivos inexistentes.

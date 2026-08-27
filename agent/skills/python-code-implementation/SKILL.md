---
name: python-code-implementation
description: Workflow y patrones para añadir funcionalidad sustancial (módulos nuevos, refactor grande, features) a codebases Python existentes. Incluye pitfalls de IDs duplicados, falsos positivos de linter, y reglas de cuándo usar subagentes vs directo.
---

# Python Implementation — Añadir funcionalidad grande a código existente

## Trigger

Cualquier tarea que implique añadir funcionalidad sustancial (500+ líneas, 2+ módulos nuevos, refactor importante) a un código Python existente. No para scripts simples de una pasada.

## Workflow numerado

1. **Audit** → `search_files` + `read_file` para entender estructura actual. Cuenta módulos, clases, tests existentes.
2. **Planificar módulos** → listar qué módulos nuevos crear vs qué ficheros existentes patchear.
3. **Implementar en paralelo** → `write_file` para nuevos módulos, `patch` para modificaciones. **EVIТАR subagentes** en codebases >500 líneas (timeout 9009).
4. **Verificar importaciones** → `python -c "from pkg.module import Class; print('✅')" ` ANTES de tests.
5. **Ejecutar tests** → `pytest tests/ -v --tb=short`
6. **Debug failures** → leer output de test, localizar línea exacta, patchear.
7. **Repetir 5-6** hasta 0 fallos.
8. **Commit limpio** → `git add -A` → `git commit -m "feat: title..."` → verificar con `git status`.

## Pitfalls críticos

### Fallo de IDs duplicados en estructuras múltiples
Cuando un método genera IDs para entidades que se llaman **varias veces** con los mismos parámetros, los IDs se duplican.

**Patrón bug:**
```python
def create_structures(self, zones):
    for zone_id in zones:
        # Este ID se repite en cada llamada del método
        fc_id = f"prefix:FC:{pub}:{zone_id}"  # ← siempre el mismo
```

**Fix:** Añadir `suffix` o `variant` al ID:
```python
def add_components(self, parent, zones, suffix=""):
    for zone_id in zones:
        if suffix:
            fc_id = f"prefix:FC:{pub}:{suffix}:{zone_id}"  # único por estructura
        else:
            fc_id = f"prefix:FC:{pub}:{zone_id}"
```

**Señal de alerta:** test de `assert len(ids) == len(set(ids))` falla → IDs duplicados.

### Falso positivo en Pyright con ElementTree
`Element.getparent()` no existe en tipo `Element[str]` de pyright pero SÍ en runtime:
```python
# Pyright se queja, runtime funciona
grandparent = parent.getparent()  # ERROR pyright

# Fix: check attribute primero
grandparent = parent.getparent() if hasattr(parent, 'getparent') else None
```

### `_el()` no acepta texto como tercer argumento
`_el("Tag", None, "text")` pasa "text" como lista de children → TypeError.

**Fix correcto:**
```python
elem = _el("Tag", None)
elem.text = "text"  # asignar .text, no pasar en constructor
```

## Verificación post-implementación

1. `pytest tests/ -v --tb=short` → 0 failures
2. `git status --short` → solo archivos esperados
3. `wc -l *.py` → verificar líneas añadidas
4. Commit message detallado: qué módulos nuevos, qué cambios, cuántos tests

## Cuando usar subagentes vs directo

| Tamaño códigobase | Enfoque |
|---|---|
| < 500 líneas | Directo con `patch`/`write_file` |
| 500-2000 líneas | Directo, 1-2 subagentes max |
| > 2000 líneas | **Directo** (subagentes timeout en 9009) |
| Múltiples módulos interdependientes | **Directo** (evita conflictos de write) |

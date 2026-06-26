# Patrón de Actualización de Star Counts en Skills

> Sesión 2026-06-08: Descubrimiento de que los star counts en SKILL.md tienen formatos muy diversos, lo que rompe los scripts de actualización por string-match simple.

## El problema

No hay un formato único para los star counts en los SKILL.md. Variantes encontradas:

| Formato | Ejemplo | Dónde aparece |
|---------|---------|---------------|
| `33.3k⭐` | `47.5k⭐` | description YAML frontmatter |
| `33K⭐` | `33K⭐` | cuerpo del markdown |
| `33K estrellas` | `33K estrellas` | sección de fecha |
| `~24k` | `~24k` | sección de stats |
| `1,430` | `1,430` | sección de stats (sin k) |
| `207.4k⭐` | `207.4k⭐` | sección de stats |
| `33.3k+⭐` | `33.3k+⭐` | sección de stats |

## Solución: Script multi-variant

```python
updates = {
    '/path/to/skill/SKILL.md': [
        ('47.5k⭐', '47.6k⭐'),
        ('33.3k⭐', '37.1k⭐'),
    ],
}

for path, replacements in updates.items():
    with open(path) as f:
        content = f.read()
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)
```

## Fallback: Añadir al final del archivo

Si ninguna variante coincide, añadir la fecha de actualización al final:

```markdown
## Fecha de descubrimiento
2026-06-06 → 2026-06-08: 21.6k⭐ → 23.3k⭐ (+1.7k), trending diario+semanal
```

## Casos de la sesión 2026-06-08

- **ECC:** `207.4k⭐` → `210k⭐` (coincidió)
- **Goose:** `47.5k⭐` → `47.6k⭐` (coincidió)
- **Taste-skill:** `33K estrellas` → `37K estrellas` (formato diferente)
- **Supermemory:** `~24k` → `~26k` (formato con ~)
- **Agent-Reach:** Sin star count en el archivo → añadido al final
- **Headroom:** Sin star count → añadido al final
- **Hermes-WebUI:** Sin star count → añadido al final
- **INDEX.md:** `content.replace()` funciona bien para las filas de tablas

## Regla práctica

1. Primero intentar `content.replace(old, new)` para cada variante conocida
2. Si ninguna coincide, añadir sección de fecha con el nuevo conteo
3. Para INDEX.md, usar `replace()` directamente sobre el contenido completo

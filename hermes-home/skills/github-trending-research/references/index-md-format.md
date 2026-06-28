# INDEX.md — Formato del Catálogo de Skills

El catálogo de skills (`skills/INDEX.md`) usa tablas Markdown con niveles de anidación `|` para representar la jerarquía de categorías.

## Estructura

```markdown
## 🏗️ Categoría Principal

| Skill | Descripción | ⭐ |
|-------|-------------|-----|
| [nombre](ruta/SKILL.md) | Descripción breve | Badge |

## 🧪 Subcategoría

|| Skill | Descripción | ⭐ |
||-------|-------------|-----|
|| [nombre](ruta/SKILL.md) | Descripción | Badge |

## 🤖 Sub-subcategoría

||| Skill | Descripción | ⭐ |
|||-------|-------------|-----|
||| [nombre](ruta/SKILL.md) | Descripción | Badge |
```

Cada nivel extra de `|` añade un nivel de indentación en la tabla.

## Badges

- `🆕 **Nuevo**` — skill recién creado
- `🔄 **Actualizado**` — skill existente con cambios
- `🔄 **Mejorado**` — skill con mejoras significativas
- `🌙 Nocturno` — descubierto en sesiones nocturnas
- `🌐 Trending` — descubierto en trending de GitHub
- `⭐ Nk` — número de estrellas del repo

## Reglas de actualización

1. Al crear un skill nuevo → añadir fila en la categoría correspondiente
2. Al actualizar un skill → cambiar badge a `🔄 **Actualizado**` y actualizar estrellas
3. Mantener el orden alfabético dentro de cada categoría cuando sea posible
4. Las categorías principales tienen emoji descriptivo

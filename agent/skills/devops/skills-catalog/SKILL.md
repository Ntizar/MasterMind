---
name: skills-catalog
description: Catálogo de skills de Matt Pocock — patrones de skills para agentes IA, estructura y mejores prácticas.
version: "1.0.0"
tags: [skills, AI, agents, patterns, structure, best-practices]
---

# Matt Pocock's Skills

## Resumen

Catálogo de skills de Matt Pocock — patrones de skills para agentes IA. 131k⭐.

## Repo de referencia

- **GitHub:** `github.com/mattpocock/skills`
- **Lenguaje:** TypeScript
- **Licencia:** MIT

## Instalación

```bash
# Clonar para referencia
git clone https://github.com/mattpocock/skills.git
cd skills
```

## Patrones Clave

1. **Estructura de skill:** Frontmatter YAML + SKILL.md
2. **Pattern matching:** Skills se cargan por nombre desde available_skills
3. **Composición:** Skills que usan otros skills internamente
4. **Versionado:** Version en frontmatter para tracking
5. **Tags:** Categorización con tags para búsqueda

## Ejemplo de estructura

```yaml
---
name: mi-skill
description: Descripción clara y concisa
version: "1.0.0"
tags: [tag1, tag2, tag3]
---

# Mi Skill

## Qué hace
...

## Instalación
...

## Uso Básico
...

## Pitfalls
...

## Referencias
...
```

## Integración con Mastermind

- Referencia para crear nuevos skills en el sistema
- Complementa `stars-explorer` — generación automática de skills
- Ideal para `mastermind-orchestration` — patrones de delegación
- Fuente de mejores prácticas para skill authoring

## Pitfalls

- **Nombre único:** Los nombres de skills deben ser únicos en todo el sistema
- **Frontmatter:** Obligatorio para que el system los detecte
- **Sobrecarga:** Demasiados skills pueden ralentizar la carga

## Referencias

- [GitHub: mattpocock/skills](https://github.com/mattpocock/skills)

---
name: dynamic-clusters-pattern
description: Patrón de clusters dinámicos y red de conocimiento. Clusters se crean orgánicamente, con mapa central, conexiones cruzadas y frontmatter por learning.
version: 1.0.0
author: Ntizar Brain
license: MIT
platforms: [linux, macos, windows, wsl]
tags: [clusters, conocimiento, red, organización, wikilinks, taxonomía-dinámica]
---

# Patrón de Clusters Dinámicos y Red de Conocimiento

## Qué es

Patrón de organización del conocimiento basado en **clusters dinámicos** que se crean orgánicamente a medida que surgen temas, en lugar de seguir una taxonomía predefinida y cerrada. Cada learning tiene clusters en su frontmatter, los proyectos tienen un hub central, y existe un mapa global en `_clusters.md`.

### Principio fundamental: organicidad

Los clusters **no** se definen de antemano. Emergen de los learnings:

```
❌ Enfoque cerrado (no usar):
  "Definir 10 clusters fijos al inicio del proyecto"

✅ Enfoque dinámico (usar):
  "Crear cluster cuando un tema aparece por tercera vez en learnings"
```

### Estructura de clusters

```
_project/
├── _clusters.md              # Mapa global de todos los clusters
├── learnings/
│   ├── _index.md             # Índice con clusters en cada entrada
│   ├── auth-patterns.md      # learning con clusters en frontmatter
│   ├── deploy-shared.md      # learning con clusters en frontmatter
│   └── ...
├── projects/
│   ├── mi-proyecto/
│   │   └── _hub.md           # Hub central del proyecto
│   └── otro-proyecto/
│       └── _hub.md
└── ...
```

### Frontmatter de clusters en cada learning

```markdown
---
nombre: "Patrón de autenticación con JWT"
fecha_creación: 2026-06-03
clusters: [seguridad, auth, backend, jwt]
---

# Patrón de Autenticación con JWT
```

### Hub central de proyectos

Cada proyecto tiene un `_hub.md` que conecta sus learnings:

```markdown
---
proyecto: "Migración frontend"
estado: activo
clusters: [frontend, react, migración]
---

# Hub: Migración Frontend

## Learnings relacionados
- [[../learnings/auth-patterns|Patrón de autenticación]]
- [[../learnings/routing-patterns|Patrón de enrutamiento]]
- [[../learnings/css-grid-fix|Fix de CSS Grid]]

## Clusters del proyecto
[[#frontend]] · [[#react]] · [[#migración]]

## Conexiones cruzadas
- Conecta con [[otro-proyecto/_hub|Otro proyecto]] via cluster [[#frontend]]
```

## Cuándo usar

- Al crear un nuevo learning: añadir los clusters relevantes en el frontmatter
- Al explorar el conocimiento: usar `_clusters.md` para navegar por temas
- Al iniciar un nuevo proyecto: crear el `_hub.md` con los clusters iniciales
- Cuando un tema aparece por tercera vez: crear un nuevo cluster
- Al buscar conexiones entre learnings: usar el mapa de clusters

## Pasos

### Paso 1 — Crear un learning con clusters

Al crear un nuevo learning, añadir clusters en el frontmatter:

```markdown
---
nombre: "Optimización de consultas SQL"
fecha_creación: 2026-06-03
clusters: [base-de-datos, rendimiento, sql]
---

# Optimización de Consultas SQL
```

### Paso 2 — Verificar si el cluster existe

Consultar `_clusters.md` para ver si el cluster ya existe:

```markdown
<!-- _clusters.md -->
# Mapa de Clusters

## base-de-datos
- [[learnings/auth-patterns|Patrón de autenticación]]
- [[learnings/sql-optimization|Optimización de consultas SQL]]

## frontend
- [[learnings/css-grid-fix|Fix de CSS Grid]]

## rendimiento
- [[learnings/sql-optimization|Optimización de consultas SQL]]
```

Si el cluster no existe, se crea (ver Paso 3).

### Paso 3 — Crear un cluster nuevo

Cuando un tema aparece por tercera vez en learnings:

1. **Nombrar en kebab-case:** `base-de-datos`, `patron-de-autenticacion`, `frontend-react`
2. **Añadir sección en `_clusters.md`:**

```markdown
## base-de-datos
- [[learnings/auth-patterns|Patrón de autenticación]]
- [[learnings/sql-optimization|Optimización de consultas SQL]]
- [[learnings/migration-strategy|Estrategia de migración]]
```

3. **Añadir al frontmatter de todos los learnings relevantes:**

```markdown
---
clusters: [base-de-datos, sql, rendimiento]
---
```

### Paso 4 — Crear el hub de un proyecto

Al iniciar un proyecto, crear `_hub.md` en la carpeta del proyecto:

```markdown
---
proyecto: "Migración frontend"
estado: activo
clusters: [frontend, react, migración]
---

# Hub: Migración Frontend

## Learnings relacionados
- [[../learnings/auth-patterns|Patrón de autenticación]]
- [[../learnings/css-grid-fix|Fix de CSS Grid]]

## Clusters del proyecto
[[#frontend]] · [[#react]] · [[#migración]]
```

### Paso 5 — Conectar clusters entre proyectos

Si dos proyectos comparten clusters, crear conexiones cruzadas:

```markdown
<!-- En _hub.md del proyecto A -->
## Conexiones cruzadas
- Conecta con [[proyecto-b/_hub|Proyecto B]] via cluster [[#frontend]]
```

## Pitfalls

- **Lista cerrada de clusters:** No definir los clusters al inicio del proyecto. Deben emerger orgánicamente. Si un tema aparece 3+ veces, crear el cluster.
- **Clusters demasiado amplios:** Un cluster como "tecnología" o "general" no es útil. Los clusters deben ser temáticos y específicos: "frontend-react", "base-de-datos-postgres".
- **Clusters demasiado estrechos:** Un cluster como "fix-css-grid-en-componente-header" es demasiado específico. Generalizar a "css-grid" o "layout-css".
- **Frontmatter sin clusters:** Todo learning debe tener clusters en el frontmatter. Sin clusters, el learning no es navegable desde el mapa.
- **Hub sin conexiones:** Un `_hub.md` sin conexiones a otros hubs ni a learnings es un dead end. Siempre conectar.
- **Nombres inconsistentes:** Usar siempre kebab-case. `base-de-datos` no `BaseDeDatos`, no `base_de_datos`, no `basededatos`.

## Verificación

1. ✅ Cada learning tiene `clusters` en el frontmatter (lista de kebab-case)
2. ✅ `_clusters.md` tiene una sección por cada cluster activo
3. ✅ Cada sección en `_clusters.md` referencia los learnings con ese cluster
4. ✅ Los proyectos tienen `_hub.md` con conexiones a learnings y otros hubs
5. ✅ Los nombres de clusters usan kebab-case consistentemente
6. ✅ No hay clusters con menos de 2 learnings (si uno solo tiene el cluster, fusionar con otro)
7. ✅ Las conexiones cruzadas entre proyectos se mantienen actualizadas

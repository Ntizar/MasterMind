---
name: knowledge-graph-analysis
version: "1.0.0"
description: "Construir un grafo de conocimiento a partir de un repositorio de documentos (skills, notas, docs). Detecta conexiones por keywords compartidas, identifica nodos huérfanos y clusters de conocimiento."
tags: [knowledge-graph, knowledge-base, analysis, skills, clustering, orphans]
---

# Knowledge Graph Analysis

## Resumen

Procedimiento para construir un grafo de conocimiento que mapea conexiones entre documentos (skills, notas, docs) de un repositorio. Detecta conexiones por keywords compartidas, identifica nodos huérfanos (sin conexiones) y clusters de conocimiento (grupos densamente conectados).

## Cuándo usar

- Usuario pide "grafo de conocimiento", "mapa de conexiones", "qué está conectado con qué"
- Análisis de la estructura del conocimiento en un repositorio de skills/notas
- Auditoría de cobertura del conocimiento — detectar áreas sin conexiones
- Identificar skills huérfanos que podrían necesitar cross-references
- Descubrir clusters naturales de conocimiento para navegación contextual

## Flujo (4 pasos)

### Paso 1: Extraer frontmatter keywords

Solo usar frontmatter (tags + título + category), NO el body completo.

```python
import re
from pathlib import Path

def extract_frontmatter_keywords(filepath):
    content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    
    # Extraer frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    fm_text = fm_match.group(1) if fm_match else ""
    
    # Extraer tags
    tags = set()
    tags_match = re.search(r'tags:\s*\[(.+?)\]', fm_text)
    if tags_match:
        for tag in tags_match.group(1).split(','):
            tag = tag.strip().strip('"').strip("'")
            if tag:
                tags.add(tag.lower())
    
    # Extraer título y palabras clave
    title_match = re.search(r'title:\s*(.+)', fm_text)
    title = title_match.group(1).strip() if title_match else ""
    title_words = set()
    for word in re.findall(r'\b[a-záéíóúüñ]{4,}\b', title.lower()):
        if word not in stopwords:
            title_words.add(word)
    
    return tags | title_words
```

**Por qué solo frontmatter:** El body de los documentos es extenso y comparte palabras genéricas ("sistema", "completo", "funciona") que generan ruido masivo. El frontmatter contiene la señal semántica real (tags específicos, título descriptivo).

**Stopwords clave a filtrar:** palabras en español genéricas que aparecen en TODO y no discriminan ("sistema", "completo", "funciona", "permite", "necesario", etc.). Ver `references/stopwords-knowledge-graph.md` para la lista completa.

### Paso 2: Construir grafo de conexiones

```python
from collections import defaultdict

nodes = {}  # name -> {type, path, keywords, refs}
edges = defaultdict(list)

# Para cada par de nodos
for name_a, node_a in nodes.items():
    for name_b, node_b in nodes.items():
        if name_a >= name_b:
            continue
        
        shared = node_a["keywords"] & node_b["keywords"]
        if len(shared) >= 3:  # Umbral: 3+ keywords compartidas
            edges[name_a].append({
                "target": name_b,
                "type": "keyword_overlap",
                "strength": len(shared),
                "shared": list(shared)[:5]
            })
    
    # Referencias directas (menciones explícitas)
    for ref in node_a.get("refs", []):
        if ref in nodes and ref != name_a:
            edges[name_a].append({
                "target": ref,
                "type": "direct_reference",
                "strength": 10
            })
```

**Umbral recomendado:** 3+ keywords compartidas para frontmatter-only. Si se usa body completo, el umbral debe ser >= 10 (pero no se recomienda usar body).

### Paso 3: Detectar anomalías

```python
# Skills huérfanas (sin conexiones entrantes ni salientes)
connected_nodes = set()
for src, targets in edges.items():
    connected_nodes.add(src)
    for t in targets:
        connected_nodes.add(t["target"])

orphans = [name for name, data in nodes.items() 
           if data["type"] == "skill" and name not in connected_nodes]

# Clusters (nodos con 3+ conexiones)
clusters = defaultdict(list)
for name, edge_list in edges.items():
    if len(edge_list) >= 3:
        clusters[name] = [e["target"] for e in edge_list[:5]]
```

### Paso 4: Generar output

- **JSON** (`knowledge-graph.json`): datos estructurados para consumo programático
- **Markdown** (`knowledge-graph.md`): reporte legible con estadísticas, top conectados, huérfanos, clusters

## Script de referencia

`scripts/knowledge-graph.py` — script completo listo para ejecutar. Copiar a cualquier proyecto para usarlo.

## Pitfalls

- **NO usar body completo** — genera miles de conexiones falsas por palabras genéricas compartidas. Solo frontmatter (tags + título).
- **Umbral bajo = ruido** — con frontmatter-only, umbral >= 3 funciona bien. Umbral >= 5 es más selectivo. Umbral >= 10 solo deja conexiones muy fuertes.
- **Stopwords incompletas = ruido** — la lista de stopwords debe incluir términos genéricos en español e inglés que aparecen en TODO ("sistema", "completo", "sistema", "frontend", "backend", etc.). Cuantas más stopwords, más señal limpia.
- **Nombres de directorio vs frontmatter** — los skills pueden tener nombre de directorio diferente al frontmatter. Usar el nombre del directorio como key del grafo.
- **Referencias directas > keywords** — cuando un skill menciona explícitamente otro (`skill_view(name='xxx')`), esa conexión tiene strength=10 y es más significativa que cualquier keyword overlap.
- **Skills STEM/físicos son huérfanos por diseño** — dominios cerrados con tags muy específicos no compartirán keywords. Esto es CORRECTO, no un bug.
- **Clusters pueden ser engañosos** — un cluster de 3+ conexiones puede ser un grupo de skills genéricos (frontend, deploy, test) que comparten palabras comunes. Interpretar con criterio.
- **Reindexación periódica** — el grafo debe regenerarse cuando se añaden/eliminan skills o notas. No es un dato estático.

## Referencias

- **`references/stopwords-knowledge-graph.md`** — Lista completa de stopwords para filtrado de keywords (español + inglés + términos técnicos genéricos).
- **`scripts/knowledge-graph.py`** — Script completo listo para ejecutar en cualquier repositorio.

# Calidad del Embedding — Mejora del documento indexado

## Problema

El script `indexar-skills.py` solo indexa el frontmatter del SKILL.md (nombre + descripción + tags) como `document` en ChromaDB. El cuerpo del skill (secciones como Resumen, Uso, Pitfalls) no se incluye en el embedding.

**Consecuencia:** Los scores de similitud son bajos (0.25-0.50) incluso para skills muy relevantes, porque el embedding solo tiene 3-4 frases de contexto.

## Solución

Modificar `indexar-skills.py` para que el `document` incluya:

1. Frontmatter (como ahora): nombre + descripción + tags
2. Primeras secciones del cuerpo: Resumen + primeras 500 palabras de las secciones principales

### Código de ejemplo

```python
def extract_document(skill_path):
    """Extrae el texto para embedding de un SKILL.md"""
    with open(skill_path) as f:
        content = f.read()
    
    # Parsear frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content[:1000]  # fallback
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Extraer campos del frontmatter
    name = extract_field(frontmatter, 'name')
    desc = extract_field(frontmatter, 'description')
    tags = extract_field(frontmatter, 'tags')
    
    # Extraer primeras secciones del cuerpo
    # Cogemos hasta 1500 chars del cuerpo (primeras secciones)
    body_preview = body[:1500].strip()
    
    # Combinar
    document = f"{name}. {desc}. Tags: {tags}. {body_preview}"
    return document[:2000]  # max 2000 chars
```

### Impacto esperado

- **Antes:** document de ~200 chars (solo frontmatter)
- **Después:** document de ~1500-2000 chars (frontmatter + cuerpo)
- **Mejora esperada en scores:** +0.15 a +0.25 (ej: 0.46 → 0.61)

### Riesgos

- Más tokens por embedding = más coste en NaN API (cada embedding cuesta por token)
- Con 192 skills × ~1500 chars = ~288K chars por re-indexación completa
- A 60 req/min, sigue siendo viable (1.5s de delay entre requests = ~5 min total)
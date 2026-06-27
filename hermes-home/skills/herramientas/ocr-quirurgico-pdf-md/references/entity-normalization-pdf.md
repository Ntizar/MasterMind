# Entity Normalization — Patrones para Extracción de PDFs

## Problema

La extracción regex de PDFs captura texto después del patrón匹配. Ejemplos reales:

| Regex match | Texto real en PDF | Resultado sin limpiar |
|-------------|-------------------|----------------------|
| `renfe\s+mercanc` | "Renfe Mercancías que había realizado..." | "Renfe Mercancías que había" |
| `empresa\s+ferroviaria\s+(\w+)` | "empresa ferroviaria Renfe Operadora debían cruzarse" | "Renfe Operadora debían cruzarse" |
| `estación\s+de\s+(\w+)` | "estación de Getafe Industrial observa que una persona..." | "Getafe Industrial observa que una persona..." |

## Solución: 3 Capas

### Capa 1: Stop phrases en extract_estacion()

Filtrar palabras que indican que el texto continuó más allá del nombre real:

```python
STOP_PHRASES = [
    'observa', 'donde', 'procedente de', 'con destino',
    'que cubría', 'que realizaba', 'se encontraba',
    'una persona', 'un grupo de', 'personal de',
]
```

Además, limitar a 35 caracteres y cortar en la última palabra completa.

### Capa 2: Trash suffixes en extract_entidades()

Lista de sufijos que el regex captura accidentalmente:

```python
TRASH_SUFFIXES = [
    'que había', 'que cubría', 'que procedía', 'que realizaba',
    'debían cruzarse', 'hacía su', 'se encuentra', 'dispone de',
    'procedente de', 'procedió en', 'realizaba el', 'cubría el',
    'operaba el', 'prestaba el', 'ejecutaba el',
]
```

### Capa 3: Case-insensitive merging

Fusionar variantes de capitalización que representan la misma entidad:

```python
FINAL_MAP = {
    'renfe': 'RENFE',
    'renfe viajeros': 'Renfe Viajeros',
    'renfe mercancías': 'Renfe Mercancías',
    'renfe operadora': 'Renfe Operadora',
}
```

## Patrón General

```python
def normalize_entity(raw_name: str) -> str:
    # 1. Limpiar whitespace y newlines
    c = re.sub(r'\s+', ' ', raw_name).strip()
    c = c.split('\n')[0].strip()
    
    # 2. Quitar trash suffixes
    for suffix in TRASH_SUFFIXES:
        if c.lower().endswith(suffix):
            c = c[:-len(suffix)].strip()
    
    # 3. Limitar longitud
    if len(c) > 30:
        c = c[:30].rsplit(' ', 1)[0]
    
    # 4. Merge case-insensitive
    cl = c.lower()
    if cl in FINAL_MAP:
        return FINAL_MAP[cl]
    return c
```

## Entidades Finales (CIAF-visor)

203/270 informes con coordenadas. 19 entidades normalizadas:
- RENFE, ADIF, ADIF AV, Renfe Viajeros, Renfe Mercancías, Renfe Operadora
- FEVE, TRAM, CAPTRAIN, Continental Rail, Logitren, Low Cost Rail
- Acciona Rail Services, Activa Rail, COMSA Rail Transport
- Tracción Rail, Transfesa Rail, Transitia Rail

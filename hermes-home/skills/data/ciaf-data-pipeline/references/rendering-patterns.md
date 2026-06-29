# Patrones de rendering en CIAF-visor frontend

## Datos en bruto → UI

### Memorias anuales: barras de causas

Las `top_cause` son strings como `"Colisión"` o `"Atropello a pasajero"`. Para barras:
1. Contar frecuencia de cada causa
2. Calcular porcentaje
3. Renderizar barra horizontal con porcentaje

```javascript
memorias.forEach(m => {
    (m.top_causes || []).forEach(cause => {
        causes[cause] = (causes[cause] || 0) + 1;
    });
});
// Renderizar: div con width = porcentaje + label
```

### Empresas: barras de evolución anual

```javascript
const empresaYears = {};
empresas.forEach(e => {
    empresaYears[e.year] = (empresaYears[e.year] || 0) + 1;
});
// Renderizar como barras verticales o cards
```

### Entidades con color

Cada tipo de entidad tiene color:
```javascript
const entityColors = {
    'renfe': '#CB1823', 'adif': '#1A4488', 'maquinista': '#6B96CF',
    'viajero': '#16a34a', 'operador': '#f97316', 'concesionario': '#8b5cf6'
};
function getEntityBadge(entity) {
    const color = entityColors[entity.toLowerCase()] || '#6b7280';
    return `<span class="badge" style="background:${color}">${entity}</span>`;
}
```

### KPIs de memorias

Los KPIs principales:
- `total_accidents` — incidentes + accidentes
- `total_fatal` — sucesos con víctimas mortales
- `total_victims` — suma de víctimas mortales
- `total_heridos` — suma de heridos
- `total_material_damage_eur` — daños materiales en euros

### Normativa: links oficiales

```javascript
const normativaLinks = {
    'Ley 6/1998': 'https://www.boe.es/buscar/act.php?id=BOE-A-1998-5832',
    'Ley 38/2015': 'https://www.boe.es/buscar/act.php?id=BOE-A-2015-11243',
    'RD 929/2022': 'https://www.boe.es/buscar/act.php?id=BOE-A-2022-21508',
    // ... más documentos
};
```

## Tipos de datos en las memorias JSON

```json
{
    "year": 2024,
    "title": "Memoria anual CIAF 2024",
    "summary": "resumen largo...",
    "total_accidents": 28,
    "total_incidents": 15,
    "total_fatal": 2,
    "total_victims": 3,
    "total_heridos": 12,
    "total_material_damage_eur": 1250000,
    "top_causes": ["Colisión", "Atropello a pasajero"],
    "top_entities": ["Renfe", "ADIF"],
    "highlights": ["año con menos accidentes desde 2010", "..."]
}
```

## Schema de recommendations en informes

Cada report puede tener `recomendaciones` como array de strings O dicts.

### Strings
```json
"recomendaciones": ["Mejorar señalización", "Instalar vallado"]
```

### Dicts (variantes de keys)
```json
// Variante 1 (181x):
{"numero": 1, "destinatario": "ADIF", "texto": "Mejorar señalización..."}

// Variante 2 (52x):
{"numero": 1, "implementador": "Renfe", "texto": "Capacitar al personal..."}

// Variante 3 (26x):
{"numero": 1, "destinatario": "ADIF", "contenido": "Instalar vallado..."}

// Variante 4 (5x):
{"número": 1, "destinatario": "ADIF", "texto": "Mejorar señalización..."}
```

**La función de rendering debe manejar todas las variantes.**

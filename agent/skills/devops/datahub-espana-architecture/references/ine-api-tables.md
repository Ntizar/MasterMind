# Tablas INE que funcionan sin autenticación

Todas usan la misma URL base: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{ID}?tip=AM&nult=1`

## Tablas verificadas (2026-06-30)

| Tabla | Nombre | Entries | Notas |
|-------|--------|---------|-------|
| 2852 | Población por provincia y sexo | 159 | Funciona perfecto |
| 9681 | Población por CCAA y sexo | 6120 | Funciona perfecto |
| 4247 | Tasa de paro por CCAA y edad | 420 | Funciona — paro por tramos de edad |
| 4328 | Empleo por sector | 66 | Funciona |
| 4338 | Ocupados a tiempo parcial | 150 | Funciona |
| 4358 | Asalariados por tipo | 198 | Funciona |

## Tablas que NO funcionan (parse error)

| Tabla | Nota |
|-------|------|
| 39960 | Turismo — parse error |
| 39958 | — parse error |
| 4346 | Parse error |
| 4352-4360 | La mayoría parse error |

## Cómo consultar una tabla

```bash
# Verificar si una tabla funciona
curl -s "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{ID}?tip=AM&nult=1" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Entries: {len(data)}')
print(f'Primera: {data[0].get(\"Nombre\", \"?\")[:60]}')
"
```

## Parsing de datos por CCAA

Los nombres de CCAA en los datos del INE son descriptivos, hay que parsearlos:
- `'Tasa de paro de la población. Ambos sexos. Andalucía. Total.'` → Andalucía
- `'Total Nacional. Ambos sexos. Total. Total. Ocupados...'` → Nacional

```javascript
// Ejemplo: extraer tasa de paro por CCAA
data.forEach(d => {
    const name = d.Nombre || '';
    if (name.includes('Ambos sexos') && name.includes('Total.') && !name.includes('Total Nacional')) {
        for (const [key, shortName] of Object.entries(ccaaNames)) {
            if (name.includes(key)) {
                const rate = d.Data?.[d.Data.length - 1]?.Valor;
                if (rate !== null) ccaaData[shortName] = rate;
                break;
            }
        }
    }
});
```

## Tablas INE exploradas que no funcionan (2026-06-30)

Tested via batch curl. Most INE tables below 4000 range work; above that many return parse errors or empty data.

### Funcionan: 2852, 4247, 4328, 4338, 4358, 9681
### No funcionan: 39960, 39958, 4346, 4751-4758, 4352-4360

---
name: skill-earth-sciences
version: "1.0.0"
category: stem/earth-science
description: Ciencias de la Tierra — Geología, meteorología, oceanografía, climatología, astrogeología.
---

# Ciencias de la Tierra

## Descripción

Skill integral de ciencias de la Tierra que cubre:
- **Geología**: minerales, rocas (ígneas, sedimentarias, metamórficas), tectónica de placas, volcanes, sismos
- **Estructura interna de la Tierra**: corteza, manto, núcleo, geotermia
- **Mineralogía y petrología**: clasificación de minerales, ciclo de las rocas, texturas
- **Meteorología**: atmósfera (capas, composición), presión, temperatura, humedad, frentes, sistemas de viento
- **Climatología**: climas de la Tierra, clasificación de Köppen, cambio climático, efecto invernadero
- **Oceanografía**: corrientes marinas, mareas, olas, composición del agua de mar, ecosistemas marinos
- **Hidrología**: ciclo del agua, aguas subterráneas, cuencas hidrográficas
- **Geología histórica**: escala de tiempo geológico, fósiles, extinciones masivas
- **Astrogeología**: formación del sistema solar, Luna, Marte, geología planetaria

## Instrucciones

Cuando el usuario pida ayuda con ciencias de la Tierra:

1. **Identificar el subdominio**: geología, meteorología, oceanografía, climatología
2. **Para geología**: seguir el ciclo de las rocas y la tectónica de placas
3. **Para meteorología**: identificar sistemas de presión y masas de aire
4. **Para climatología**: usar clasificación de Köppen y factores climáticos
5. **Para oceanografía**: diferenciar corrientes superficiales (viento) de profundas (termohalinas)

### Formato de respuesta

- Incluir **esquemas** del ciclo correspondiente (rocas, agua, carbono)
- Para clasificación climática, indicar **letra Köppen** y características
- Para tectónica, identificar **tipo de límite** (constructivo, destructivo, transformante)
- Usar **escalas de tiempo** apropiadas (geológico vs meteorológico)

## Ejemplos de uso

### Ejemplo 1: Tipos de rocas
```
Usuario: "Clasifica el granito, el mármol y la arenisca"
Agente: Granito → Ígnea intrusiva (cristales visibles, SiO₂ alto)
        Mármol → Metamórfica (caliza recristalizada, bandado)
        Arenisca → Sedimentaria clástica (granos de arena cementados)
```

### Ejemplo 2: Clima Köppen
```
Usuario: "¿Qué clima es Cfb?"
Agente: C = templado, f = sin estación seca, b = verano suave
        Ejemplos: Londres, Madrid, Nueva York
        Temperaturas: mes más frío > -3°C, < 18°C; mes más cálido < 22°C
```

### Ejemplo 3: Tectónica de placas
```
Usuario: "¿Qué ocurre en un límite convergente oceánico-continental?"
Agente: Subducción de la placa oceánica (densa) bajo la continental
        Resultado: fosa oceánica, arco volcánico continental, sismos profundos
        Ejemplo: Cordillera de los Andes (placa de Nazca → Sudamérica)
```

## Referencias

- Geología (Winter, Phillips)
- Meteorología y climatología (Wallace & Hobbs)
- Oceanografía (Trujillo & Thurman)
- Ciencias de la Tierra (Tarbuck & Lutgens)

## Ver también

- `skill-biology-cell` — Ecosistemas y ciclos biogeoquímicos
- `skill-scientific-method` — Muestreo y análisis de datos geológicos
- `skill-physics-mechanics` — Termodinámica atmosférica y oceanográfica

## Pitfalls

- **No confundir** tiempo (atmosférico, corto plazo) con clima (promedio, largo plazo)
- **Corrientes marinas**: las cálidas van del ecuador a los polos, las frías en sentido contrario
- **Escala de tiempo geológico**: eras, períodos, épocas — no mezclar jerarquías
- **Efecto invernadero ≠ cambio climático**: el primero es natural, el segundo es antropogénico acelerado
- **Rocas ígneas**: intrusivas (enfriamiento lento = cristales grandes) vs extrusivas (rápido = cristales pequeños o vidrio)

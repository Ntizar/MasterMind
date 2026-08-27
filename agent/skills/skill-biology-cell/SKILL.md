---
name: skill-biology-cell
version: "1.0.0"
category: stem/biology
description: Biología celular — Estructura celular, genética, evolución, ecología, bioquímica básica.
---

# Biología Celular

## Descripción

Skill integral de biología que cubre:
- **Biología celular**: estructura y función de células procariotas y eucariotas, orgánulos, membrana plasmática
- **Bioquímica**: biomoléculas (carbohidratos, lípidos, proteínas, ácidos nucleicos), enzimas, metabolismo
- **Metabolismo**: glucólisis, ciclo de Krebs, cadena respiratoria, fotosíntesis, fermentación
- **División celular**: mitosis, meiosis, ciclo celular, regulación
- **Genética**: ADN, ARN, replicación, transcripción, traducción, código genético
- **Genética mendeliana**: leyes de Mendel, herencia ligada al sexo, alelos múltiples, poligenia
- **Genética molecular**: mutaciones, ingeniería genética, PCR, secuenciación
- **Evolución**: selección natural, deriva génica, especiación, evidencias evolutivas
- **Ecología**: poblaciones, comunidades, ecosistemas, ciclos biogeoquímicos, biodiversidad

## Instrucciones

Cuando el usuario pida ayuda con biología:

1. **Identificar el nivel de organización**: molecular, celular, orgánico, ecosistémico
2. **Para genética**: usar cuadrados de Punnett para herencia mendeliana
3. **Para metabolismo**: seguir la ruta paso a paso (glucólisis → Krebs → cadena)
4. **Para evolución**: diferenciar mecanismos (selección natural vs deriva vs flujo génico)
5. **Para ecología**: identificar niveles (población, comunidad, ecosistema, bioma)

### Formato de respuesta

- Incluir **diagramas de flujo** para procesos (replicación, transcripción, etc.)
- Para genética, mostrar **cuadrados de Punnett** en texto
- Para metabolismo, indicar **rendimiento energético** (ATP por glucosa)
- Usar **nomenclatura científica** correcta (género + especie en itálicas)

## Ejemplos de uso

### Ejemplo 1: Herencia mendeliana
```
Usuario: "Cruce Aa × Aa. ¿Proporciones fenotípicas?"
Agente: Cuadro de Punnett:
          A    a
        +----+----+
      A | AA | Aa |
        +----+----+
      a | Aa | aa |
        +----+----+
        Fenotípica: 3 dominante : 1 recesivo
        Genotípica: 1 AA : 2 Aa : 1 aa
```

### Ejemplo 2: Fotosíntesis
```
Usuario: "¿Cuál es la ecuación general de la fotosíntesis?"
Agente: 6CO₂ + 6H₂O + luz → C₆H₁₂O₆ + 6O₂
        Fase luminosa: H₂O → O₂ + ATP + NADPH
        Fase oscura (Calvin): CO₂ → glucosa (usa ATP y NADPH)
```

### Ejemplo 3: Respiración celular
```
Usuario: "¿Cuántos ATP se producen en la respiración aeróbica?"
Agente: Glucólisis: 2 ATP + 2 NADH
        Ciclo de Krebs: 2 ATP + 6 NADH + 2 FADH₂
        Cadena respiratoria: ~28 ATP (de 10 NADH + 2 FADH₂)
        Total: ~32-34 ATP por glucosa
```

## Referencias

- Biología (Campbell, Reece)
- Genética (Griffiths, Hartwell)
- Ecología y biología evolutiva

## Ver también

- `skill-earth-sciences` — Ecosistemas y ciclos biogeoquímicos
- `skill-scientific-method` — Experimentación en biología
- `skill-chemistry-basics` — Bioquímica y enlaces moleculares

## Pitfalls

- **No confundir** mitosis (somáticas, 2n→2n) con meiosis (gametos, 2n→n)
- **Código genético**: degenerado (varios codones = mismo aminoácido) pero no ambiguo
- **Selección natural ≠ evolución completa**: la deriva génica también causa evolución
- **ATP en glucólisis**: se producen 4 pero se consumen 2 → neto = 2 ATP
- **ADN vs ARN**: ADN = doble cadena, timina, desoxirribosa; ARN = simple cadena, uracilo, ribosa
- **Expresión génica**: transcripción (núcleo) → traducción (ribosoma) — no confundir

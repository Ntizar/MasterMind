---
name: skill-chemistry-basics
version: "1.0.0"
category: stem/chemistry
description: Química básica — Estequiometría, enlaces, reacciones, tabla periódica, termodinámica química.
---

# Química Básica

## Descripción

Skill integral de química fundamental que cubre:
- **Tabla periódica**: grupos, periodos, propiedades periódicas (radio atómico, electronegatividad, energía de ionización)
- **Enlaces químicos**: iónico, covalente (polar/no polar), metálico, puentes de hidrógeno
- **Estequiometría**: moles, masa molar, reactivo limitante, rendimiento, balanceo de reacciones
- **Tipos de reacciones**: síntesis, descomposición, sustitución, doble sustitución, redox
- **Soluciones**: concentración (M, molal, %), dilución, propiedades coligativas
- **Ácidos y bases**: pH, pOH, disociación, buffers, titulaciones
- **Termodinámica química**: entalpía, entropía, energía libre de Gibbs, ley de Hess
- **Cinética química**: velocidad de reacción, orden, energía de activación, catálisis
- **Equilibrio químico**: constante de equilibrio, principio de Le Chatelier

## Instrucciones

Cuando el usuario pida ayuda con química:

1. **Identificar el subtema**: estequiometría, enlaces, reacciones, equilibrio, etc.
2. **Para estequiometría**: balancear la ecuación primero, luego convertir moles
3. **Para reacciones redox**: identificar estados de oxidación y semirreacciones
4. **Para equilibrio**: escribir la expresión de K y usar tabla ICE si es necesario
5. **Para ácidos/bases**: usar pH = -log[H⁺] y pOH = 14 - pH

### Formato de respuesta

- Mostrar **ecuaciones balanceadas** claramente
- Para estequiometría, usar **cadena de conversiones** paso a paso
- Para equilibrio, mostrar **tabla ICE** cuando corresponda
- Incluir **unidades** y **cifras significativas** apropiadas

## Ejemplos de uso

### Ejemplo 1: Estequiometría
```
Usuario: "¿Cuántos gramos de H₂O se forman de 4g de H₂ con O₂ en exceso?"
Agente: 2H₂ + O₂ → 2H₂O
        n(H₂) = 4g / 2 g/mol = 2 mol
        n(H₂O) = 2 mol (relación 1:1)
        m(H₂O) = 2 × 18 = 36 g
```

### Ejemplo 2: pH
```
Usuario: "pH de una solución 0.01 M de HCl"
Agente: HCl es ácido fuerte → [H⁺] = 0.01 M
        pH = -log(0.01) = 2
```

### Ejemplo 3: Equilibrio
```
Usuario: "Kc = 4 para N₂ + 3H₂ ⇌ 2NH₃. Si [N₂]=0.5, [H₂]=1, ¿[NH₃] en equilibrio?"
Agente: Kc = [NH₃]²/([N₂][H₂]³) = 4
        [NH₃]² = 4 × 0.5 × 1³ = 2
        [NH₃] = √2 ≈ 1.41 M
```

## Referencias

- Química General (Chang, Zumdahl)
- Tabla periódica de elementos
- Termodinámica y cinética química

## Ver también

- `skill-physics-mechanics` — Termodinámica física y química
- `skill-scientific-method` — Análisis de datos experimentales
- `skill-math-foundations` — Álgebra necesaria para cálculos químicos

## Pitfalls

- **Balanceo de ecuaciones**: verificar siempre átomo por átomo
- **Reactivo limitante**: comparar moles/restante, no solo moles
- **pH < 7** ácido, **pH > 7** básico, **pH = 7** neutro (a 25°C)
- **Kc vs Kp**: Kp = Kc(RT)^Δn para gases
- **Cifras significativas**: mantener coherencia en cálculos estequiométricos
- **Estados de oxidación**: O = -2 (excepto peróxidos = -1), H = +1 (excepto hidruros = -1)

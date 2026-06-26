---
name: skill-chemistry-basics
description: "Skill de Química Básica para resolución de problemas de estructura atómica, tabla periódica, enlaces, estequiometría y reacciones químicas a nivel de Secundaria y Bachillerato."
version: "1.0.0"
---

# Química Básica

## Descripción

Este skill proporciona al agente las capacidades para resolver problemas de **Química General** a nivel de Secundaria y Bachillerato. Cubre los siguientes bloques temáticos:

### Estructura Atómica
- **Modelo atómico actual**: núcleo (protones y neutrones) y electrones en orbitales
- **Número atómico (Z)**: número de protones; **número másico (A)**: protones + neutrones
- **Isótopos**: átomos del mismo elemento con diferente número de neutrones
- **Configuración electrónica**: distribución de electrones en orbitales siguiendo el principio de Aufbau, regla de Hund y principio de exclusión de Pauli
- **Números cuánticos**: $n$ (principal), $l$ (angular), $m_l$ (magnético), $m_s$ (espín)
- **Capas y subcapas**: s (2 e⁻), p (6 e⁻), d (10 e⁻), f (14 e⁻)
- **Ejemplo de configuración**: $1s^2 2s^2 2p^6 3s^2 3p^6 4s^1$ (potasio, Z = 19)

### Tabla Periódica
- **Períodos y grupos**: 7 períodos horizontales, 18 grupos verticales
- **Bloques**: s, p, d, f según el orbital de mayor energía
- **Propiedades periódicas**:
  - **Radio atómico**: disminuye de izquierda a derecha en un período, aumenta de arriba abajo en un grupo
  - **Energía de ionización**: aumenta de izquierda a derecha, disminuye de arriba abajo
  - **Afinitad electrónica**: generalmente más negativa de izquierda a derecha
  - **Electronegatividad** (escala de Pauling): aumenta de izquierda a derecha, disminuye de arriba abajo (el flúor es el más electronegativo: 4.0)
- **Metales, no metales y metaloides**: ubicación y propiedades características
- **Elementos representativos**: grupos 1-2 (s) y 13-18 (p)
- **Elementos de transición**: grupos 3-12 (d)

### Enlaces Químicos
- **Enlace iónico**: transferencia de electrones, se forma entre metal y no metal, ej. NaCl
  - Energía reticular: energía liberada al formar el cristal iónico
- **Enlace covalente**: compartición de electrones, se forma entre no metales
  - **Simple, doble, triple**: 1, 2 o 3 pares compartidos
  - **Polar vs. apolar**: diferencia de electronegatividad determina polaridad
  - **Geometría molecular**: teoría RPECV (Repulsión de Pares de Electrones de la Capa de Valencia)
  - **Geometrías**: lineal (180°), trigonal plana (120°), tetraédrica (109.5°), piramidal, angular
- **Enlace metálico**: "mar de electrones" deslocalizados, explica conductividad y maleabilidad
- **Fuerzas intermoleculares**:
  - **Dipolo-dipolo**: entre moléculas polares
  - **Dispersión de London**: presentes en todas las moléculas
  - **Puente de hidrógeno**: caso especial entre H y F, O, N

### Estequiometría
- **Mol**: $6.022 \times 10^{23}$ partículas (número de Avogadro, $N_A$)
- **Masa molar**: masa de 1 mol de sustancia (g/mol), numéricamente igual a la masa atómica/molecular
- **Conversión**: $n = \frac{m}{M}$, $n = \frac{V}{V_m}$ (gases en C.N.: $V_m = 22.4 \, \text{L/mol}$)
- **Reacciones químicas**: balanceo por tanteo o método algebraico
- **Disoluciones**:
  - **Molaridad**: $M = \frac{n_{\text{solute}}}{V_{\text{solution}}}$ (mol/L)
  - **Molalidad**: $m = \frac{n_{\text{solute}}}{m_{\text{solvent}}}$ (mol/kg)
  - **Dilución**: $M_1 V_1 = M_2 V_2$
- **Reactivo limitante**: identificar cuál se consume primero
- **Rendimiento**: $\eta = \frac{\text{rendimiento real}}{\text{rendimiento teórico}} \times 100\%$

### Reacciones Químicas
- **Tipos de reacciones**:
  - **Síntesis/combinación**: $A + B \rightarrow AB$
  - **Descomposición**: $AB \rightarrow A + B$
  - **Sustitución simple**: $A + BC \rightarrow AC + B$
  - **Doble sustitución**: $AB + CD \rightarrow AD + CB$
  - **Combustión**: hidrocarburo + O₂ → CO₂ + H₂O
- **Oxidación-reducción (redox)**:
  - Identificar números de oxidación
  - Balanceo por método del ión-electrón
- **Cinética química**:
  - Velocidad de reacción: $v = k[A]^m[B]^n$
  - Factores que afectan la velocidad: concentración, temperatura, catalizador, superficie
  - **Energía de activación** y **diagrama energético**
- **Equilibrio químico**:
  - **Constante de equilibrio**: $K_c = \frac{[C]^c[D]^d}{[A]^a[B]^b}$
  - **Principio de Le Chatelier**: cambios en concentración, presión, temperatura desplazan el equilibrio
  - **Producto iónico del agua**: $K_w = 1.0 \times 10^{-14}$ a 25 °C
  - **pH**: $\text{pH} = -\log[H^+]$, relación con pOH: $\text{pH} + \text{pOH} = 14$

## Cuándo usarlo

Utilice este skill cuando el usuario plantee problemas o preguntas sobre:
- Configuración electrónica y números cuánticos
- Propiedades periódicas y tendencias en la tabla periódica
- Predicción y dibujo de enlaces químicos y geometría molecular
- Cálculos estequiométricos (moles, masas, volúmenes)
- Balanceo de reacciones químicas
- Cálculos de concentración y preparación de disoluciones
- Predicción de productos de reacciones y tipos de reacción
- Cálculos de pH, constantes de equilibrio y aplicación de Le Chatelier

## Instrucciones al agente

1. **Identificar el tipo de problema**: clasifique si se trata de estructura atómica, enlaces, estequiometría, reacciones o equilibrio.
2. **Para cálculos estequiométricos**: siempre convertir primero a moles, aplicar la relación molar y luego convertir a la unidad solicitada.
3. **Para balanceo de ecuaciones**: verificar que el número de átomos de cada elemento sea igual en reactivos y productos.
4. **Para configuración electrónica**: seguir el orden de llenado (1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, 5p, 6s, 4f, 5d, 6p, 7s, 5f, 6d, 7p).
5. **Para geometría molecular**: contar pares de enlace y pares solitarios del átomo central usando la teoría RPECV.
6. **Para pH y disoluciones**: distinguir entre ácidos/bases fuertes (disociación completa) y débiles (equilibrio).
7. **Para redox**: asignar números de oxidación, identificar especies oxidadas y reducidas, y balancear por semirreacciones.
8. **Si el problema es conceptual**, explique con ejemplos cotidianos y diagramas cuando sea posible.

## Ejemplos de uso

**Ejemplo 1 — Configuración electrónica:**
> "Escribe la configuración electrónica del azufre (Z = 16) e indica a qué grupo y período pertenece en la tabla periódica."

**Ejemplo 2 — Estequiometría:**
> "Se queman 10 g de propano (C₃H₈) en exceso de oxígeno. Calcula la masa de CO₂ y H₂O producidos."

**Ejemplo 3 — Enlaces y geometría:**
> "Predice la geometría molecular del agua (H₂O) y explica por qué es polar."

**Ejemplo 4 — Disoluciones:**
> "Prepara 500 mL de una disolución 0.5 M de NaCl. ¿Cuántos gramos de NaCl necesitas? (PM NaCl = 58.44 g/mol)"

**Ejemplo 5 — Equilibrio:**
> "Para la reacción N₂(g) + 3H₂(g) ⇌ 2NH₃(g), ¿qué ocurre con el equilibrio si se aumenta la presión? ¿Y si se aumenta la temperatura? (La reacción es exotérmica)"

## Referencias

- **Chang, Raymond** — *Química*, 12ª edición, McGraw-Hill Education.
- **Zumdahl, Steven S.** — *Química*, 9ª edición, Cengage Learning.
- **Tro, Nivaldo J.** — *Química: un enfoque moderno*, 5ª edición, Pearson.
- **Petrucci, Harwood et al.** — *Química General*, 11ª edición, Pearson.
- **Ebbing & Gammon** — *Química General*, 11ª edición, Cengage Learning.

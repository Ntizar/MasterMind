---
name: td-acotacion
description: Acotación según ISO 129: principios, elementos de cota, métodos de acotación (cadena, paralela, combinada, coordenadas), cotas funcionales, cotas auxiliares y reglas de acotación.
tags: [stem, td, basics]
---

# Acotación (ISO 129)

## Referencias de autoridad

- **ISO 129-1**: Technical products documentation — Dimensioning — General principles, definitions and methods
- **UNE 1037**: Principios generales de acotación
- **ISO 129-2**: Technical product documentation — Dimensioning — Rules for indication of dimensions
- **Barron-Bravo**: Dibujo Técnico, Editorial Paraninfo

## Elementos de la acotación

### Línea de cota
- Línea continua fina, paralela a la dimensión que acota
- Termina en flechas (abiertas, cerradas, oblicuas) o en trazos
- Separación entre línea de cota y pieza: 7-10 mm mínimo
- Separación entre líneas de cota paralelas: 5-7 mm

### Línea auxiliar (de referencia)
- Línea continua fina, perpendicular a la línea de cota
- Sobresale 2-3 mm de la línea de cota
- Separación de la pieza: 1-2 mm (con línea fina discontinua) o desde el contorno visible con línea fina continua

### Valor (cifra de cota)
- Sobre la línea de cota, centrado
- Orientación: horizontal (dimensiones debajo de la línea)
- Rotación: vertical (dimensiones izquierda de la línea)
- Inclinada o en cajetín (dimensiones en cualquier dirección)
- **Regla**: no se repiten cotas, no se omiten cotas necesarias

### Símbolo de cota
- Φ (diámetro)
- R (radio)
- SR (radio esférico)
- SΦ (diámetro esférico)
- □ (cuadrado)
- C (chaflán) — puede usarse C × 45°
- t (espesor) — también T o S
- X (collares)

### Flechas
- **Flecha oblicua**: 45°, relación largo/ancho ≈ 4:1
- **Flecha abierta**: 15°-20°
- **Flecha cerrada**: 15°-20°, rellena
- **Trazo oblicuo**: para espacios pequeños

## Métodos de acotación

### En cadena
- Cotas sucesivas una tras otra (→ → →)
- La suma de tolerancias puede acumularse
- **Ventaja**: fácil lectura
- **Inconveniente**: acumulación de tolerancias

### En paralelo
- Todas las cotas desde una misma referencia (origen común)
- **Ventaja**: tolerancias independientes
- **Inconveniente**: ocupa más espacio

### Combinada (mixta)
- Mezcla de cadena y paralelo
- Usar cuando ambas ventajas son necesarias

### Por coordenadas
- Cotas X e Y desde un origen común
- Útil: piezas con taladros, CNC
- **Tabla de coordenadas**: agujero → X, Y, Φ

## Reglas de acotación

### Reglas generales
1. **No repetir cotas**: cada dimensión se acota una sola vez
2. **No omitir cotas necesarias**: la pieza debe poderse fabricar e inspeccionar
3. **Cotas en la vista más clara** (generalmente donde la dimensión se representa en verdadera magnitud)
4. **No acotar en cortes ni secciones** (salvo excepciones)
5. **Las cotas se leen desde abajo y desde la derecha**
6. **Las cotas funcionales son prioritarias**: las que afectan al funcionamiento

### Posición de la cifra
- **Horizontal**: sobre la línea de cota
- **Vertical**: a la izquierda de la línea de cota
- **Inclinada**: siguiendo la dirección de la línea de cota (en ángulo ≤ 45° desde la horizontal)
- **En cajetín**: cuando hay varias cotas cerca

### Cotas de diámetros y radios
- **Diámetros**: delante del valor (Φ30)
- **Radios**: delante del valor (R15)
- El centro de arco se marca con una cruz (+)
- Círculos pequeños (< 6 mm): la flecha se coloca por fuera

### Acotación de ángulos
- El valor se alinea con la bisectriz del ángulo
- La línea de cota es un arco concéntrico al vértice del ángulo

## Acotación funcional vs auxiliar

- **Cota funcional**: necesaria para el funcionamiento de la pieza (F)
- **Cota auxiliar**: para información complementaria (entre paréntesis)
- **Cotas de fabricación**: para el proceso (por ejemplo, para fundición, mecanizado)

## Errores comunes / Pitfalls

- **Repetir cotas**: cada cota una sola vez. Si se repite, puede haber contradicciones
- **Cotas en azul**: las cotas no se tachan ni se corrigen con tinta
- **Cotas ocultas**: no acotar en aristas ocultas (salvo que sea imprescindible)
- **Flechas**: tipo uniforme en todo el plano (0° u 80°)
- **Redondeces**: olvidar poner Φ o R. Sin símbolo, el valor es ambiguo
- **Cotas en serie**: la suma de cotas en cadena debe coincidir con la cota total (DIBCO: no acotar la suma de cotas en cadena si la suma de cotas en cadena ya acota la pieza completa)

## Verificación

- [ ] ¿Cada dimensión única aparece exactamente una vez?
- [ ] ¿Símbolo Φ o R presente en diámetros y radios?
- [ ] ¿Las cotas funcionales son correctas y prioritarias?
- [ ] ¿Las líneas de cota son paralelas a la dimensión que acotan?
- [ ] ¿Las líneas auxiliares son perpendiculares a las de cota?
- [ ] ¿Los valores de cota están orientados correctamente?
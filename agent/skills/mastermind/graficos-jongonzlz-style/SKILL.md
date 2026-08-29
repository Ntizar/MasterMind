---
name: graficos-jongonzlz-style
description: "Patrón visual de gráficos estilo @jongonzlz — gráficos de datos macroeconómicos y demográficos españoles con estilo limpio, minimalista y periodístico. Tipos: small multiples, dumbbell plots, diverging bars, stacked bars, line charts con doble eje, population pyramids, waterfall fiscal."
tags: [mastermind, graficos, visualizacion, dataviz, economics, demografia, estilos]
---

# Gráficos estilo @jongonzlz

## Cuándo usar este skill

- Cuando el usuario pida crear gráficos de datos macroeconómicos, demográficos o sociales de España/UE
- Cuando se necesite un estilo visual limpio, minimalista y periodístico
- Cuando se quieran replicar gráficos de estilo "informe técnico" o "divulgación económica"
- Temas típicos: salarios, gasto público, pensiones, demografía, precios, IRPF, pobreza

## Referencia visual

- Fuente original: @jongonzlz (Notion gallery)
- Estilo: Datawrapper / Plotly / D3.js export estático
- Paleta: blanca, azul oscuro, rojo, naranja, gris claro, verde teal
- Fondo: SIEMPRE blanco puro (#FFFFFF)

## Paleta de colores maestra

### Colores principales
- **Azul oscuro (serie primaria):** #1B3A5C o #2C3E50 — líneas principales, títulos, badges positivos
- **Rojo (alerta/negativo):** #CC2222 o #E74C3C — variaciones negativas, anotaciones, series destacadas
- **Naranja (serie secundaria):** #E67E22 o #F39C12 — segunda serie, cotizaciones SS
- **Verde teal (positivo):** #1ABC9C o #00BFA5 — valores actuales en dumbbell plots, badges positivos
- **Amarillo (terciario):** #F1C40F — tercera serie, precio vivienda
- **Gris claro (neutro):** #CCCCCC o #E0E0E0 — cuadrícula, ejes, fondo de badges
- **Gris oscuro (texto):** #333333 o #2D3436 — labels, títulos secundarios

### Colores de acento (paleta extendida)
- **Morado:** #8E44AD — categoría adicional
- **Verde bosque:** #27AE60 — educación
- **Azul cielo:** #87CEEB — desempleo
- **Naranja claro:** #FFA07A — incapacidad temporal

### Reglas de color
- Máximo 4-5 colores por gráfico para evitar saturación
- Si hay 2 series: azul + rojo o azul + naranja
- Si hay 3 series: azul + naranja + gris
- Si hay 4+ series: usar grises para fondos, colores saturados para destacados
- Badges: fondo del color de la serie, texto blanco
- Negativos: siempre rojo o rojo oscuro
- Positivos: azul o verde teal

## Tipografía

- **Fuente principal:** sans-serif limpia (Inter, Roboto, Arial, Helvetica)
- **Títulos:** bold, 18-24pt, negro #000000
- **Subtítulos:** regular/italic, 12-14pt, gris oscuro
- **Labels de ejes:** 10-12pt, gris
- **Valores en badges:** bold, 10-14pt, blanco sobre color
- **Fuente y crédito:** 8-10pt, gris claro, alineados a izquierda (fuente) y derecha (crédito)

## Tipos de gráfico y cuándo usarlos

### 1. Small Multiples Grid (Grid de mini-gráficos)
**Cuándo:** Comparar tendencias de muchas entidades (países, CCAA, regiones) con la misma escala
**Ejemplo:** "Evolución precio vivienda UE por país"

**Layout:**
- Grid de 4-5 columnas × filas necesarias
- Panel principal más grande (ej: UE completa) arriba a la izquierda
- Paneles individuales más pequeños alrededor
- Cada panel: mini line chart con misma escala Y

**Diseño por panel:**
- Línea azul oscura (#1B3A5C) con área sombreada azul claro (#E6F0FA) debajo
- País con España: área en rojo claro (#FCE8E8) para destacar
- Badge porcentaje al final: fondo azul (positivo) o rojo (negativo), texto blanco
- Positivos dentro del área sombreada, negativos fuera
- Ejes: solo marcas en extremos del período, Y de 50 a 150 (índice)
- Título del país centrado debajo del panel

### 2. Dumbbell Plot (Gráfico de mancuerna)
**Cuándo:** Comparar dos puntos en el tiempo para múltiples categorías
**Ejemplo:** "Evolución salario bruto por CCAA 3T2018-3T2025"

**Layout:**
- Eje Y: categorías (CCAA) ordenadas de mayor a menor valor actual
- Eje X: valores numéricos (euros)
- Dos puntos por fila conectados por línea

**Diseño:**
- Punto izquierdo (año antiguo): rojo (#E74C3C) o coral
- Punto derecho (año actual): teal (#1ABC9C)
- Línea conectora: gris claro (#DCDDE1)
- Valores numéricos al lado de cada punto en el color correspondiente
- Leyenda arriba: "3T2018" con punto rojo, "3T2025" con punto teal
- Sin línea de eje X explícita, solo números flotantes

### 3. Diverging Bar Chart (Barras divergentes)
**Cuándo:** Mostrar variación positiva/negativa desde un eje central cero
**Ejemplo:** "Variación del gasto público sobre PIB por funciones"

**Layout:**
- Eje Y: categorías (funciones de gasto) ordenadas por magnitud
- Eje X: centrado en 0%, extendiéndose a izquierda (negativo) y derecha (positivo)
- Barras horizontales que crecen desde el eje central

**Diseño:**
- Barras negativas: verde claro (#86C966) — disminución
- Barras positivas: rojo oscuro (#B9181E) — aumento
- Línea vertical en 0% más gruesa y oscura
- Valores numéricos al final de cada barra
- Categorías ordenadas de menor a mayor magnitud
- Etiquetas de totales arriba: "Variación total: +80,182M€"

### 4. Multi-series Line Chart (Gráfico de líneas múltiples)
**Cuándo:** Evolución temporal de 2-5 variables relacionadas
**Ejemplo:** "Evolución componentes del salario 1T2018-3T2025"

**Layout:**
- Eje X: tiempo (trimestres o años)
- Eje Y: índice o valor (1T2018 = 100 como base)
- 2-4 líneas con marcadores en cada punto de datos

**Diseño:**
- Colores: azul oscuro + naranja + rojo + amarillo (en orden de prioridad)
- Marcadores: círculos rellenos de 6px en cada punto
- Líneas de 2-3px de grosor
- Cuadrícula horizontal gris muy clara (#F0F0F0)
- Leyenda dentro del área del gráfico, no fuera
- Badges con valor final al final de cada línea
- Anotaciones con flechas para eventos importantes (línea vertical discontinua + caja de texto)

**Anotaciones especiales:**
- Línea vertical discontinua para eventos legislativos
- Caja de texto blanco con borde gris para eventos
- Flecha roja apuntando al punto de inflexión

### 5. Grouped Horizontal Bar (Barras horizontales agrupadas)
**Cuándo:** Comparar múltiples series por categoría
**Ejemplo:** "Variación del gasto público ajustado a la inflación. 2 gobiernos"

**Layout:**
- Eje Y: categorías (funciones de gasto)
- Eje X: valores numéricos (millones de euros)
- Dos barras lado a lado por categoría

**Diseño:**
- Serie 1 (gobierno anterior): azul oscuro (#003366)
- Serie 2 (gobierno actual): rojo (#FF3333)
- Valores numéricos al final de cada barra
- Totales arriba a la derecha con color de cada serie
- Eje X con línea central en 0

### 6. Stacked Bar Chart 100% (Barras apiladas al 100%)
**Cuándo:** Distribución porcentual de categorías
**Ejemplo:** "Distribución salarial por tipo de pensionista"

**Layout:**
- Eje X: categorías (tipos de pensionista)
- Eje Y: 0% a 100%
- Cada barra dividida en segmentos de color

**Diseño:**
- Escala semáforo: rojo oscuro (bajo) → naranja → amarillo → verde claro (alto)
- Etiquetas de porcentaje dentro de cada segmento (blanco si el segmento es suficientemente grande)
- Leyenda arriba con rangos de valores
- Fondo blanco, cuadrícula horizontal sutil

### 7. Vertical Bar Chart con Colores Condicionales
**Cuándo:** Comparar valores absolutos con énfasis en extremos
**Ejemplo:** "Variación población residente UE por país"

**Layout:**
- Eje X: países (etiquetas verticales para legibilidad)
- Eje Y: valores (positivos arriba, negativos abajo)
- Línea de base en 0

**Diseño:**
- Barras mayoritarias: gris (#808080)
- País destacado positivo: verde (#4CAF50)
- País destacado negativo: rojo (#F44336)
- Solo 2-3 colores diferentes para no saturar

### 8. Line Chart con Doble Eje Y
**Cuándo:** Comparar dos magnitudes con escalas diferentes
**Ejemplo:** "Comparación IRPF 2018-2025"

**Layout:**
- Eje X: variable continua (ingresos anuales)
- Eje Y izquierdo: serie 1
- Eje Y derecho: serie 2
- 3 líneas: 2 para el eje izquierdo, 1 para el derecho

**Diseño:**
- Colores contrastantes: rojo vs azul vs amarillo
- Leyenda con indicador "[der.]" para series del eje derecho
- Valores de cada eje en su lado correspondiente

### 9. Stacked Bar + Linea Neto (Balance fiscal por edad)
**Cuándo:** Descomposición de gastos/ingresos por grupo de edad
**Ejemplo:** "Estimacion gasto total proteccion social e impuestos por edad"

**Layout:**
- Eje X: grupos de edad (0 a >100)
- Eje Y: millones de euros (positivos y negativos)
- Barras apiladas positivas (gastos) y negativas (impuestos)
- Linea roja superpuesta: saldo neto

**Diseño:**
- 10+ colores para diferentes categorias de gasto
- Leyenda extensa en parte superior
- Linea roja (#8B0000) de 3px
- Nota tecnica extensa al pie con metodologia

### 10. Population Piramide Comparativa
**Cuándo:** Comparar estructura poblacional entre dos puntos en el tiempo
**Ejemplo:** "Comparativa demografica Espana 2024 vs 2050"

**Layout:**
- Eje Y central: edad (0 a 100+)
- Eje X izquierdo: poblacion punto 1
- Eje X derecho: poblacion punto 2
- Barras apiladas horizontales por origen migratorio

**Diseño:**
- 4 colores por generacion:
  - Azul (#799FD4): nacido en Espana, 2 padres espanoles
  - Amarillo claro (#FDEDA0): gen 2.5, 1 padre extranjero
  - Verde (#70AD47): gen 2, 2 padres extranjeros
  - Rosa/naranja (#ED7D31): gen 1, nacido en el extranjero
- Cuadricula fina horizontal y vertical
- Leyenda en esquina superior izquierda

## Elementos comunes a TODOS los graficos

### Header
- Titulo principal: bold, 18-24pt, negro
- Subtitulo: regular, 12-14pt, gris oscuro
- Badges de categorias: pidoras grises con texto oscuro

### Footer
- Fuente: alineada a izquierda, 8-10pt, gris
- Credito: autor, alineado a derecha, 8-10pt, gris
- Nota metodologica: si aplica, en letra muy pequena

### Cuadricula
- SIEMPRE gris muy clara (#F0F0F0 o #E0E0E0)
- Solo horizontal (excepto en small multiples que puede ser ambas)
- Nunca competir con los datos

### Marcas de agua
- Opcional: diagonal semitransparente para proteger autoria
- Opacidad: 5-10%

## Herramientas de creacion

### Opcion 1: HTML + Canvas/SVG (recomendado para Mastermind)
- Crear archivo HTML autocontenido
- Usar Canvas 2D o SVG inline
- Ideal para graficos estaticos de alta calidad
- Exportable a imagen con html2canvas

### Opcion 2: Plotly.js
- Ideal para graficos interactivos
- Soporta todos los tipos listados
- CDN: https://cdn.plot.ly/plotly-latest.min.js

### Opcion 3: D3.js
- Maxima flexibilidad
- Ideal para small multiples y graficos personalizados
- CDN: https://d3js.org/d3.v7.min.js

### Opcion 4: Chart.js
- Simple y rapido
- Ideal para line charts y bar charts basicos
- CDN: https://cdn.jsdelivr.net/npm/chart.js

## Pitfalls

1. NO usar mas de 5 colores por grafico — saturacion visual, pierde legibilidad
2. NO usar tablas markdown — incompatibles con Telegram, usar listas
3. NO olvidar la fuente y credito — SIEMPRE al pie del grafico
4. NO usar fondos grises o de color — SIEMPRE blanco puro
5. NO hacer lineas de cuadricula oscuras — competir con los datos
6. NO olvidar ajustar por inflacion — "terminos reales" es clave en datos economicos
7. NO usar 3D — el estilo es SIEMPRE plano y minimalista
8. NO poner leyenda fuera del grafico — integrarla dentro cuando sea posible
9. NO usar etiquetas de eje X horizontales — rotar verticalmente si hay muchas categorias
10. NO hacer graficos sin contexto — SIEMPRE incluir subtitulo que explique que se muestra

## Verificacion

- Titulo + subtitulo descriptivo presentes
- Colores consistentes con la paleta maestra
- Fuente de datos y credito al pie
- Cuadricula lo suficientemente sutil
- Badges/valores legibles
- Fondo blanco puro
- Grafico plano (sin 3D)
- Maximo 5 colores diferentes
- Anotaciones aportan valor (no ruido)
- Grafico cuenta una historia clara

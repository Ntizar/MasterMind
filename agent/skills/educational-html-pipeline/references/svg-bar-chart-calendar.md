# SVG Bar Chart — Patrón para Calendario/Tiempo

## Cuándo usar
- Temas de primaria sobre tiempo, calendario, meses, días
- Cuando el score `visual` está por debajo de 9
- Temas que involucran comparar cantidades discretas (días/mes, horas/día)

## Patrón visual
Gráfico de barras verticales mostrando valores por categoría (meses del año), con leyenda codificada por colores.

## Ejemplo: Días por mes (s05-9-tiempo-calendarios.html)
```svg
<svg viewBox="0 0 500 200" width="500" height="200">
  <!-- Título centrado arriba -->
  <text x="250" y="20" text-anchor="middle" font-size="13" fill="#1e293b" font-weight="bold">Días por mes en un año normal (365)</text>
  
  <!-- Barras: cada mes = rectángulo de 25px ancho, altura = días * 3 -->
  <!-- Eje base en y=160 -->
  <!-- Ene: 31 días → height=93, y=160-93=67 -->
  <rect x="15" y="67" width="25" height="93" fill="#2563eb" rx="3"/>
  <text x="27" y="175" text-anchor="middle" font-size="9" fill="#2563eb" font-weight="bold">31</text>
  <text x="27" y="195" text-anchor="middle" font-size="8" fill="#64748b">Ene</text>
  
  <!-- Feb: 28 días → height=84, y=160-84=76 -->
  <rect x="45" y="76" width="25" height="84" fill="#f97316" rx="3"/>
  <text x="57" y="175" text-anchor="middle" font-size="9" fill="#f97336" font-weight="bold">28</text>
  <text x="57" y="195" text-anchor="middle" font-size="8" fill="#64748b">Feb</text>
  
  <!-- ... repetir para cada mes ... -->
  
  <!-- Leyenda a la derecha -->
  <rect x="390" y="30" width="95" height="70" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
  <rect x="398" y="40" width="12" height="12" fill="#2563eb" rx="2"/>
  <text x="415" y="50" font-size="9" fill="#334155">31 días (7 meses)</text>
  <rect x="398" y="58" width="12" height="12" fill="#10b981" rx="2"/>
  <text x="415" y="68" font-size="9" fill="#334155">30 días (4 meses)</text>
  <rect x="398" y="76" width="12" height="12" fill="#f97316" rx="2"/>
  <text x="415" y="86" font-size="9" fill="#334155">28 días (1 mes)</text>
</svg>
```

## Colores recomendados
- 31 días: `#2563eb` (azul) — mayor frecuencia
- 30 días: `#10b981` (verde) — frecuencia media
- 28 días: `#f97316` (naranja) — valor atípico
- Texto etiquetas: `#64748b` (gris)
- Texto valores: color del rectángulo + `font-weight="bold"`

## Reglas
- Altura base del SVG: 200px, eje en y=160
- Factor de escala: `días * 3` para altura del rectángulo
- Espaciado entre barras: 5px (25px ancho + 5px gap = 30px entre x)
- Leyenda siempre a la derecha, dentro de un rectángulo con borde suave
- Truco pedagógico debajo del SVG con `text-small-hex-mt-1`

## Variantes
- Para horas/día: usar mismo patrón con valores 0-24
- Para eventos por mes: mismo patrón, colores según categoría
- Para comparar dos años (normal vs bisiesto): barras dobles lado a lado

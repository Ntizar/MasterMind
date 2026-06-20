# SVG Area Model — Patrón para multiplicación de decimales

## Cuándo usar
- Temas de primaria con multiplicación de decimales
- Cuando el score `visual` está por debajo de 5
- Temas de 5º-6º Primaria donde se introduce la multiplicación decimal

## Patrón visual
Dividir la multiplicación decimal en 4 rectángulos de un modelo de área. Cada rectángulo se colorea diferente.

## Ejemplo: 2.5 × 1.2
```
        2    |  0.5
   ─────────────────
1   │ 2.00   │  0.50
    │────────┼───────
0.2 │ 0.40   │  0.10
```
Total: 2.00 + 0.50 + 0.40 + 0.10 = 3.00

## Colores recomendados
- Rectángulo principal (entero × entero): `#2563eb` (azul)
- Rectángulo 1 (decimal × entero): `#10b981` (verde)
- Rectángulo 2 (entero × decimal): `#f97316` (naranja)
- Rectángulo 3 (decimal × decimal): `#a855f7` (morado)

## Verificación
- Cada rectángulo debe tener texto con el resultado parcial
- Líneas divisorias blancas entre rectángulos
- Etiqueta de ejes X e Y con los factores
- Suma total visible a la derecha o abajo

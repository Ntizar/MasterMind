---
name: dieta
description: "Seguimiento de dieta y nutrición — cálculo de macros, registro de comidas en el repo /root/workspace/dieta/, estimación de kcal y macronutrientes a partir de descripciones o fotos de packaging."
version: "1.0.0"
tags: [dieta, nutricion, macros, salud, tracking]
---

# Dieta — Seguimiento Nutricional

## Trigger

Cuando el usuario escribe **"dieta"** al inicio de una orden, se refiere a llevar el cálculo de comidas en el repo `/root/workspace/dieta/SEGUIMIENTO.md`.

## Flujo de trabajo

1. **Leer SEGUIMIENTO.md** — `read_file(path="/root/workspace/dieta/SEGUIMIENTO.md")`
2. **Analizar la comida** — estimar kcal, proteínas, grasas, hidratos, sal a partir de:
   - Descripción textual del usuario
   - Foto de packaging (usar `vision_analyze` para leer tabla nutricional)
   - Base de datos de alimentos comunes (patata, boniato, cerdo, etc.)
3. **Actualizar la tabla** — añadir fila con fecha, hora, platos, kcal estimadas y notas macro
4. **Commit** — `cd /root/workspace/dieta && git add SEGUIMIENTO.md && git commit -m "🍽️ Registro comida <fecha>: <descripcion>"`

## Estimación de alimentos comunes

### Vegetales asados/roasted
- Patata asada: ~90 kcal/100g, 0,3g grasa, 20g hidratos, 2g proteína
- Boniato asado: ~90 kcal/100g, 0,2g grasa, 20g hidratos, 1,5g proteína
- Cebolla asada: ~40 kcal/100g, 0,1g grasa, 9g hidratos, 1g proteína
- **Mezcla de vegetales asados (salteado rústico):** ~75-80 kcal/100g, ~0,1g grasa, ~15g hidratos, ~2g proteína

### Carnes
- Filete de cerdo (lomo magro): ~180 kcal/100g crudo, 10g grasa, 0g hidratos, 25g proteína
- Filete de cerdo (paletilla): ~220 kcal/100g crudo, 14g grasa, 0g hidratos, 22g proteína
- "Filete pequeño" ≈ 50-60g por pieza → 2 filetes ≈ 100-120g

### Cálculo rápido mental
- **Proteína** → 1g = 4 kcal
- **Grasa** → 1g = 9 kcal
- **Hidratos** → 1g = 4 kcal
- **Fibra** → 1g = 2 kcal (aproximado)

## Formato de registro

La tabla de comidas en SEGUIMIENTO.md usa columnas:
`Fecha | Hora | Desayuno | Almuerzo | Comida | Merienda | Cena | Calorías est. | Notas`

Si no encaja en las columnas de comidas, usar la columna "Comida" y poner todo en la descripción.

## Referencias

- `references/alimentos-base.md` — Base de datos de alimentos con valores nutricionales por 100g (patatas, carnes, vegetales, platos compuestos). Actualizar con nuevos alimentos que aparezcan.

## Notas

- TODO en castellano. NUNCA inglés.
- Atribución: si se genera un informe/artefacto → "Hecho con (L) por David Antizar"
- El repo está en `/root/workspace/dieta/` con branch `main`

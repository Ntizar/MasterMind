# Eliminar antes de añadir — Principio de mejora de calidad

## Regla de oro (2026-06-10)

**Antes de añadir NUEVO contenido, eliminar REPETITIVO.**

Cuando un tema tiene muchos ejercicios del mismo tipo, el problema NO es "falta contenido" — es "hay demasiado contenido repetitivo".

## Procedimiento

1. **Leer el HTML y contar tipos de ejercicio** (no solo cantidad)
2. **Identificar tipos repetidos** — si un tipo aparece >3 veces, es sospechoso
3. **Eliminar los peores repetitivos** — los que no aportan nada nuevo
4. **Añadir SOLO tipos que falten** — completar la variedad
5. **Verificar** que después de la mejora, ningún tipo supera el 30% del total

## Ejemplo real: s01-10-patrones.html (2026-06-10)

**Antes:** 17 ejercicios, 7 de los cuales eran "completar con quiz botones" (41% del total)
- Ejercicio 1: 🔴🔵🔴🔵🔴___ → quiz botones
- Ejercicio 2: 1,2,3,4,___ → quiz botones (BUG: dos opciones "5")
- Ejercicio 3: ⭐⭐🌙⭐⭐🌙⭐⭐___ → quiz botones
- Ejercicio 4: 5,10,15,20,___ → quiz botones
- Ejercicio 5: 🍎🍎🍌🍎🍎🍌🍎🍎___ → quiz botones

**Acción:** Eliminar ejercicios 1-4, mantener solo el 5 (el mejor contextualizado con frutas)

**Añadir:**
- Canvas interactivo creador de patrones (visualización nueva)
- Problema de cumpleaños (caso real nuevo)
- Conexión música (vals ABB)

**Resultado:** 12 ejercicios, 7 tipos diferentes, 0 tipos repetitivos.

## Señales de que debes ELIMINAR, no añadir

| Señal | Acción |
|-------|--------|
| >50% de ejercicios son del mismo tipo | Eliminar repetitivos |
| Ejercicios con bugs (opciones duplicadas, refs rotas) | Arreglar o eliminar |
| "Completa: X, Y, Z" con solo cambiar números | Eliminar |
| Score exercises > 15 pero dificultad_range < 6 | Demasiados fáciles/repetitivos |

## Regla de distribución post-mejora

Después de cualquier mejora, la distribución de tipos debe cumplir:

- **Ningún tipo > 30%** del total de ejercicios
- **Al menos 4 tipos diferentes** presentes
- **Cada tipo aporta algo distinto** al aprendizaje

## Score objetivo

| Dimensión | Antes | Después |
|-----------|-------|---------|
| exercises | 17 (inflado, repetitivo) | 12 (variado) |
| visual | 5 | 7 (canvas nuevo) |
| real_world | 9 | 10 (caso cumpleaños) |
| connections | 3 | 4 (música) |

## Referencias

- Caso práctico: `s01-10-patrones.html` mejora 2026-06-10
- Principio relacionado: `calidad-sobre-cantidad.md`

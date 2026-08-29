# Presupuesto de Construcción — Dashboard HTML

## Cuándo usar
- El usuario sube un PDF de presupuesto de obra/construcción
- Necesita visualizar capítulos, partidas, mediciones de forma interactiva
- El PDF tiene estructura de RESUMEN + capítulos + mediciones

## Estructura típica de un presupuesto español (PCPI)

1. **Datos generales** — cliente, ubicación, fecha, importe total
2. **RESUMEN** — tabla con capítulos (0-30+) y sus importes
3. **Capítulos detallados** — cada uno con:
   - Número y título (01.01 Albañilería, etc.)
   - Partidas con: Nº, Descripción, Unidad, PM, Cant, Parcial
4. **Datos financieros** — gastos generales, beneficio industrial, IVA

## Patrones de parsing

### Extraer el RESUMEN
Buscar patrón:
```
CAPÍTULO  |  DESCRIPCIÓN  |  IMPORTE
01.01     |  Albañilería  |  193.456,78 €
```

O en texto plano:
```
RESUMEN
Capítulo 01.01 - Albañilería: 193.456,78 €
Capítulo 01.02 - Estructuras: 174.123,45 €
```

### Extraer datos financieros
Buscar:
- Total ejecución material
- Gastos generales (%)
- Beneficio industrial (%)
- IVA (10% o 21%)
- Total general

## Dashboard HTML — Estructura recomendada

### 1. Header
- Título del proyecto
- Cliente, ubicación, fecha
- Importe total destacado

### 2. KPIs principales (6 cards)
- Total presupuesto
- Ejecución material
- Gastos generales
- Beneficio industrial
- IVA
- Total con impuestos

### 3. Visualizaciones
- **Donut chart** — distribución por capítulos (top 10 + "otros")
- **Horizontal bar chart** — top 10 capítulos por importe
- **Pie chart** — desglose financiero (material, GG, BI, IVA)

### 4. Tabla detallada
- Todos los capítulos con: número, descripción, importe, % del total
- Ordenable por cualquier columna
- Filtrable por texto
- Expandible para ver partidas

### 5. Desglose de mediciones
- Unidades más frecuentes
- Partidas con mayor PM

## Librerías recomendadas
- **Chart.js** — para gráficos (CDN o embebido)
- **Aurora Design System** — para estilo (CDN)
- **Sin dependencias de backend** — todo en un HTML

## Ejemplo de datos parseados

```javascript
const budgetData = {
  project: "Edificio residencial",
  client: "TREVICON OBRAS Y SERVICIOS, S.L.",
  location: "Alcobendas, MADRID",
  date: "16/06/2026",
  total: 1207801.33,
  executionMaterial: 1098001.21,
  generalExpenses: 0.08,
  industrialBenefit: 0.05,
  vat: 0.10,
  chapters: [
    { id: "01.01", name: "Albañilería", amount: 193456.78, pct: 16.02 },
    { id: "01.02", name: "Estructuras", amount: 174123.45, pct: 14.42 },
    // ... más capítulos
  ]
};
```

## Pitfalls
- **PDFs de presupuesto son grandes** (300+ páginas) — extraer solo RESUMEN + capítulos principales
- **Formatos variables** — no todos los presupuestos siguen el mismo patrón de RESUMEN
- **Moneda** — siempre verificar si es EUR u otra moneda
- **IVA** — en España puede ser 10% (reducido) o 21% (general)

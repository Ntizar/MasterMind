# Patrón: Fichas Arquitectónicas desde PDF

## Caso de uso
Generar fichas individuales de apartamentos/viviendas a partir de planos PDF arquitectónicos.

## Flujo de trabajo

### 1. Análisis del PDF
```python
import fitz

doc = fitz.open("planos.pdf")
for page in doc:
    text = page.get_text()
    # Detectar patrones: "Apartamento X", "Habitación", "Baño", áreas en m²
```

### 2. Extracción de datos
- Identificar unidades (apartamentos, viviendas)
- Extraer áreas por estancia (habitaciones, baños, cocinas, salones)
- Detectar tipo de vivienda (estudio, 1 hab, 2 hab, etc.)
- Calcular superficie total

### 3. Generación de fichas HTML
Estructura recomendada:
```
┌─────────────────────────────────────────┐
│ Título: Apartamento X │ Badge: XX m² │
├─────────────────────┬───────────────────┤
│ Plano 2D │ Renders │
│ (placeholder) │ (placeholder) │
├─────────────────────┼───────────────────┤
│ Vista 3D │ Renders │
│ (placeholder) │ (placeholder) │
├─────────────────────┴───────────────────┤
│ Distribución por Estancias │
│ • Habitación: XX m² │
│ • Cocina: XX m² │
│ • Baño: XX m² │
├─────────────────────────────────────────┤
│ Stats: Hab │ Baños │ Estancias │ m² │
├─────────────────────────────────────────┤
│ Observaciones del proyecto │
└─────────────────────────────────────────┘
```

### 4. Estilo visual
- Fondo blanco, sombras sutiles
- Acentos azul (#2563eb)
- Tipografía limpia (Segoe UI, system fonts)
- Layout responsive con CSS Grid

## Ejemplo de extracción de datos

```python
apartments = [
    {
        "numero": 1,
        "superficie_m2": 25.46,
        "tipo": "Estudio",
        "estancias": [
            {"nombre": "Habitación principal", "area_m2": 18.50, "tipo": "dormitorio"},
            {"nombre": "Cocina americana", "area_m2": 4.20, "tipo": "cocina"},
            {"nombre": "Baño completo", "area_m2": 2.76, "tipo": "baño"}
        ],
        "observaciones": "Diseño compacto y funcional..."
    }
]
```

## Pitfalls

### 🔴 Planos escaneados (imágenes)
Si el PDF contiene imágenes escaneadas en vez de texto seleccionable:
- Usar `ocr-quirurgico-pdf-md` para OCR
- O `pdf-llm-extraction` con análisis de fuentes

### 🔴 Datos implícitos en gráficos
Los planos arquitectónicos suelen mostrar áreas en el gráfico pero no en texto:
- Buscar patrones como "XX.XX m²" en el texto
- Si no hay texto, usar visión para extraer datos del gráfico

### 🔴 Duplicados entre páginas
Los mismos apartamentos pueden aparecer en múltiples páginas (vistas diferentes):
- Usar sets para deduplicar por número de apartamento
- Validar que áreas sean consistentes

### 🔴 Renders no están en el PDF
Los renders interiores normalmente NO están en el plano de distribución:
- Dejar placeholders para imágenes externas
- O generar renders con herramientas 3D aparte

## Template HTML mínimo

Ver `templates/ficha-apartamento.html` para boilerplate completo.

## Referencias
- PyMuPDF: extracción de texto y análisis de fuentes
- CSS Grid: layout responsive de 2 columnas
- Print CSS: exportación a PDF con @media print

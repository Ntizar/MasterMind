# Real Estate Property Cards - Reference

## Project Pattern: Residential Building Property Sheets

Complete workflow for creating technical property cards from architectural plans.

### Source Material
- **PDF architectural plans** with floor layouts and room areas
- **Reference image** showing desired output format
- **Data extraction** from PDF using PyMuPDF

### Data Extraction from PDFs

```python
import fitz
import re

def extract_apartment_data(pdf_path):
    doc = fitz.open(pdf_path)
    apartments = []
    
    for page in doc:
        text = page.get_text()
        
        # Pattern: "Apartamento X" followed by area
        apt_matches = re.finditer(
            r'Apartamento\s+(\d+).*?(\d+\.?\d*)\s*m²',
            text, re.DOTALL
        )
        
        for match in apt_matches:
            apt_num = int(match.group(1))
            area = float(match.group(2))
            
            # Extract rooms
            rooms = []
            room_pattern = r'(Habitación|Cocina|Baño|Salón|Recibidor)\s*(\d*)\s*(\d+\.?\d*)\s*m²'
            for room_match in re.finditer(room_pattern, text):
                rooms.append({
                    'name': f"{room_match.group(1)} {room_match.group(2)}".strip(),
                    'area': float(room_match.group(3))
                })
            
            apartments.append({
                'number': apt_num,
                'total_area': area,
                'rooms': rooms
            })
    
    doc.close()
    return apartments
```

### HTML Structure Pattern

```html
<div class="apartment-card">
    <div class="card-header">
        <div class="apt-title-group">
            <span class="apt-number">Apartamento 1</span>
            <span class="apt-type">Estudio</span>
        </div>
        <div class="apt-badge">
            <span class="apt-floor">📍 Semisótano</span>
            <span class="apt-area">25.46 m²</span>
        </div>
    </div>
    
    <div class="main-grid">
        <div>
            <div class="section-title">Plano de Distribución</div>
            <div class="plan-box">
                <!-- SVG floor plan here -->
            </div>
        </div>
        
        <div>
            <div class="section-title">Renders Interiores</div>
            <div class="renders-grid">
                <div class="render-box">
                    <div class="render-header">🛏️ Render Principal</div>
                    <div class="render-content render-dormitorio">
                        <!-- CSS-rendered interior -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">1</div>
            <div class="stat-label">Habitaciones</div>
        </div>
        <!-- More stats -->
    </div>
    
    <div class="observations">
        <div class="obs-title">📝 Observaciones</div>
        <div class="obs-text">Diseño compacto y funcional...</div>
    </div>
</div>
```

### CSS Design System

**Colors:**
- Primary: `#2563eb` (blue)
- Background: `#f5f6f8` (light gray)
- Card: `#ffffff` (white)
- Bedroom: `#e8f5e9` (green)
- Kitchen: `#fff3e0` (orange)
- Bathroom: `#e3f2fd` (blue)
- Living: `#f3e5f5` (purple)

**Typography:**
- Font: `'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif`
- Headings: 28px, weight 800
- Body: 14-16px, weight 400
- Labels: 12px, weight 700, uppercase

**Spacing:**
- Card padding: 32px
- Section gap: 24px
- Element gap: 16px

### GitHub Pages Deployment

**Workflow file:** `.github/workflows/deploy.yml`

**Steps:**
1. Create repository
2. Add workflow file
3. Push to master
4. Wait 2-5 minutes for deployment

**URL pattern:** `https://username.github.io/repo-name/`

### Export to PDF

**Instructions for users:**
1. Open page in browser
2. Ctrl+P (Cmd+P on Mac)
3. Select "Save as PDF"
4. Format: Landscape
5. Margins: Minimum

### Example Projects

- **Residencia Estudiantes Tajo:** 9 apartments (studios + 1-2 bedroom units)
- **Fichas:** Complete cards with floor plans, renders, room lists, statistics
- **Repo:** github.com/Ntizar/fichas-residencia-tajo

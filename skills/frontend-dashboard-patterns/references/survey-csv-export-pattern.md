# Survey Form + CSV Export — Formularios de recolección zero-install

## El patrón

Formularios HTML progresivos (multi-sección) que recolectan datos estructurados y exportan a CSV UTF-8 con BOM (compatible con Excel). Todo funciona en el navegador, sin backend, sin instalación.

## Arquitectura

```
encuesta.html (autocontenido, ~900-1000 líneas)
├── CSS inline (Aurora style, responsive)
├── 5-7 secciones con cards
│   ├── Datos personales (nombre, depto, centro)
│   ├── Modalidad trabajo (teletrabajo slider)
│   ├── Modo transporte (option cards con iconos)
│   ├── Entorno (paradas TP, parking)
│   ├── Actitud (disposición, barreras, alternativas)
│   └── Resumen + export
├── Progress bar sticky
├── Navegación Siguiente/Anterior
└── JavaScript
    ├── selectOption() — radio cards con click
    ├── updateSlider() — sliders con display
    ├── collectData() — FormData → objeto
    ├── exportCSV() — Blob UTF-8 + BOM + download
    ├── copyToClipboard() — navigator.clipboard
    └── generateSummary() — cards + tabla preview
```

## Option Cards — patrón visual

```html
<div class="option-grid">
    <label class="option-card" onclick="selectOption(this, 'modo')">
        <input type="radio" name="modo_principal" value="coche_particular" required>
        <div class="icon">🚗</div>
        <div class="label">Coche particular</div>
        <div class="sublabel">Solo conductor</div>
    </label>
    <!-- más opciones... -->
</div>
```

```javascript
function selectOption(card, groupName) {
    const group = card.closest('.option-grid');
    group.querySelectorAll('.option-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    card.querySelector('input').checked = true;

    // Conditional visibility
    if (groupName === 'teletrabajo') {
        const val = card.querySelector('input').value;
        document.getElementById('diasPresencialGroup').style.display =
            (val !== 'total' && val !== 'nunca') ? 'block' : 'none';
    }
}
```

## CSV Export — UTF-8 con BOM para Excel

```javascript
function exportCSV() {
    const data = collectData(); // FormData → objeto
    const headers = Object.keys(data);
    const csv = [
        headers.join(','),
        headers.map(h => `"${(data[h] || '').replace(/"/g, '""')}"`).join(',')
    ].join('\n');

    const BOM = '\uFEFF'; // UTF-8 BOM — CRÍTICO para Excel
    const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `encuesta_${data.nombre.replace(/\s+/g, '_')}_${data.fecha}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}
```

**Pitfall:** Sin el BOM (`\uFEFF`), Excel interpreta el CSV como ANSI y tildes/ñ se rompen.

## collectData() — Validación de campos requeridos

```javascript
function collectData() {
    const form = document.getElementById('surveyForm');
    const fd = new FormData(form);

    const required = ['nombre', 'departamento', 'centro', 'modo_principal'];
    for (const field of required) {
        if (!fd.get(field)) {
            alert(`Completa: ${field.replace(/_/g, ' ')}`);
            return null;
        }
    }

    // Checkboxes → arrays
    const secundarios = fd.getAll('modo_secundario');
    const alternativas = fd.getAll('alternativas');

    return {
        fecha: new Date().toISOString().split('T')[0],
        nombre: fd.get('nombre'),
        departamento: fd.get('departamento'),
        modo_principal: fd.get('modo_principal'),
        modo_secundario: secundarios.join('; '),
        distancia_km: fd.get('distancia_km'),
        tiempo_viaje_min: fd.get('tiempo_viaje_min'),
        // ... todos los campos
    };
}
```

## 21 columnas CSV típicas para PMST

```
fecha, nombre, email, departamento, puesto, centro, teletrabajo,
dias_presenciales, modo_principal, modo_secundario, distancia_km,
tiempo_viaje_min, ocupacion_coche, parada_cercana, tipo_parada,
tiempo_a_parada, parking_trabajo, dispuesto_cambiar, alternativas,
barreras, comentarios
```

## Progress Bar sticky

```html
<div class="progress-bar" style="position:sticky;top:0;z-index:100">
    <div class="progress-track">
        <div class="progress-fill" id="progressFill" style="width:0%"></div>
    </div>
    <div class="progress-text">
        <span id="progressLabel">Sección 1 de 6</span>
        <span id="progressPct">0%</span>
    </div>
</div>
```

## Referencia de sesión

- Proyecto: PLANDEMOVILIDAD v2.0
- Archivo: `encuesta.html` (990 líneas, 6 secciones)
- 21 columnas CSV, responsive, 100% local
- Export compatible con Excel (UTF-8 BOM)

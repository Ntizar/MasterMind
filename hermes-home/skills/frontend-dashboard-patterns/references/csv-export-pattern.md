# CSV Export Pattern — Referencia Completa

Patrón de exportación de datos a CSV para apps web con backend Express.

## Código Backend Completo

```javascript
app.get('/api/export/csv', (req, res) => {
  try {
    const db = readDB();
    const { tipo } = req.query;

    const escapeCSV = (val) => {
      const s = String(val == null ? '' : val);
      if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
        return '"' + s.replace(/"/g, '""') + '"';
      }
      return s;
    };

    const toCSV = (headers, rows) => {
      const lines = [headers.join(',')];
      for (const row of rows) {
        lines.push(row.map(escapeCSV).join(','));
      }
      return lines.join('\n');
    };

    let csv = '';
    let filename = 'export';

    if (tipo === 'peso') {
      filename += '-peso';
      csv = toCSV(['fecha', 'hora', 'peso_kg', 'notas'],
        (db.peso || []).map(p => [p.fecha, p.hora, p.peso_kg, p.notas]));
    } else if (tipo === 'comidas') {
      filename += '-comidas';
      csv = toCSV(['fecha', 'hora', 'tipo', 'descripcion', 'kcal', 'proteinas_g', 'hidratos_g', 'grasas_g', 'notas'],
        (db.comidas || []).map(c => [c.fecha, c.hora, c.tipo, c.descripcion, c.kcal, c.proteinas_g, c.hidratos_g, c.grasas_g, c.notas]));
    } else if (tipo === 'all') {
      const sections = [];
      sections.push('=== PESO ===');
      sections.push(toCSV(['fecha', 'hora', 'peso_kg', 'notas'], (db.peso || []).map(p => [p.fecha, p.hora, p.peso_kg, p.notas])));
      sections.push('');
      sections.push('=== COMIDAS ===');
      sections.push(toCSV(['fecha', 'hora', 'tipo', 'descripcion', 'kcal', 'proteinas_g', 'hidratos_g', 'grasas_g', 'notas'],
        (db.comidas || []).map(c => [c.fecha, c.hora, c.tipo, c.descripcion, c.kcal, c.proteinas_g, c.hidratos_g, c.grasas_g, c.notas])));
      csv = sections.join('\n');
    }

    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
    res.setHeader('Content-Disposition', 'attachment; filename="' + filename + '.csv"');
    res.send('\uFEFF' + csv);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

## Código Frontend Completo

### Modal HTML
```html
<div id="exportModal" style="display:none;position:fixed;inset:0;z-index:100000;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);align-items:center;justify-content:center;">
  <div style="background:rgba(255,255,255,0.95);backdrop-filter:blur(16px);border-radius:16px;padding:24px;max-width:480px;width:90%;">
    <h3>📥 Exportar Datos a CSV</h3>
    <button onclick="downloadCSV('all')">📋 Todo</button>
    <button onclick="downloadCSV('peso')">⚖️ Peso</button>
  </div>
</div>
```

### JS Functions
```javascript
function showExportModal() {
  document.getElementById('exportModal').style.display = 'flex';
}
function closeExportModal() {
  document.getElementById('exportModal').style.display = 'none';
}
document.addEventListener('click', (e) => {
  const modal = document.getElementById('exportModal');
  if (modal && e.target === modal) closeExportModal();
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeExportModal();
});
function downloadCSV(tipo) {
  const a = document.createElement('a');
  a.href = '/api/export/csv?tipo=' + encodeURIComponent(tipo);
  a.download = '';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => {
    showToast('¡Exportado!', 'CSV descargado', 'success');
    closeExportModal();
  }, 800);
}
```

## Reglas

1. **BOM UTF-8** — siempre `\uFEFF` al inicio para Excel
2. **Escape de comas** — campos con `,`, `"`, `\n` deben ir entre comillas
3. **No usar `fetch()`** — usar `<a>` element para descarga de archivos
4. **Headers en español** — nombres descriptivos para el usuario
5. **Modal accesible** — cerrar con backdrop click o Escape key

## Historial

- **2026-06-13** — Implementado en MasterFit v3.2 (dieta-masterfit). Backend endpoint `/api/export/csv` con soporte para peso, comidas, entrenamientos, pasos, agua, inbody y todo. Frontend modal con 7 opciones de exportación.

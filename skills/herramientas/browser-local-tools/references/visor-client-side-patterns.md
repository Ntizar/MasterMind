# Visor Client-Side Patterns — Export y Paginación sin servidor

Patrones para visores standalone (file://, sin backend): export CSV filtrado y paginación client-side.

**Proyecto:** CIAF Visor CSV (`/root/workspace/ciafvisorcsv/visor.html`)

## 1. Export CSV filtrado — 100% client-side (sin backend)

A diferencia del patrón backend (`frontend-dashboard-patterns/references/csv-export-pattern.md`), este funciona sin servidor usando `Blob` + `URL.createObjectURL`. Ideal para visores standalone abiertos con `file://`.

```javascript
function exportFilteredCSV() {
    if (filteredReports.length === 0) {
        alert('No hay informes para exportar.');
        return;
    }

    // Construir CSV manualmente desde objetos en memoria
    const headers = Object.keys(filteredReports[0]);
    const csvLines = [headers.join(',')];

    filteredReports.forEach(row => {
        const values = headers.map(h => {
            let val = row[h] || '';
            // Escapar comillas y envolver en comillas si contiene comas o saltos
            val = String(val).replace(/"/g, '""');
            if (val.includes(',') || val.includes('\n') || val.includes('"')) {
                val = `"${val}"`;
            }
            return val;
        });
        csvLines.push(values.join(','));
    });

    // BOM UTF-8 para Excel + Blob download (funciona en file://)
    const csvContent = '\ufeff' + csvLines.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `CIAF-filtrado-${new Date().toISOString().slice(0,10)}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url); // Limpiar memoria
}
```

**Diferencias clave vs. patrón backend:**

| Aspecto | Backend (Express) | Client-side (este patrón) |
|---------|------------------|--------------------------|
| URL | `/api/export/csv?tipo=...` | `URL.createObjectURL(blob)` |
| Servidor | Requerido | No necesario |
| file:// | No funciona | ✅ Funciona |
| Datos | Query backend | Objetos en memoria (filteredReports) |
| Filtro | Backend filtra | JS ya tiene filteredReports |
| BOM | `res.send('\uFEFF')` | `'\ufeff' + csvContent` |

**Reglas:**
1. Siempre `URL.revokeObjectURL(url)` después del click — evita memory leaks
2. BOM `\ufeff` al inicio para que Excel detecte UTF-8
3. Escape `"` → `""` y envolver en comillas si hay comas/saltos
4. Filename con fecha: `CIAF-filtrado-2026-07-04.csv`

## 2. Paginación client-side

Para visores con cientos de informes, paginar en lugar de renderizar todo:

```javascript
let currentPage = 1;
const PAGE_SIZE = 25;

function renderTable() {
    const tbody = document.getElementById('tableBody');
    if (filteredReports.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align:center">Sin resultados</td></tr>';
        return;
    }

    // Slice para página actual
    const start = (currentPage - 1) * PAGE_SIZE;
    const end = start + PAGE_SIZE;
    const pageData = filteredReports.slice(start, end);

    tbody.innerHTML = pageData.map((r, i) => {
        const globalIdx = start + i; // Índice global para modal
        return `<tr onclick="showDetail(${globalIdx})">
            <td>${r.expediente || ''}</td>
            <td>${r.fecha_suceso || ''}</td>
            <!-- más columnas -->
        </tr>`;
    }).join('');
}

function renderPagination() {
    const totalPages = Math.ceil(filteredReports.length / PAGE_SIZE);
    const pag = document.getElementById('pagination');

    if (totalPages <= 1) {
        pag.innerHTML = `<span class="page-info">${filteredReports.length} informe(s)</span>`;
        return;
    }

    let html = '';
    // First + Prev
    html += `<button onclick="goPage(1)" ${currentPage === 1 ? 'disabled' : ''}>«</button>`;
    html += `<button onclick="goPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>‹</button>`;

    // Pages cercanas (ventana de 5)
    const start = Math.max(1, currentPage - 2);
    const end = Math.min(totalPages, currentPage + 2);
    for (let p = start; p <= end; p++) {
        html += `<button onclick="goPage(${p})" class="${p === currentPage ? 'active' : ''}">${p}</button>`;
    }

    // Next + Last
    html += `<button onclick="goPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>›</button>`;
    html += `<button onclick="goPage(${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>»</button>`;
    html += `<span class="page-info">Página ${currentPage} de ${totalPages} (${filteredReports.length} informes)</span>`;
    pag.innerHTML = html;
}

function goPage(p) {
    currentPage = p;
    renderTable();
    renderPagination();
    // Scroll suave arriba de la tabla
    document.querySelector('.table-container').scrollIntoView({ behavior: 'smooth', block: 'start' });
}
```

**Reglas:**
1. `PAGE_SIZE = 25` — balance entre scroll excesivo y demasiadas páginas
2. Ventana de 5 páginas (actual ±2) — evita 50 botones cuando hay 1000 informes
3. `«` `‹` `1` `2` `3` `›` `»` — navegación completa (first, prev, pages, next, last)
4. `scrollIntoView` al cambiar de página — UX: el usuario ve la primera fila de la nueva página
5. `globalIdx = start + i` — el modal necesita el índice en `filteredReports`, no el local de la página
6. Reset `currentPage = 1` al aplicar filtros — evitar página vacía tras filtrar

## 3. Filtros + ordenación + paginación — flujo completo

```javascript
function applyFilters() {
    // 1. Filtrar
    filteredReports = allReports.filter(r => { /* criterios */ });

    // 2. Ordenar (si hay columna activa)
    if (sortColumn) sortData();

    // 3. Reset paginación
    currentPage = 1;

    // 4. Renderizar todo
    renderStats();
    renderTable();
    renderPagination();
}
```

**Orden de operaciones crítico:** filtrar → ordenar → reset página → renderizar. Si se ordena antes de filtrar, el orden se pierde al filtrar.

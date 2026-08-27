# HTML Escaping in Frontend Dashboards — Patrón de escaping correcto

Cuando un frontend vanilla JS renderiza datos del backend (JSON), hay un error común que aparece una y otra vez: **escapar HTML después de construirlo**.

## El error clásico

```javascript
// MAL — esto muestra <strong>64/2024-1:</strong> como texto literal
function truncateText(text, maxLen) {
    if (text.length <= maxLen) return escapeHtml(text);
    return escapeHtml(text.substring(0, maxLen)) + '…';
}

// En el caller:
const rec = `<strong>${rec.numero}:</strong> ${rec.texto}`;
// Luego: truncateText(rec, 500) → escapeHtml destruye los <strong>
```

## La solución

```javascript
// BIEN — truncateText NO escapa HTML
function truncateText(text, maxLen) {
    if (!text) return '';
    if (text.length <= maxLen) return text;  // ← sin escapeHtml
    return text.substring(0, maxLen) + '…';
}

// En el caller: escapar SOLO el contenido raw, ANTES de añadir tags
const html = `<strong>${escapeHtml(rec.numero)}:</strong> ${escapeHtml(rec.texto)}`;
// Luego: truncateText(html, 500) → las tags sobreviven
```

## Regla de oro

**`escapeText()` ANTES de combinar con HTML, NUNCA después.**

```javascript
// Patrón correcto para listas con HTML intencional:
const items = data.map(item => {
    const safeText = escapeHtml(item.texto);    // 1. Escapar contenido raw
    const label = item.numero
        ? `<strong>${item.numero}:</strong> `    // 2. Añadir tags HTML
        : '';
    return `<li>${label}${safeText}</li>`;       // 3. Combinar
});
```

## Verificación

Si ves `<strong>` o `<em>` como texto plano en el navegador:
1. Busca `escapeHtml` o `textContent` en la cadena de rendering
2. Verifica que `escapeHtml` se aplica SOLO al contenido raw, no al HTML construido
3. Si usas `textContent` en vez de `innerHTML`, las tags nunca se renderizan — cámbialo

## El pitfall del `setTxt` utility

Muchos dashboards definen una función helper como:
```javascript
const setTxt = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
};
```

Esto funciona para datos simples (números, texto), pero **escapa HTML silenciosamente**. Si construyes HTML con `<div>`, `<span>`, etc. y lo pasas por `setTxt`, se muestra como texto crudo.

```javascript
// ❌ MAL — el HTML se muestra como texto
const html = `<div style="display:flex;">${name}</div>`;
setTxt('tab-summary', html);  // Muestra: <div style="display:flex;">Energía</div>

// ✅ BIEN — usar innerHTML directamente
const el = document.getElementById('tab-summary');
if (el) el.innerHTML = html;
```

**Regla:** Si el contenido contiene tags HTML, NUNCA usar `setTxt`/`textContent`. Usar `innerHTML` directamente.

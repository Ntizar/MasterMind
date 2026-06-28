# Kaizen Sidebar Override Pattern — CSS Inheritance Pitfalls

When a project uses **Kaizen Design System** (`kaizen.css`) and adds custom overrides (`time-custom.css`, etc.), the Kaizen CSS defines sidebar styles for a **navigation list** use case. Projects that use the sidebar for **forms/controls** (inputs, chips, buttons) inherit mismatched defaults.

## The Problem

Kaizen CSS defines:
```css
/* For NAVIGATION lists — not forms */
.kz-sidebar-category {
  display: flex;
  justify-content: space-between;  /* pushes ▾ arrow to far right */
  border-bottom: 3px solid var(--kz-azul);  /* thick blue bottom */
}
.kz-sidebar-item {
  display: flex;
  justify-content: space-between;  /* pushes form elements apart */
  cursor: pointer;                 /* misleading for form elements */
  border-bottom: 1px solid var(--kz-gris-100);  /* unnecessary separators */
}
```

If `time-custom.css` only overrides `padding` and `border-top` without addressing `display`, `justify-content`, `cursor`, and `border-bottom`, the sidebar looks broken.

## Symptoms

1. **Double borders** on category headers — thick blue bottom (Kaizen) + thin gray top (custom)
2. **▸ arrows pushed to far right** — `justify-content: space-between` separates text from arrow
3. **Input/button squeezed** — flex layout pushes form elements to opposite edges
4. **Cursor: pointer everywhere** — misleading on non-interactive elements
5. **Unnecessary borders** between form elements

## Fix Pattern

In the custom CSS override file, add these overrides **after** the Kaizen import:

```css
/* ============================================
   KAIZEN OVERRIDES — Sidebar for FORM use case
   ============================================ */

/* Categories: remove Kaizen's flex + border-bottom, keep custom border-top */
.kz-sidebar-category {
  display: block;              /* Override Kaizen's flex */
  justify-content: normal;     /* Override space-between */
  cursor: default;             /* Not clickable */
  border-bottom: none;         /* Remove Kaizen's thick blue bottom */
  /* Keep your custom border-top and padding */
}

/* Items: remove flex + border + cursor for form content */
.kz-sidebar-item {
  display: block;              /* Override Kaizen's flex */
  justify-content: normal;     /* Override space-between */
  cursor: default;             /* Not a nav item */
  border-bottom: none;         /* No separators between form elements */
  /* Keep your custom padding */
}
```

## Detection Checklist

When auditing a project that uses Kaizen CSS:

```bash
# 1. Check if Kaizen is loaded
grep -l 'kaizen.css' index.html

# 2. Check if custom CSS overrides are sufficient
grep -c 'justify-content' css/time-custom.css  # If 0, Kaizen's space-between leaks through
grep -c 'cursor.*default\|cursor.*auto' css/time-custom.css  # If 0, cursor: pointer leaks through
grep 'border-bottom.*none\|border-bottom.*0' css/time-custom.css  # If missing, Kaizen's thick border leaks

# 3. Quick visual check — does the sidebar have ▾ arrows pushed to far right?
# If yes, categories need display: block override
```

## Projects Affected

- **Time** (TimeIneco) — sidebar with form controls, chips, checkboxes
- Any future project using `kz-grid-sidebar` + `kz-sidebar` for non-navigation content

## Related Kaizen Pitfalls

- `kz-btn-primary` with `width: 100%` — needs `display: block` override on parent `.kz-sidebar-item` to actually fill width
- `.kz-chips` flex-wrap — works correctly from Kaizen, no override needed
- `.kz-header` with `position: sticky` — works correctly, keeps header visible while scrolling sidebar

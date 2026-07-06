# Treemap + Shelf-Packing Algorithm

**Source:** CallesDinamicas v2 (2026-07-06) — dense treemap cell filling
**Use case:** Any visualization where items need to fill rectangular cells proportionally (streets by angle, files by type, products by category, etc.)

## Problem

Naive treemap: each item is centered at its centroid within its cell → tiny dots, wasted space.
Correct treemap: items are **shelf-packed** to fill the entire cell densely.

## Algorithm

### Step 1: Squarified Treemap Layout

Recursively divide a rectangle into cells proportional to each group's "area" (total length, count, size, etc.).

```javascript
function squarify(items, x, y, w, h) {
  // items: [{idx, area}] — sorted descending by area
  // Returns: [{idx, x, y, w, h}]
  if (!items.length) return [];
  const total = items.reduce((s, i) => s + i.area, 0);
  const rects = [];
  layoutRow(items, x, y, w, h, total, rects);
  return rects;
}

function layoutRow(items, x, y, w, h, totalArea, rects) {
  if (!items.length) return;
  if (items.length === 1) {
    rects.push({ idx: items[0].idx, x, y, w, h });
    return;
  }
  const vertical = w >= h;
  let bestAspect = Infinity, bestSplit = 1, running = 0;
  for (let i = 0; i < items.length; i++) {
    running += items[i].area;
    const frac = running / totalArea;
    const aspect = vertical
      ? Math.max((w * frac) / h, h / (w * frac))
      : Math.max(w / (h * frac), (h * frac) / w);
    if (aspect < bestAspect) { bestAspect = aspect; bestSplit = i + 1; }
  }
  const row = items.slice(0, bestSplit);
  const rest = items.slice(bestSplit);
  const rowArea = row.reduce((s, i) => s + i.area, 0);
  const frac = rowArea / totalArea;
  if (vertical) {
    const rowW = w * frac;
    let yy = y;
    for (const item of row) {
      const ih = h * (item.area / rowArea);
      rects.push({ idx: item.idx, x, y: yy, w: rowW, h: ih });
      yy += ih;
    }
    layoutRow(rest, x + rowW, y, w - rowW, h, totalArea - rowArea, rects);
  } else {
    const rowH = h * frac;
    let xx = x;
    for (const item of row) {
      const iw = w * (item.area / rowArea);
      rects.push({ idx: item.idx, x: xx, y, w: iw, h: rowH });
      xx += iw;
    }
    layoutRow(rest, x, y + rowH, w, h - rowH, totalArea - rowArea, rects);
  }
}
```

### Step 2: Shelf-Packing Within Each Cell

Pack items into each cell like books on a shelf — sorted by size, filling rows left-to-right.

```javascript
function shelfPack(streets, cellX, cellY, cellW, cellH, rotAngle) {
  const cosR = Math.cos(rotAngle), sinR = Math.sin(rotAngle);
  // Sort longest first (better packing)
  streets.sort((a, b) => b.len - a.len);
  
  let curX = 0, curY = 0, rowH = 0;
  const packed = [];
  const GAP = 1;
  
  for (const st of streets) {
    // Rotated bounding box
    const w0 = st.bex - st.bsx, h0 = st.bey - st.bsy;
    const rw = Math.abs(w0 * cosR) + Math.abs(h0 * sinR);
    const rh = Math.abs(w0 * sinR) + Math.abs(h0 * cosR);
    
    if (curX + rw > cellW && curX > 0) {
      curX = 0; curY += rowH + GAP; rowH = 0;
    }
    if (curY + rh > cellH) continue; // won't fit — skip
    
    // Translate: move street bbox origin to (curX, curY) within cell
    const tx = cellX + curX - st.bsx * cosR + st.bsy * sinR;
    const ty = cellY + curY - st.bsx * sinR - st.bsy * cosR;
    
    packed.push({ st, tx, ty, cosR, sinR });
    curX += rw + GAP;
    if (rh > rowH) rowH = rh;
  }
  return packed;
}
```

### Step 3: Render

```javascript
for (const pk of packed) {
  ctx.strokeStyle = color;
  ctx.lineWidth = tierWidths[pk.st.tier];
  ctx.beginPath();
  for (let j = 0; j < pk.st.pts.length; j += 2) {
    const x = pk.st.pts[j], y = pk.st.pts[j + 1];
    const rx = x * pk.cosR - y * pk.sinR;
    const ry = x * pk.sinR + y * pk.cosR;
    const sx = pk.tx + rx, sy = pk.ty + ry;
    j === 0 ? ctx.moveTo(sx, sy) : ctx.lineTo(sx, sy);
  }
  ctx.stroke();
}
```

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Sort order | Longest first | Longest items create the structure, small ones fill gaps |
| Packing direction | Left-to-right, top-to-bottom | Natural reading order, easy to debug |
| Overflow handling | Skip (continue) | Items that don't fit are omitted — longest items dominate |
| Gap between items | 1px | Prevents visual merging of same-color items |
| Gap between cells | 4px | Shows treemap structure clearly |
| Cell background | #f5f5f5 with #e0e0e0 border | Subtle but visible structure |

## Adaptation Examples

- **File system treemap:** area = file size, items = files, bins = file type
- **Product catalog:** area = revenue, items = products, bins = category
- **Budget visualization:** area = budget line, items = sub-items, bins = department
- **Font/character distribution:** area = frequency, items = characters, bins = script

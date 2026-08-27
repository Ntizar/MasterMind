# KaTeX Double-Escape Fix — DeSumarIntegrar

## Problema

En el `<head>` de algunos HTML, el script de auto-render de KaTeX tiene la barra invertida escapada doblemente:

```html
<!-- ROTO: 4 barras invertidas -->
<script ... onload="renderMathInElement(document.body,{delimiters:[{left:'\\\\[',right:'\\\\]',display:true},{left:'\\(',right:')',display:false}]})"></script>
```

Esto hace que KaTeX busque `\\[` literalmente en lugar de `\[`, por lo que **no renderiza nada**.

## Detección

```bash
# Detectar doble escape en el head
grep '\\\\\\\\[' /root/workspace/DeSumarIntegrar/*.html
# Si devuelve resultados → está roto

# Contar ocurrencias
grep -c '\\\\\\\\[' /root/workspace/DeSumarIntegrar/*.html
```

## Fix

```bash
# Reemplazar en el archivo
sed -i "s/\\\\\\\\\\[/\\\\[/g; s/\\\\\\\\]/\\\\]/g; s/\\\\\\\\(/\\\\(/g; s/\\\\\\\\)/\\\\)/g" file.html
```

O con `patch` en el `<script>` del `<head>`:
```html
<!-- CORRECTO: 2 barras invertidas (escape HTML + escape JS) -->
<script ... onload="renderMathInElement(document.body,{delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:')',display:false}]})"></script>
```

## Causa

El `patch` tool o `write_file` pueden escapar barras invertidas adicionales cuando el contenido viene de un contexto que ya tiene escapes (JSON, terminal, etc.).

## Verificación post-fix

```bash
# Debe devolver 0 ocurrencias de doble escape
grep -c '\\\\\\\\[' file.html  # → 0

# Debe tener escapes simples
grep -c '\\\\[' file.html  # → 1 (en el script del head)
```

## Archivos afectados conocidos

- `s08-2-3eso.html` — corregido en sesión 2026-06-15

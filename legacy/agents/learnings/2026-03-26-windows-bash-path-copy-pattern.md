---
fecha: 2026-03-26
tarea: windows-bash-path-copy-pattern
tipo: software
clusters:
  - "#sistema"
  - "#github"
patron: windows-bash-forward-slash-copy
decay: normal
---

# Copiar archivos en Windows bash: forward slashes y cp -r

## Contexto
Al intentar copiar archivos del vault al repo con `xcopy` y rutas con backslash, todos los comandos fallaron con "unexpected EOF while looking for matching". El entorno de OpenCode usa bash en Windows (Git Bash/MSYS2).

## Problema
- `xcopy` con comillas dobles y backslashes falla en bash
- Bash interpreta `\` como escape character dentro de comillas dobles
- Backslashes en rutas causan parsing errors silenciosos

## Patron: windows-bash-forward-slash-copy
En entorno bash-on-Windows (OpenCode, Git Bash, WSL):
1. **Siempre usar forward slashes** en rutas: `C:/Users/...` no `C:\Users\...`
2. **Usar `cp -r`** en vez de `xcopy` para copiar directorios
3. **Usar `rm -rf`** en vez de `rmdir /s /q`
4. **Usar `mv`** en vez de `move`
5. Si necesitas un comando Windows nativo, usar `cmd //c "comando"`

## Anti-patron
```bash
# MAL — falla en bash
xcopy "C:\path\source" "C:\path\dest" /E /I /Y

# BIEN — funciona en bash-on-Windows
cp -r "C:/path/source" "C:/path/dest"
```

## Senal de relevancia
Cualquier operacion de archivos en OpenCode sobre Windows.

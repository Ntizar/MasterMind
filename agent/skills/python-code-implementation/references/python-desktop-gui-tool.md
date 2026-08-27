# Python Desktop GUI Tool — Patrón completo spec→repo→exe

## Flujo estándar para crear herramientas de escritorio Python

Cuando el usuario pide una herramienta local (no web), el ciclo completo es:

### 1. Spec (skill: project-spec-workflow)
- Preguntas estructuradas: plataforma, datos, volumen, seguridad
- Generar SPEC.md en el repo
- Esperar ✅ antes de codear

### 2. Estructura de archivos típica
```
nombre-proyecto/
├── main.py              # Entry point
├── gui.py               # Interfaz (tkinter/PyQt)
├── core_logic.py         # Lógica del dominio
├── utils.py             # Utilidades, constantes
├── requirements.txt     # openpyxl, PyPDF2, etc.
├── build.bat            # Script PyInstaller para Windows
├── README.md            # Instrucciones de usuario
├── SPEC.md              # Especificación
└── .gitignore           # Ignorar dist/, build/, __pycache__/
```

### 3. Repo en GitHub (sin gh CLI)
```bash
# Crear repo privado vía API REST
source .env
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d '{"name":"nombre","description":"...","private":true}'

# Init + push
git init && git branch -m main
git remote add origin https://github.com/Ntizar/nombre.git
git add -A && git commit -m "feat: initial"
git push -u origin main
```

### 4. Build ejecutable Windows (build.bat)
```bat
@echo off
pip show pyinstaller >nul 2>&1
if errorlevel 1 pip install pyinstaller

pyinstaller --onefile --windowed --name AppName main.py
copy dist\AppName.exe .
```

**Pitfall:** PyInstaller `--windowed` oculta la consola. Para debugging, lanzar sin `--windowed` o usar `.pyw`.

### 5. Dependencias típicas por tipo de herramienta
| Tipo | Dependencias |
|------|-------------|
| Excel/CSV → procesamiento | openpyxl, pandas |
| PDF lectura/escritura | PyPDF2, pikepdf |
| PDF generation | reportlab, fpdf2 |
| GUI básica | tkinter (stdlib) |
| GUI avanzada | PyQt6, customtkinter |
| HTTP/API | requests |
| Imaging | Pillow |

### 6. Pitfalls de tkinter en Windows
- `tkinter` viene con Python estándar (no necesita pip)
- `filedialog.askdirectory()` bloquea el hilo principal
- Para operaciones largas: usar `threading.Thread` + `root.after()` para actualizar UI
- `messagebox` se usa para confirmaciones (sobrescritura, errores)
- Estilo: `ttk.Style().theme_use('clam')` para aspecto más moderno

### 7. Mapeo automático de columnas
Cuando el Excel tiene columnas dinámicas, mapear por nombre case-insensitive:
```python
COLUMN_MAP = {
    'autor': '/Author',
    'title': '/Title',
    'fecha': '/CreationDate',
    # ... mapear español + inglés
}
```

### 8. Validación antes de procesar
- Verificar que el archivo de entrada existe
- Verificar que los archivos referenciados existen
- Generar resumen de cambios (qué se modificó, qué falló)
- Log a archivo para revisión posterior

### 9. Git commit message convention
```
feat: add [module] — [qué hace]
fix: [qué corrige]
refactor: [qué reestructura]
```

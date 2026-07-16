---
name: corporate-windows-tooling
description: "Crear herramientas de escritorio Windows que funcionen en entornos corporativos restringidos — PowerShell + .NET, sin admin, sin .exe"
version: 1.0.0
author: Mastermind
tags: [windows, powershell, dotnet, corporate, deployment, desktop, portable]
related_skills: [software-development, python-code-implementation]
---

# Corporate Windows Tooling

Patrones para crear herramientas de escritorio que funcionen en entornos corporativos donde PyInstaller `.exe` está bloqueado por políticas de seguridad.

## Trigger

Activar cuando el usuario mencione:
- "No funciona en el ordenador de la empresa"
- "Sin ser administrador no me deja usarlo"
- "Antivirus bloquea el .exe"
- "AppLocker" / "políticas de grupo"
- "No tengo permisos de instalación"
- Necesita herramienta de escritorio Windows para usuarios no técnicos

## Decision Matrix

| Solución | Cuándo usarla | Requisitos |
|----------|--------------|------------|
| **PyInstaller .exe** | Primera opción si no hay restricciones | Python + PyInstaller |
| **PowerShell + .NET** | Entorno corporativo restringido | Windows 10+ (ya incluido) |
| **Batch + Python** | Si Python ya está instalado en los PCs | Python en PATH |
| **HTML + JavaScript** | Solo lectura/exportación, sin modificar archivos | Navegador |

**Regla:** Si el usuario menciona "corporativo", "empresa", "sin admin" → PowerShell + .NET directamente. No preguntar.

## Patrón PowerShell + .NET

### Estructura del proyecto

```
mi-herramienta/
├── ejecutar.bat              # Lanzador (doble clic)
├── src/
│   ├── Mi-Script.ps1        # Script principal
│   └── lib/
│       └── libreria.dll     # Librería .NET (ej: itextsharp.dll)
├── README.md
└── SPEC.md
```

### ejecutar.bat (siempre el mismo patrón)

```batch
@echo off
chcp 65001 >nul 2>&1
title Título de la Herramienta
echo ========================================
echo   Nombre de la Herramienta
echo   Hecho con ❤️ por David Antizar
echo ========================================
echo.
echo Iniciando herramienta...
echo.

:: Verificar si PowerShell está disponible
where powershell.exe >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: No se encontro PowerShell en el sistema.
    pause
    exit /b 1
)

:: Ejecutar script PowerShell
powershell.exe -ExecutionPolicy Bypass -File "%~dp0src\Mi-Script.ps1"

if %errorlevel% neq 0 (
    echo.
    echo La herramienta se cerro con errores.
    pause
)
```

**Pitfall:** `%~dp0` resuelve la ruta relativa al .bat, no al directorio de trabajo actual. Essential para que funcione desde cualquier ubicación.

### Script PowerShell — Cabecera

```powershell
#Requires -Version 5.1
<#
.SYNOPSIS
    Descripción corta
.DESCRIPTION
    Descripción detallada
.NOTES
    Autor: David Antizar (Ntizar)
    Hecho con ❤️ por David Antizar
#>

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LibDir = Join-Path $ScriptDir "lib"
$LibDll = Join-Path $LibDir "libreria.dll"
```

### Cargar librería .NET

```powershell
if (-not (Test-Path $LibDll)) {
    [System.Windows.Forms.MessageBox]::Show(
        "No se encuentra libreria.dll en:`n$LibDir",
        "Error", "OK", "Error"
    )
    exit 1
}
Add-Type -Path $LibDll
```

### GUI con Windows Forms

```powershell
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = "Título - David Antizar"
$form.Size = New-Object System.Drawing.Size(800, 650)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedSingle"
$form.MaximizeBox = $false
$form.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$form.BackColor = [System.Drawing.Color]::White
```

### Leer Excel con COM (sin librería externa)

```powershell
function Read-ExcelFile {
    param([string]$RutaArchivo)
    
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    $workbook = $excel.Workbooks.Open($RutaArchivo)
    $worksheet = $workbook.Sheets[1]
    
    $usedRange = $worksheet.UsedRange
    $filas = $usedRange.Rows.Count
    $columnas = $usedRange.Columns.Count
    
    # Cabeceras (primera fila)
    $cabeceras = @()
    for ($col = 1; $col -le $columnas; $col++) {
        $cabeceras += $worksheet.Cells.Item(1, $col).Text
    }
    
    # Datos
    $datos = @()
    for ($fila = 2; $fila -le $filas; $fila++) {
        $valores = @{}
        for ($col = 1; $col -le $columnas; $col++) {
            $valores[$cabeceras[$col-1]] = $worksheet.Cells.Item($fila, $col).Text
        }
        $datos += [PSCustomObject]$valores
    }
    
    $workbook.Close($false)
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    
    return @{ Cabeceras = $cabeceras; Datos = $datos }
}
```

**Pitfall:** Sin `[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel)`, el proceso EXCEL.EXE queda zombie en segundo plano.

### Escribir Excel con COM

```powershell
function Write-ExcelFile {
    param([string]$RutaArchivo, [array]$Datos)
    
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    $workbook = $excel.Workbooks.Add()
    $worksheet = $workbook.Sheets[1]
    $worksheet.Name = "METADATOS"
    
    $columnas = $Datos[0].PSObject.Properties.Name
    
    # Cabeceras
    for ($col = 0; $col -lt $columnas.Count; $col++) {
        $worksheet.Cells.Item(1, $col + 1) = $columnas[$col]
    }
    
    # Datos
    for ($fila = 0; $fila -lt $Datos.Count; $fila++) {
        for ($col = 0; $col -lt $columnas.Count; $col++) {
            $worksheet.Cells.Item($fila + 2, $col + 1) = $Datos[$fila].$($columnas[$col])
        }
    }
    
    $worksheet.Columns.AutoFit() | Out-Null
    $workbook.SaveAs($RutaArchivo)
    $workbook.Close($false)
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}
```

## Descargar librerías .NET desde NuGet

Si necesitas una librería .NET (ej: iTextSharp para PDFs):

```bash
# Descargar paquete NuGet
curl -sL "https://www.nuget.org/api/v2/package/iTextSharp/5.5.13.4" -o itextsharp.nupkg

# Extraer DLL
python3 -c "
import zipfile
with zipfile.ZipFile('itextsharp.nupkg', 'r') as z:
    z.extractall('itextsharp')
    for f in z.namelist():
        if f.endswith('.dll'):
            print(f)
"
# Resultado: lib/net461/itextsharp.dll

# Copiar al proyecto
cp itextsharp/lib/net461/itextsharp.dll /ruta/proyecto/src/lib/
```

**Pitfall:** Los `.nupkg` son archivos ZIP. Python `zipfile` funciona para extraerlos si `unzip` no está disponible.

## Patrón iTextSharp para PDFs

```powershell
Add-Type -Path "$LibDir\itextsharp.dll"

# Leer metadatos de PDF
$reader = New-Object iTextSharp.text.pdf.PdfReader($RutaPdf)
$info = $reader.Info  # Hashtable con /Title, /Author, etc.
$reader.Close()

# Escribir metadatos en PDF
$tempFile = $RutaPdf + ".tmp"
$reader = New-Object iTextSharp.text.pdf.PdfReader($RutaPdf)
$stamper = New-Object iTextSharp.text.pdf.PdfStamper($reader, [System.IO.File]::Create($tempFile))
$infoDict = $stamper.Writer.Info
$infoDict["/Title"] = "Nuevo título"
$infoDict["/Author"] = "Autor"
$stamper.Close()
$reader.Close()

# Reemplazar original
Remove-Item $RutaPdf -Force
Rename-Item $tempFile $RutaPdf
```

## Pitfalls

1. **Execution Policy Bypass:** Siempre usar `powershell.exe -ExecutionPolicy Bypass -File` en el .bat. Sin esto, PowerShell bloquea scripts por defecto.

2. **COM Excel zombie:** Siempre hacer `ReleaseComObject` después de usar Excel COM. Sino, `EXCEL.EXE` queda en memoria.

3. **iTextSharp 5.x vs 7.x:** iTextSharp 5.5.x es la versión con namespace `iTextSharp.text.pdf`. iTextSharp 7.x cambió a `iText.Kernel.Pdf`. Usar 5.5.x para simplificar.

4. **Ruta relativa:** `%~dp0` en .bat = directorio del .bat. `$MyInvocation.MyCommand.Path` en PowerShell = ruta del script. Nunca usar rutas absolutas hardcodeadas.

5. **GUI PowerShell:** Windows Forms en PowerShell es limitado pero suficiente para herramientas simples. No intentar hacer frameworks complejos.

6. **CSV fallback:** Si Excel no está instalado, el COM approach falla. Ofrecer CSV como alternativa. El usuario puede exportar Excel a CSV.

7. **pyinstaller .exe sin admin:** Si el usuario puede ejecutar .exe pero no instalar Python, PyInstaller sigue siendo la primera opción. PowerShell es solo cuando el .exe está bloqueado por políticas.

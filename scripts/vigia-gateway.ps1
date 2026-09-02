# vigia-gateway.ps1 - Watchdog del Hermes gateway (fuera del gateway, a prueba de muerte)
# Programado en el Task Scheduler de Windows cada 10 minutos.
# Si el gateway esta muerto: lo relanza, avisa por Telegram y deja rastro en logs\vigia-gateway.log
# Si esta vivo: sale en silencio (cero ruido, cero tokens).
$ErrorActionPreference = 'SilentlyContinue'
$hermesHome = Join-Path $env:LOCALAPPDATA 'hermes'
$hermes = Join-Path $hermesHome 'bin\hermes.exe'
$logFile = Join-Path $hermesHome 'logs\vigia-gateway.log'
$stamp = (Get-Date).ToString('s')

$status = (& $hermes gateway status 2>&1) -join ' '
if ($status -notmatch 'No gateway process') { exit 0 }   # vivo: callar

# --- muerto: relanzar ---
& $hermes gateway start 2>&1 | Out-Null
Start-Sleep -Seconds 15
$status2 = (& $hermes gateway status 2>&1) -join ' '

# leer token del .env para avisar (puede estar revocado -> silencio en ese caso)
$token = $null
foreach ($line in Get-Content (Join-Path $hermesHome '.env')) {
  if ($line -match '^TELEGRAM_BOT_TOKEN=(.+)') { $token = $Matches[1].Trim() }
}

# comprobar en el log si Telegram conecto de verdad tras el relanzamiento
$gatewayLog = Join-Path $hermesHome 'logs\gateway.log'
$telegramOk = $false
if (Test-Path $gatewayLog) {
  $tail = Get-Content $gatewayLog -Tail 30 -Raw
  if ($tail -match 'telegram connected') { $telegramOk = $true }
}

if ($status2 -match 'process running') {
  if ($telegramOk) {
    $msg = "[$stamp] vigia-gateway: gateway caido -> relanzado OK (telegram conectado)"
  } else {
    $msg = "[$stamp] vigia-gateway: ALERTA gateway relanzado pero Telegram NO conecta (posible token revocado: revisar con @BotFather y TELEGRAM_BOT_TOKEN en .env)"
  }
} else {
  $msg = "[$stamp] vigia-gateway: ALERTA critica - gateway sigue caido tras el relanzamiento"
}
Add-Content -Path $logFile -Value $msg

if ($token) {
  $body = @{ chat_id = '7288273982'; text = $msg } | ConvertTo-Json
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
  Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -ContentType 'application/json; charset=utf-8' -Body $bytes | Out-Null
}

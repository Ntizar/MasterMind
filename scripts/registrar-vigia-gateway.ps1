# Registra la tarea del watchdog del gateway en el Task Scheduler de Windows
$ErrorActionPreference = 'Stop'
$script = Join-Path $env:LOCALAPPDATA 'hermes\scripts\vigia-gateway.ps1'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$script`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName 'Hermes_Gateway_Watchdog' -Action $action -Trigger $trigger -Settings $settings -Description 'Revive el Hermes gateway si muere y avisa por Telegram (vigia-gateway.ps1)' -Force | Out-Null
Get-ScheduledTask -TaskName Hermes_Gateway_Watchdog | Select-Object TaskName, State | Format-List
Write-Output 'LISTO'

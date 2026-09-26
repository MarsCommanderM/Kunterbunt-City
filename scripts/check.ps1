# Kunterbunt City – ALLE Qualitäts-Tore (Windows). Rot = nicht committen.
# Godot-Pfad: $env:GODOT, sonst godot.exe / godot4.exe im PATH.
Set-Location (Join-Path $PSScriptRoot "..")
$fail = $false
$py = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "py" }
$godot = if ($env:GODOT) { $env:GODOT } else { (Get-Command godot, godot4 -ErrorAction SilentlyContinue | Select-Object -First 1).Source }

Write-Host "`n>> 1/3 Maßstab"; & $py tools/validate_scale.py; if ($LASTEXITCODE -ne 0) { $fail = $true }
Write-Host "`n>> 2/3 Tool-Tests (pytest)"; & $py -m pytest tools/tests -q; if ($LASTEXITCODE -ne 0) { $fail = $true }
Write-Host "`n>> 3/3 Godot-Tests (GUT)"
if (-not $godot) { Write-Host "Godot nicht gefunden – `$env:GODOT setzen"; $fail = $true }
else {
  & $godot --headless --import *> $null
  $out = & $godot --headless -s addons/gut/gut_cmdln.gd -gconfig=res://.gutconfig.json 2>&1 | Out-String
  $code = $LASTEXITCODE
  $out -split "`n" | Where-Object { $_ -match "Totals|Passing|Failing|Failed|SCRIPT ERROR|Parse Error|All tests passed" } | ForEach-Object { Write-Host $_ }
  if ($code -ne 0 -or $out -match "SCRIPT ERROR|Parse Error") { $fail = $true }
}
if ($fail) { Write-Host "`nROT – nicht committen"; exit 1 } else { Write-Host "`nalles grün"; exit 0 }

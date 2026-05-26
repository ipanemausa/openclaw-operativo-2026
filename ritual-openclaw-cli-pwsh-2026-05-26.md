\# Ventana 2: Ritual OC CLI



Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\\Users\\ipane\\openclaw-operativo-2026'; Write-Host '🐳 Ventana 2: Ritual OC CLI' -ForegroundColor Green"



\# En esa ventana, ejecutar luego el ritual:



\# 1. Ir al repo operativo

cd C:\\Users\\ipane\\openclaw-operativo-2026



\# 2. Asegurar que el stack Docker está arriba

docker compose up -d



\# 3. Ver estado del gateway desde la CLI de OpenClaw en Windows

openclaw status --gateway-url http://127.0.0.1:18789



\# 4. (Cuando el dashboard Flask esté sano) generar URL del dashboard con token

openclaw dashboard --gateway-url http://127.0.0.1:18789 --no-open


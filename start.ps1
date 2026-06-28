cd C:\Users\ipane\openclaw-cloud-2026
docker compose ps
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\ipane\openclaw-cloud-2026\frontend; pnpm dev"
Start-Sleep 3
Start-Process "http://localhost:5173"
Write-Host "LAMAUTONOMIA lista." -ForegroundColor Green

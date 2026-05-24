@echo off
schtasks /create /tn "OpenClawWorkspace" /tr "powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\ipane\openclaw-operativo-2026\setup-workspace.ps1" /sc onlogon /ru %USERNAME% /f
echo Task created successfully

# Script para simular el rol de ejecutor de bajo nivel (pwsh CLI) leyendo el estado de Hermes

$yamlPath = ".\state\test_hermes_flow.yaml"
$yamlContent = Get-Content -Path $yamlPath -Raw

Write-Host "--- SIMULACIÓN DE FLUJO MULTIAGENTE ---"
Write-Host "1. Leyendo contrato de estado en $yamlPath..."

if ($yamlContent -match 'status: "pending"') {
    Write-Host "   -> Estado detectado: pending."
    Write-Host "2. Ejecutando Tarea (Paso 1): Creando archivo de prueba..."
    
    # Acción física: crear el archivo de prueba
    if (-not (Test-Path ".\logs")) { New-Item -ItemType Directory -Path ".\logs" | Out-Null }
    Set-Content -Path ".\logs\hermes_test_output.txt" -Value "Flujo multiagente completado con éxito mediante PowerShell. Docker no requerido para esta fase."
    Write-Host "   -> Archivo 'logs\hermes_test_output.txt' creado exitosamente."
    
    Write-Host "3. Actualizando el contrato de estado (Paso 2)..."
    # Actualizamos el estado siguiendo el contrato
    $timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    $yamlContent = $yamlContent -replace 'status: "pending"', 'status: "done"'
    $yamlContent = $yamlContent -replace 'current_step: 1', 'current_step: 2'
    $yamlContent = $yamlContent -replace 'last_actor: "hermes"', 'last_actor: "ps_script"'
    $yamlContent = $yamlContent -replace 'last_update: ".*"', "last_update: `"$timestamp`""
    
    Set-Content -Path $yamlPath -Value $yamlContent
    
    Write-Host "   -> Estado actualizado a 'done' y actor cambiado a 'ps_script'."
    Write-Host "Simulación Completada 100% segura. Ningún sistema de producción fue alterado."
} else {
    Write-Host "   -> El estado no está en pending. No se requiere acción."
}

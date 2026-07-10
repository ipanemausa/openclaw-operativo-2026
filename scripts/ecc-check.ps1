# ECC Check
Write-Host "=== ECC STATUS ===" -ForegroundColor Cyan
$result = curl http://localhost:8090/api/ecc/drift -ErrorAction SilentlyContinue
if ($result) { $result | ConvertFrom-Json }

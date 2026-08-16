Add-Type -AssemblyName System.Windows.Forms

Write-Host "=== PANTALLAS DETECTADAS ===" -ForegroundColor Cyan
[System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
    [PSCustomObject]@{
        DeviceName  = $_.DeviceName
        Primary     = $_.Primary
        X           = $_.Bounds.X
        Y           = $_.Bounds.Y
        Width       = $_.Bounds.Width
        Height      = $_.Bounds.Height
        Orientation = $_.Bounds
    }
} | Format-Table -AutoSize

Write-Host "`n=== DISPOSITIVOS MONITOR (WMI) ===" -ForegroundColor Cyan
$monitors = Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorID
foreach ($m in $monitors) {
    $nameBytes = $m.UserFriendlyName | Where-Object { $_ -ne 0 }
    $name = if ($nameBytes) { [System.Text.Encoding]::ASCII.GetString([byte[]]$nameBytes) } else { "Desconocido" }
    
    $serialBytes = $m.SerialNumberID | Where-Object { $_ -ne 0 }
    $serial = if ($serialBytes) { [System.Text.Encoding]::ASCII.GetString([byte[]]$serialBytes) } else { "N/A" }
    
    [PSCustomObject]@{
        InstanceName = $m.InstanceName
        MonitorName  = $name
        SerialNumber = $serial
    } | Format-Table -AutoSize
}

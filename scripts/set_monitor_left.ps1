Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class DisplayManager {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct DEVMODE {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmDeviceName;
        public short dmSpecVersion;
        public short dmDriverVersion;
        public short dmSize;
        public short dmDriverExtra;
        public int dmFields;
        public int dmPositionX;
        public int dmPositionY;
        public int dmDisplayOrientation;
        public int dmDisplayFixedOutput;
        public short dmColor;
        public short dmDuplex;
        public short dmYResolution;
        public short dmTTOption;
        public short dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public short dmLogPixels;
        public short dmBitsPerPel;
        public int dmPelsWidth;
        public int dmPelsHeight;
        public int dmDisplayFlags;
        public int dmDisplayFrequency;
        public int dmICMMethod;
        public int dmICMIntent;
        public int dmMediaType;
        public int dmDitherType;
        public int dmReserved1;
        public int dmReserved2;
        public int dmPanningWidth;
        public int dmPanningHeight;
    }

    [DllImport("user32.dll", CharSet = CharSet.Ansi)]
    public static extern int EnumDisplaySettings(string lpszDeviceName, int iModeNum, ref DEVMODE lpDevMode);

    [DllImport("user32.dll", CharSet = CharSet.Ansi)]
    public static extern int ChangeDisplaySettingsEx(string lpszDeviceName, ref DEVMODE lpDevMode, IntPtr hwnd, uint dwflags, IntPtr lParam);

    public const int ENUM_CURRENT_SETTINGS = -1;
    public const int DM_POSITION = 0x00000020;
    public const int CDS_UPDATEREGISTRY = 0x00000001;
    public const int CDS_GLOBAL = 0x00000008;
    public const int DISP_CHANGE_SUCCESSFUL = 0;

    public static bool MoveDisplay(string deviceName, int newX, int newY) {
        DEVMODE dm = new DEVMODE();
        dm.dmSize = (short)Marshal.SizeOf(dm);

        if (EnumDisplaySettings(deviceName, ENUM_CURRENT_SETTINGS, ref dm) != 0) {
            dm.dmPositionX = newX;
            dm.dmPositionY = newY;
            dm.dmFields |= DM_POSITION;

            int result = ChangeDisplaySettingsEx(deviceName, ref dm, IntPtr.Zero, CDS_UPDATEREGISTRY | CDS_GLOBAL, IntPtr.Zero);
            return result == DISP_CHANGE_SUCCESSFUL;
        }
        return false;
    }
}
"@

Write-Host "Reorganizando pantallas: Colocando ASUS (DISPLAY2) a la IZQUIERDA del monitor principal..." -ForegroundColor Cyan

Add-Type -AssemblyName System.Windows.Forms
$screens = [System.Windows.Forms.Screen]::AllScreens
$secondary = $screens | Where-Object { -not $_.Primary } | Select-Object -First 1

if ($secondary) {
    $secWidth = $secondary.Bounds.Width
    $newX = -$secWidth
    Write-Host "Moviendo $($secondary.DeviceName) a posición X = $newX, Y = 0" -ForegroundColor Yellow
    $res = [DisplayManager]::MoveDisplay($secondary.DeviceName, $newX, 0)
    if ($res) {
        Write-Host "✅ Pantalla reubicada exitosamente a la izquierda." -ForegroundColor Green
    } else {
        Write-Host "⚠️ Intento de actualización completado. Verificando estado..." -ForegroundColor Yellow
    }
} else {
    Write-Host "No se detectó pantalla secundaria activa." -ForegroundColor Red
}

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class MultiDisplayManager {
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

    [DllImport("user32.dll", CharSet = CharSet.Ansi, EntryPoint = "ChangeDisplaySettingsEx")]
    public static extern int ChangeDisplaySettingsExNull(IntPtr lpszDeviceName, IntPtr lpDevMode, IntPtr hwnd, uint dwflags, IntPtr lParam);

    public const int ENUM_CURRENT_SETTINGS = -1;
    public const int DM_POSITION = 0x00000020;
    public const int CDS_UPDATEREGISTRY = 0x00000001;
    public const int CDS_GLOBAL = 0x00000008;
    public const int DISP_CHANGE_SUCCESSFUL = 0;

    public static bool SetDisplayPosition(string deviceName, int newX, int newY) {
        DEVMODE dm = new DEVMODE();
        dm.dmSize = (short)Marshal.SizeOf(dm);

        if (EnumDisplaySettings(deviceName, ENUM_CURRENT_SETTINGS, ref dm) != 0) {
            dm.dmPositionX = newX;
            dm.dmPositionY = newY;
            dm.dmFields |= DM_POSITION;

            int result = ChangeDisplaySettingsEx(deviceName, ref dm, IntPtr.Zero, CDS_UPDATEREGISTRY | CDS_GLOBAL, IntPtr.Zero);
            return (result == DISP_CHANGE_SUCCESSFUL);
        }
        return false;
    }

    public static void ApplyChanges() {
        ChangeDisplaySettingsExNull(IntPtr.Zero, IntPtr.Zero, IntPtr.Zero, 0, IntPtr.Zero);
    }
}
"@

Add-Type -AssemblyName System.Windows.Forms

Write-Host "Configurando disposición de 3 monitores:" -ForegroundColor Cyan
Write-Host "  <- [ASUS MB16AC] (Izquierda: X = -1280)" -ForegroundColor Green
Write-Host "  -- [LAPTOP LENOVO] (Centro / Principal: X = 0)" -ForegroundColor Yellow
Write-Host "  -> [ACER T232HL] (Derecha: X = 1536)" -ForegroundColor Green

# Obtener los nombres de dispositivos actuales
$screens = [System.Windows.Forms.Screen]::AllScreens
$laptopScreen = $screens | Where-Object { $_.Primary } | Select-Object -First 1
$nonPrimary = $screens | Where-Object { -not $_.Primary }

# Acer suele ser 1920x1080 (o mayor), ASUS es 1280x720
$asusScreen = $nonPrimary | Where-Object { $_.Bounds.Width -le 1366 } | Select-Object -First 1
$acerScreen = $nonPrimary | Where-Object { $_.Bounds.Width -ge 1600 } | Select-Object -First 1

if ($asusScreen) {
    $res = [MultiDisplayManager]::SetDisplayPosition($asusScreen.DeviceName, -1280, 0)
    Write-Host "Posicionando ASUS ($($asusScreen.DeviceName)) a la IZQUIERDA (X = -1280): $res" -ForegroundColor Green
}

if ($laptopScreen) {
    $res = [MultiDisplayManager]::SetDisplayPosition($laptopScreen.DeviceName, 0, 0)
    Write-Host "Posicionando Laptop ($($laptopScreen.DeviceName)) al CENTRO (X = 0): $res" -ForegroundColor Yellow
}

if ($acerScreen) {
    $res = [MultiDisplayManager]::SetDisplayPosition($acerScreen.DeviceName, 1536, 0)
    Write-Host "Posicionando Acer ($($acerScreen.DeviceName)) a la DERECHA (X = 1536): $res" -ForegroundColor Green
}

[MultiDisplayManager]::ApplyChanges()

Write-Host "`n✅ Disposición de 3 pantallas aplicada exitosamente." -ForegroundColor Green

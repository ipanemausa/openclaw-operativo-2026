Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class WinDisplayManager {
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
    public static extern int ChangeDisplaySettingsExReset(IntPtr lpszDeviceName, IntPtr lpDevMode, IntPtr hwnd, uint dwflags, IntPtr lParam);

    public const int ENUM_CURRENT_SETTINGS = -1;
    public const int DM_POSITION = 0x00000020;
    public const uint CDS_UPDATEREGISTRY = 0x00000001;
    public const uint CDS_NORESET = 0x10000000;
    public const uint CDS_GLOBAL = 0x00000008;

    public static int SetPosition(string deviceName, int x, int y) {
        DEVMODE dm = new DEVMODE();
        dm.dmSize = (short)Marshal.SizeOf(dm);
        if (EnumDisplaySettings(deviceName, ENUM_CURRENT_SETTINGS, ref dm) != 0) {
            dm.dmPositionX = x;
            dm.dmPositionY = y;
            dm.dmFields |= DM_POSITION;
            int ret = ChangeDisplaySettingsEx(deviceName, ref dm, IntPtr.Zero, CDS_UPDATEREGISTRY | CDS_NORESET, IntPtr.Zero);
            return ret;
        }
        return -99;
    }

    public static int Commit() {
        return ChangeDisplaySettingsExReset(IntPtr.Zero, IntPtr.Zero, IntPtr.Zero, 0, IntPtr.Zero);
    }
}
"@

Write-Host "Reordenando pantallas vía PowerShell Win32 API..." -ForegroundColor Cyan

# DISPLAY3 (ASUS MB16AC) -> IZQUIERDA (X = -1920)
$r1 = [WinDisplayManager]::SetPosition("\\.\DISPLAY3", -1920, 0)
Write-Host "1. ASUS (DISPLAY3) posicionada a la IZQUIERDA (X = -1920): RetCode $r1" -ForegroundColor Green

# DISPLAY1 (Laptop) -> CENTRO (X = 0)
$r2 = [WinDisplayManager]::SetPosition("\\.\DISPLAY1", 0, 0)
Write-Host "2. Laptop (DISPLAY1) posicionada en el CENTRO (X = 0): RetCode $r2" -ForegroundColor Yellow

# DISPLAY2 (Acer) -> DERECHA (X = 1920)
$r3 = [WinDisplayManager]::SetPosition("\\.\DISPLAY2", 1920, 0)
Write-Host "3. Acer (DISPLAY2) posicionada a la DERECHA (X = 1920): RetCode $r3" -ForegroundColor Green

# Aplicar los cambios en el sistema
$commit = [WinDisplayManager]::Commit()
Write-Host "Resultado del Commit de Windows: $commit (0 = ÉXITO)" -ForegroundColor Cyan

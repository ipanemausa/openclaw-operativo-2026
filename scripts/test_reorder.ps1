Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class WinDisplayManager2 {
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
    public const int DM_PELSWIDTH = 0x00080000;
    public const int DM_PELSHEIGHT = 0x00100000;
    public const uint CDS_UPDATEREGISTRY = 0x00000001;
    public const uint CDS_GLOBAL = 0x00000008;

    public static int ApplyPosition(string deviceName, int x, int y, int width, int height) {
        DEVMODE dm = new DEVMODE();
        dm.dmSize = (short)Marshal.SizeOf(dm);
        if (EnumDisplaySettings(deviceName, ENUM_CURRENT_SETTINGS, ref dm) != 0) {
            dm.dmPositionX = x;
            dm.dmPositionY = y;
            dm.dmPelsWidth = width;
            dm.dmPelsHeight = height;
            dm.dmFields = DM_POSITION | DM_PELSWIDTH | DM_PELSHEIGHT;
            int ret = ChangeDisplaySettingsEx(deviceName, ref dm, IntPtr.Zero, CDS_UPDATEREGISTRY | CDS_GLOBAL, IntPtr.Zero);
            return ret;
        }
        return -99;
    }
}
"@

# Posicionar ASUS MB16AC (DISPLAY3) a la IZQUIERDA: X = -1920
$res1 = [WinDisplayManager2]::ApplyPosition("\\.\DISPLAY3", -1920, 0, 1920, 1080)
Write-Host "ASUS (Izquierda X=-1920): RetCode $res1"

# Posicionar Laptop (DISPLAY1) al CENTRO: X = 0
$res2 = [WinDisplayManager2]::ApplyPosition("\\.\DISPLAY1", 0, 0, 1920, 1080)
Write-Host "Laptop (Centro X=0): RetCode $res2"

# Posicionar Acer (DISPLAY2) a la DERECHA: X = 1920
$res3 = [WinDisplayManager2]::ApplyPosition("\\.\DISPLAY2", 1920, 0, 1920, 1080)
Write-Host "Acer (Derecha X=1920): RetCode $res3"

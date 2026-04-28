"""
Direct screenshot using Windows API via ctypes
"""
import ctypes
import os
from ctypes import wintypes

# Constants
SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0
BI_RGB = 0

# Structures
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3)
    ]

# Get DCs
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)
print(f"Screen: {screen_w} x {screen_h}")

# Get screen DC
hdcScreen = user32.GetDC(0)
# Create compatible DC and bitmap
hdcMem = gdi32.CreateCompatibleDC(hdcScreen)
hBitmap = gdi32.CreateCompatibleBitmap(hdcScreen, screen_w, screen_h)
gdi32.SelectObject(hdcMem, hBitmap)

# BitBlt
gdi32.BitBlt(hdcMem, 0, 0, screen_w, screen_h, hdcScreen, 0, 0, SRCCOPY)

# Create bitmap info
bmi = BITMAPINFO()
bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
bmi.bmiHeader.biWidth = screen_w
bmi.bmiHeader.biHeight = -screen_h  # Top-down
bmi.bmiHeader.biPlanes = 1
bmi.bmiHeader.biBitCount = 32
bmi.bmiHeader.biCompression = BI_RGB

# Allocate buffer
buffer_size = screen_w * screen_h * 4
buffer = ctypes.create_string_buffer(buffer_size)

# Get bitmap bits
gdi32.GetDIBits(hdcMem, hBitmap, 0, screen_h, buffer, ctypes.byref(bmi), DIB_RGB_COLORS)

# Save as PNG using Pillow
from PIL import Image
img = Image.frombuffer('RGBA', (screen_w, screen_h), buffer, 'raw', 'BGRA', 0, 1)

output_path = r"D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428.png"
img.save(output_path, 'PNG')
print(f"Saved: {output_path}")

# Cleanup
user32.ReleaseDC(0, hdcScreen)
gdi32.DeleteDC(hdcMem)
gdi32.DeleteObject(hBitmap)

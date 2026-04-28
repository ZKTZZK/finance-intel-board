"""
截图脚本 - 使用PIL/Pillow
"""
import ctypes
from PIL import Image
import os

# Windows API
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# 获取屏幕尺寸
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

print(f"屏幕尺寸: {screen_width} x {screen_height}")

# 创建位图
dib = ctypes.create_string_buffer(screen_width * screen_height * 4)
handle = gdi32.CreateCompatibleDC(0)
handlebmp = gdi32.CreateCompatibleBitmap(handle, screen_width, screen_height)
gdi32.SelectObject(handle, handlebmp)

# 复制屏幕
gdi32.BitBlt(handle, 0, 0, screen_width, screen_height, 0, 0, 0, 0x00CC0020)

# 保存
img = Image.frombuffer('RGBA', (screen_width, screen_height), dib, 'raw', 'BGRA', 0, 1)

output_path = r"D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428.png"
img.save(output_path)
print(f"截图已保存: {output_path}")

# 清理
gdi32.DeleteObject(handlebmp)
gdi32.DeleteDC(handle)

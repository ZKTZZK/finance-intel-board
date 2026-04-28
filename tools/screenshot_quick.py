"""
一键生成长图 - 使用系统浏览器截图
打开HTML → 全屏截图 → 保存
"""
import os
import subprocess
import time
from pathlib import Path
from PIL import Image
import sys

def screenshot_snappy():
    """截图「一图看懂」板块"""
    
    # 路径设置
    base_dir = Path(__file__).parent.parent
    html_file = base_dir / 'assets' / 'images' / 'snappy_20260428.html'
    output_file = base_dir / 'assets' / 'images' / 'snappy_20260428.png'
    
    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 打开浏览器
    html_path = str(html_file.absolute())
    print(f"📂 打开: {html_path}")
    
    # 使用Edge打开（最大化窗口）
    subprocess.Popen(['msedge', '--new-window', '--start-maximized', html_path])
    
    print("⏳ 等待页面加载...")
    time.sleep(3)  # 等待页面加载
    
    # 使用PowerShell截图
    print("📸 截图...")
    
    ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 获取屏幕尺寸
$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bounds = $screen.Bounds

# 创建截图
$bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)

# 保存
$output = "{output}"
$bitmap.Save($output, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()

Write-Host "截图已保存: $output"
'''.format(output=str(output_file).replace('\\', '\\\\'))
    
    # 执行PowerShell截图
    result = subprocess.run(
        ['powershell', '-Command', ps_script],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ 截图成功!")
        print(f"📁 {output_file}")
        
        # 裁剪为540px宽度（手机视图）
        try:
            img = Image.open(output_file)
            # 裁剪：保留顶部约2200px高度
            cropped = img.crop((0, 0, 540 * 2, 2200 * 2))  # 2x分辨率
            cropped.save(output_file, optimize=True)
            img.close()
            cropped.close()
            print(f"✂️ 已裁剪为540px宽度")
        except Exception as e:
            print(f"⚠️ 裁剪失败: {e}")
        
        return True
    else:
        print(f"❌ 截图失败: {result.stderr}")
        return False

if __name__ == '__main__':
    screenshot_snappy()
    input("\n按回车退出...")

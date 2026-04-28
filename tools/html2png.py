"""
HTML长图生成工具
使用Edge headless模式从HTML文件生成PNG截图

使用方法:
1. 直接运行: python html2png.py
2. 或双击运行: html2png.cmd
"""
import subprocess
import os
from PIL import Image
from datetime import datetime

# 配置
HTML_PATH = r"D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428.html"
OUTPUT_PATH = r"D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
VIEWPORT_WIDTH = 560  # 比目标宽20px，滚动条+缓冲区域
FINAL_WIDTH = 540     # 最终输出宽度
VIEWPORT_HEIGHT = 2000
PAGE_WAIT_MS = 8000  # 等待页面渲染的时间
TARGET_HEIGHT = 1850  # 最终裁剪高度

def html_to_png(html_path, output_dir, viewport_w=550, final_w=540, viewport_h=2000, wait_ms=8000, crop_h=1850):
    """将HTML文件转换为PNG长图（无损）"""
    
    # 生成输出文件名
    date_str = datetime.now().strftime("%Y%m%d")
    base_name = os.path.splitext(os.path.basename(html_path))[0]
    temp_file = os.path.join(output_dir, f"{base_name}_temp.png")
    final_file = os.path.join(output_dir, f"{base_name}_final.png")
    
    # 转换为file:// URL
    html_abs = os.path.abspath(html_path).replace('\\', '/')
    html_url = f"file:///{html_abs}"
    
    # 构建Edge命令行
    cmd = [
        EDGE_PATH,
        "--headless=new",
        f"--screenshot={temp_file}",
        f"--window-size={viewport_w},{viewport_h}",
        f"--virtual-time-budget={wait_ms}",
        "--disable-gpu",
        "--no-sandbox",
        html_url
    ]
    
    print(f"正在生成截图: {html_url}")
    print(f"输出: {temp_file}")
    
    # 执行截图
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"截图失败: {result.stderr}")
        return None
    
    # 检查临时文件
    if not os.path.exists(temp_file):
        print("截图文件未生成")
        return None
    
    # 裁剪为合适高度
    img = Image.open(temp_file)
    print(f"原始尺寸: {img.size[0]}x{img.size[1]}")
    
    # 裁剪（去掉右侧滚动条区域）
    cropped = img.crop((0, 0, final_w, min(img.size[1], crop_h)))
    cropped.save(final_file, 'PNG')
    print(f"最终尺寸: {cropped.size[0]}x{cropped.size[1]}（已裁剪右侧{right_crop}px）")
    print(f"保存至: {final_file}")
    
    # 删除临时文件
    os.remove(temp_file)
    
    img.close()
    cropped.close()
    
    return final_file

if __name__ == "__main__":
    result = html_to_png(HTML_PATH, OUTPUT_PATH, crop_h=TARGET_HEIGHT)
    if result:
        print(f"\n✅ 长图生成成功!")
    else:
        print(f"\n❌ 长图生成失败")

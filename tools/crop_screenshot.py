"""
裁剪截图 - 提取浏览器窗口区域
"""
from PIL import Image

# 打开截图
input_path = r"D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428.png"
output_path = r"D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428_final.png"

img = Image.open(input_path)
w, h = img.size
print(f"原始尺寸: {w} x {h}")

# 假设浏览器窗口在屏幕中心位置
# 提取中心区域 - 540px手机宽度，2x缩放
target_width = 540 * 2  # 1080px
target_height = int(target_width * 2.5)  # 约2700px高

# 计算裁剪区域（居中）
left = max(0, (w - target_width) // 2)
top = max(0, (h - target_height) // 2)

# 裁剪
cropped = img.crop((
    left,
    top,
    left + target_width,
    top + target_height
))

# 保存
cropped.save(output_path, 'PNG', optimize=True)
print(f"裁剪后尺寸: {cropped.size}")
print(f"已保存: {output_path}")

# 关闭
cropped.close()
img.close()

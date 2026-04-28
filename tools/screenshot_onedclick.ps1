"""
📸 一键截图 - 使用Windows系统API，无需安装任何包
"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# 截图保存路径
$outputPath = "D:\WorkBuddy_WorkSpace\Finance_IntelBoard\assets\images\snappy_20260428.png"

Write-Host "📸 正在截图..."
Write-Host ""

# 获取屏幕
$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bounds = $screen.Bounds

# 创建截图
$bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)

# 保存
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "✅ 截图已保存: $outputPath"
Write-Host ""
Write-Host "📌 提示：请在截图软件中打开此图片"
Write-Host "   然后裁剪为540px宽度即可"

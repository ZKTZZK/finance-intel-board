Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
s = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
b = New-Object System.Drawing.Bitmap(s.Width, s.Height)
[System.Drawing.Graphics]::FromImage(b).CopyFromScreen(s.Location, [System.Drawing.Point]::Empty, s.Size)
b.Save('D:\\WorkBuddy_WorkSpace\\Finance_IntelBoard\\assets\\images\\snappy_20260428.png')
b.Dispose()
Write-Host Done

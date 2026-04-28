"""
Finance Intel Board Screenshot Tool
将 daily_board.html 的「一图看懂」板块生成为长图
"""
import os
import asyncio
from pathlib import Path

# 尝试导入playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not available, trying alternative...")

def screenshot_snappy_board(html_path, output_path):
    """截取「一图看懂」板块生成长图"""
    
    if not PLAYWRIGHT_AVAILABLE:
        print("ERROR: Playwright is required for HTML screenshot")
        return False
    
    html_path = Path(html_path).resolve()
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 540, 'height': 1920},  # 手机视图
            device_scale_factor=2  # 高清
        )
        page = context.new_page()
        
        # 加载HTML文件
        page.goto(f'file:///{html_path.as_posix()}')
        page.wait_for_load_state('networkidle')
        
        # 点击「一图看懂」Tab（如果不在当前视图）
        try:
            page.click('#sec-snap')
        except:
            pass
        
        # 等待内容加载
        page.wait_for_timeout(1000)
        
        # 截取整个页面
        page.screenshot(
            path=output_path,
            full_page=True,
            type='png'
        )
        
        browser.close()
        print(f"✅ Screenshot saved: {output_path}")
        return True

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    html_file = base_dir / 'daily_board.html'
    output_file = base_dir / 'assets' / 'images' / 'snappy_20260428.png'
    
    # 确保输出目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if screenshot_snappy_board(html_file, output_file):
        print(f"\n📱 长图已生成: {output_file}")
    else:
        print("\n❌ 截图失败")

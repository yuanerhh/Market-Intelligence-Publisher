#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体检测和调试工具
用于检测系统中可用的中文字体
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont


def check_font_file(font_path, font_size=60):
    """检查单个字体文件是否可用"""
    try:
        font = ImageFont.truetype(font_path, font_size)
        return True, "可用"
    except Exception as e:
        return False, str(e)


def find_chinese_fonts():
    """查找系统中的中文字体"""
    print("="*60)
    print("字体检测工具 - 查找系统中的中文字体")
    print("="*60)
    print()
    
    # 常见字体路径
    font_paths = [
        # Windows
        ("Windows - 微软雅黑粗体", "C:/Windows/Fonts/msyhbd.ttc"),
        ("Windows - 微软雅黑", "C:/Windows/Fonts/msyh.ttc"),
        ("Windows - 黑体", "C:/Windows/Fonts/simhei.ttf"),
        ("Windows - 宋体", "C:/Windows/Fonts/simsun.ttc"),
        
        # Linux - 文泉驿
        ("Linux - 文泉驿正黑 (路径1)", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
        ("Linux - 文泉驿正黑 (路径2)", "/usr/share/fonts/wqy-zenhei/wqy-zenhei.ttc"),
        ("Linux - 文泉驿微米黑", "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
        
        # Linux - Droid
        ("Linux - Droid Fallback", "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"),
        
        # Linux - Noto
        ("Linux - Noto CJK (路径1)", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        ("Linux - Noto CJK (路径2)", "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc"),
        
        # Linux - AR PL
        ("Linux - AR PL UMing", "/usr/share/fonts/truetype/arphic/uming.ttc"),
        ("Linux - AR PL UKai", "/usr/share/fonts/truetype/arphic/ukai.ttc"),
        
        # macOS
        ("macOS - 苹方", "/System/Library/Fonts/PingFang.ttc"),
        ("macOS - 宋体", "/Library/Fonts/Songti.ttc"),
        ("macOS - 黑体", "/System/Library/Fonts/STHeiti Medium.ttc"),
    ]
    
    available_fonts = []
    unavailable_fonts = []
    
    print("检查预定义字体路径...")
    print()
    
    for name, path in font_paths:
        exists = os.path.exists(path)
        if exists:
            is_usable, message = check_font_file(path)
            if is_usable:
                print(f"✅ {name}")
                print(f"   路径: {path}")
                available_fonts.append((name, path))
            else:
                print(f"⚠️  {name} (文件存在但无法加载)")
                print(f"   路径: {path}")
                print(f"   错误: {message}")
                unavailable_fonts.append((name, path, message))
        else:
            unavailable_fonts.append((name, path, "文件不存在"))
    
    print()
    print("="*60)
    print(f"检测结果：找到 {len(available_fonts)} 个可用字体")
    print("="*60)
    
    if available_fonts:
        print()
        print("可用的字体：")
        for i, (name, path) in enumerate(available_fonts, 1):
            print(f"{i}. {name}")
            print(f"   {path}")
    else:
        print()
        print("❌ 未找到任何可用的中文字体！")
        print()
        print("建议安装字体：")
        print("  Ubuntu/Debian: sudo apt-get install fonts-wqy-zenhei")
        print("  CentOS/RHEL: sudo yum install wqy-zenhei-fonts")
    
    return available_fonts


def test_font_rendering(font_path):
    """测试字体渲染效果"""
    print()
    print("="*60)
    print("测试字体渲染效果")
    print("="*60)
    
    try:
        # 创建测试图片
        img = Image.new('RGB', (1280, 720), color=(13, 27, 62))
        draw = ImageDraw.Draw(img)
        
        # 加载字体
        title_font = ImageFont.truetype(font_path, 120)
        date_font = ImageFont.truetype(font_path, 50)
        
        # 绘制测试文字
        title_text = "行情晚报"
        date_text = "2026年02月13日"
        
        # 计算居中位置
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (1280 - title_width) // 2
        
        date_bbox = draw.textbbox((0, 0), date_text, font=date_font)
        date_width = date_bbox[2] - date_bbox[0]
        date_x = (1280 - date_width) // 2
        
        # 绘制文字
        gold_color = (218, 165, 32)
        draw.text((title_x, 250), title_text, font=title_font, fill=gold_color)
        draw.text((date_x, 420), date_text, font=date_font, fill=(255, 255, 255))
        
        # 保存测试图片
        test_file = 'font_test.jpg'
        img.save(test_file, 'JPEG', quality=95)
        
        print(f"✅ 测试成功！")
        print(f"   测试图片已保存: {test_file}")
        print(f"   请打开图片查看渲染效果")
        
        # 显示图片信息
        import os
        file_size = os.path.getsize(test_file)
        print(f"   文件大小: {file_size / 1024:.2f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    # 查找可用字体
    available_fonts = find_chinese_fonts()
    
    if not available_fonts:
        print()
        print("💡 调试提示：")
        print("   1. 运行命令查找系统字体: fc-list :lang=zh")
        print("   2. 查找字体文件: find /usr/share/fonts -name '*.ttf' -o -name '*.ttc'")
        print("   3. 检查字体是否安装: dpkg -l | grep font")
        sys.exit(1)
    
    # 测试第一个可用字体
    print()
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        name, path = available_fonts[0]
        print(f"使用字体进行渲染测试: {name}")
        print(f"字体路径: {path}")
        test_font_rendering(path)
    else:
        print("💡 提示：运行 'python3 font_checker.py --test' 可进行渲染测试")


if __name__ == "__main__":
    main()

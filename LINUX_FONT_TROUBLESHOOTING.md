# Linux字体问题排查指南

## 🐛 问题：文字特别小

### 症状描述
在Linux系统下生成的封面图片：
- ✅ 背景渐变正常
- ✅ 装饰元素正常（线条、圆形、箭头、太阳）
- ⚠️ 文字显示但**非常小**
- ⚠️ 文字位置在底部，而不是居中

### 根本原因
PIL库字体加载失败，回退到`ImageFont.load_default()`：
- 默认字体大小固定（约10-12px）
- 无法通过参数设置大小
- 文字会显示在意外的位置

### 为什么Windows正常？
Windows系统自带微软雅黑等中文字体，PIL可以成功加载。

---

## 🔍 诊断步骤

### 步骤1：运行字体检测工具

```bash
cd /path/to/Market-Intelligence-Publisher
python3 font_checker.py
```

**预期输出：**
```
===========================================================
字体检测工具 - 查找系统中的中文字体
============================================================

检查预定义字体路径...

✅ Linux - 文泉驿正黑 (路径1)
   路径: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc

============================================================
检测结果：找到 1 个可用字体
============================================================

可用的字体：
1. Linux - 文泉驿正黑 (路径1)
   /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
```

### 步骤2：检查脚本输出

运行脚本时查看输出：

```bash
python3 morning_report_publisher.py
```

**如果字体加载成功：**
```
正在生成封面图片...
✓ 成功加载字体: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
✓ 封面图片生成成功: morning_cover_1234567890.jpg
```

**如果字体加载失败：**
```
正在生成封面图片...
⚠ 警告：未找到中文字体，使用默认字体（可能无法显示中文）
✗ 最后错误: cannot open resource
💡 建议：在Linux上安装中文字体
   Ubuntu/Debian: sudo apt-get install fonts-wqy-zenhei
   CentOS/RHEL: sudo yum install wqy-zenhei-fonts
```

---

## ✅ 解决方案

### 方案1：安装文泉驿字体（推荐）

#### Ubuntu / Debian
```bash
sudo apt-get update
sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei
fc-cache -fv
```

#### CentOS / RHEL
```bash
sudo yum install wqy-zenhei-fonts
fc-cache -fv
```

### 方案2：验证字体安装

```bash
# 检查字体是否安装
fc-list :lang=zh

# 应该看到类似输出
# /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc: WenQuanYi Zen Hei:style=Regular
```

### 方案3：检查字体文件权限

```bash
# 查看字体文件
ls -lh /usr/share/fonts/truetype/wqy/

# 应该是可读的
# -rw-r--r-- 1 root root 4.5M ... wqy-zenhei.ttc

# 如果权限不对，修复
sudo chmod 644 /usr/share/fonts/truetype/wqy/*.ttc
```

### 方案4：手动测试字体

使用我们的测试工具：

```bash
python3 font_checker.py --test
```

这会生成 `font_test.jpg`，打开查看效果：
- ✅ 文字大而清晰 → 字体正常
- ❌ 文字小而模糊 → 字体加载失败

---

## 🔧 高级排查

### 问题1：字体已安装但仍加载失败

**可能原因：字体路径不匹配**

查找实际字体路径：
```bash
find /usr/share/fonts -name '*wqy*' -o -name '*zenhei*'
```

输出示例：
```
/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
```

如果路径不同，修改脚本中的字体路径列表。

### 问题2：字体文件损坏

重新安装字体：
```bash
# Ubuntu/Debian
sudo apt-get remove fonts-wqy-zenhei
sudo apt-get install fonts-wqy-zenhei

# 清除字体缓存并重建
sudo fc-cache -fv
```

### 问题3：PIL版本问题

检查Pillow版本：
```bash
python3 -c "from PIL import Image; print(Image.__version__)"
```

如果版本太旧，升级：
```bash
pip3 install --upgrade Pillow
```

推荐版本：Pillow >= 8.0.0

### 问题4：字体索引问题

某些.ttc文件包含多个字体，需要指定索引：

```python
# 修改脚本，尝试指定字体索引
font = ImageFont.truetype(font_path, 120, index=0)
```

---

## 📊 对比测试

### 正确的效果
- 标题："行情早报"/"行情晚报" - 大字体（120px），居中
- 日期："2026年02月13日" - 中等字体（50px），居中偏下
- 位置：文字在图片中央区域

### 错误的效果（使用默认字体）
- 标题：很小的文字，约10-12px
- 日期：同样很小
- 位置：文字在图片底部

---

## 🛠️ 调试脚本

### 创建测试脚本

创建 `debug_font.py`：

```python
from PIL import Image, ImageDraw, ImageFont
import os

print("="*60)
print("字体加载调试")
print("="*60)

# 测试字体路径
font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

print(f"\n检查字体文件:")
print(f"路径: {font_path}")
print(f"存在: {os.path.exists(font_path)}")

if os.path.exists(font_path):
    print(f"大小: {os.path.getsize(font_path) / 1024 / 1024:.2f} MB")
    print(f"权限: {oct(os.stat(font_path).st_mode)[-3:]}")

print(f"\n尝试加载字体:")
try:
    font = ImageFont.truetype(font_path, 120)
    print("✅ 字体加载成功！")
    
    # 测试渲染
    img = Image.new('RGB', (800, 400), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((50, 150), "行情早报", font=font, fill='black')
    img.save('debug_test.jpg')
    print("✅ 测试图片已保存: debug_test.jpg")
    
except Exception as e:
    print(f"❌ 字体加载失败: {e}")
    print(f"错误类型: {type(e).__name__}")
```

运行：
```bash
python3 debug_font.py
```

---

## 💡 最佳实践

### 1. 安装多个字体作为备选

```bash
# 安装多个中文字体
sudo apt-get install \
  fonts-wqy-zenhei \
  fonts-wqy-microhei \
  fonts-noto-cjk
```

### 2. 验证安装

```bash
# 安装后验证
fc-list :lang=zh | wc -l

# 应该显示数字 > 0
```

### 3. 测试渲染

```bash
# 每次安装新字体后测试
python3 font_checker.py --test
```

### 4. 查看脚本输出

运行脚本时注意查看"成功加载字体"的提示。

---

## 📋 快速解决方案

### 一键修复脚本

创建 `fix_font.sh`：

```bash
#!/bin/bash

echo "正在修复Linux字体问题..."

# 检测操作系统
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    echo "检测到 Debian/Ubuntu 系统"
    sudo apt-get update
    sudo apt-get install -y fonts-wqy-zenhei
elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL
    echo "检测到 CentOS/RHEL 系统"
    sudo yum install -y wqy-zenhei-fonts
else
    echo "未知系统，请手动安装字体"
    exit 1
fi

# 更新字体缓存
echo "更新字体缓存..."
fc-cache -fv

# 验证安装
echo ""
echo "验证字体安装..."
if fc-list :lang=zh | grep -q "WenQuanYi"; then
    echo "✅ 字体安装成功！"
    fc-list :lang=zh | grep "WenQuanYi"
else
    echo "❌ 字体安装失败"
    exit 1
fi

# 测试渲染
echo ""
echo "运行渲染测试..."
python3 font_checker.py --test

echo ""
echo "✅ 修复完成！请运行脚本测试："
echo "   python3 morning_report_publisher.py"
```

运行：
```bash
chmod +x fix_font.sh
./fix_font.sh
```

---

## ✅ 验证清单

修复后验证：

- [ ] `fc-list :lang=zh` 显示中文字体
- [ ] `python3 font_checker.py` 找到可用字体
- [ ] `python3 font_checker.py --test` 生成正常大小的文字
- [ ] 运行脚本时显示"成功加载字体"
- [ ] 生成的封面图片文字大而清晰
- [ ] 文字位置在图片中央

---

## 📞 仍然无法解决？

### 收集调试信息

运行以下命令并提供输出：

```bash
# 1. 系统信息
uname -a
cat /etc/os-release

# 2. Python和PIL版本
python3 --version
python3 -c "from PIL import Image; print(Image.__version__)"

# 3. 字体信息
fc-list :lang=zh
find /usr/share/fonts -name '*.ttf' -o -name '*.ttc' | head -20

# 4. 权限信息
ls -lh /usr/share/fonts/truetype/wqy/

# 5. 运行字体检测
python3 font_checker.py

# 6. 运行脚本并保存输出
python3 morning_report_publisher.py 2>&1 | tee debug.log
```

---

**最后更新**: 2026年02月13日  
**适用版本**: v1.1+

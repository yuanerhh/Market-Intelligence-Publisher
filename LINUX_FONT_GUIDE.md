# Linux 中文字体安装指南

## 问题说明

在Linux系统下运行脚本生成的封面图片**没有文字和日期**，这是因为PIL库找不到中文字体导致的。

Windows系统下正常，因为有微软雅黑等中文字体。

---

## 🔍 问题诊断

### 症状
- ✅ 封面背景正常
- ✅ 装饰元素正常（线条、圆形、箭头等）
- ❌ 文字不显示（"行情早报"/"行情晚报"）
- ❌ 日期不显示

### 原因
Linux系统默认没有安装中文字体，PIL库的`ImageFont.load_default()`只支持ASCII字符。

---

## 💡 解决方案

### 方案1：安装文泉驿字体（推荐）

#### Ubuntu / Debian
```bash
sudo apt-get update
sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei
```

#### CentOS / RHEL / Fedora
```bash
sudo yum install wqy-zenhei-fonts wqy-microhei-fonts
```

#### Arch Linux
```bash
sudo pacman -S wqy-zenhei wqy-microhei
```

---

### 方案2：安装Noto字体

#### Ubuntu / Debian
```bash
sudo apt-get install fonts-noto-cjk fonts-noto-cjk-extra
```

#### CentOS / RHEL
```bash
sudo yum install google-noto-sans-cjk-fonts
```

---

### 方案3：安装Droid字体

#### Ubuntu / Debian
```bash
sudo apt-get install fonts-droid-fallback
```

---

### 方案4：手动安装字体

#### 1. 下载字体文件

从Windows复制字体文件，或下载开源字体：
- 文泉驿正黑：https://sourceforge.net/projects/wqy/files/wqy-zenhei/
- Noto Sans CJK：https://github.com/googlefonts/noto-cjk/releases

#### 2. 创建字体目录
```bash
mkdir -p ~/.fonts
```

#### 3. 复制字体文件
```bash
# 复制.ttf或.ttc文件到字体目录
cp wqy-zenhei.ttc ~/.fonts/
```

#### 4. 更新字体缓存
```bash
fc-cache -fv
```

#### 5. 验证字体安装
```bash
fc-list :lang=zh
```

---

## ✅ 验证安装

### 方法1：运行脚本测试

```bash
cd /path/to/Market-Intelligence-Publisher
python3 morning_report_publisher.py
```

查看输出，应该显示：
```
✓ 成功加载字体: /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc
```

### 方法2：查看生成的图片

```bash
# 查看生成的封面图片
ls -lh morning_cover_*.jpg

# 使用图片查看器打开
xdg-open morning_cover_*.jpg
```

检查图片中是否显示：
- ✅ "行情早报" 或 "行情晚报"
- ✅ 日期（如"2026年02月13日"）

---

## 🔧 脚本已支持的字体路径

脚本会自动尝试以下字体路径（按顺序）：

### Windows
1. `C:/Windows/Fonts/msyhbd.ttc` - 微软雅黑粗体
2. `C:/Windows/Fonts/msyh.ttc` - 微软雅黑
3. `C:/Windows/Fonts/simhei.ttf` - 黑体

### Linux
1. `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` - 文泉驿正黑
2. `/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf` - Droid字体
3. `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc` - Noto字体

### macOS
1. `/System/Library/Fonts/PingFang.ttc` - 苹方
2. `/Library/Fonts/Songti.ttc` - 宋体

---

## 📊 推荐字体对比

| 字体 | 大小 | 优点 | 缺点 |
|------|------|------|------|
| **文泉驿正黑** | ~10MB | 开源免费、显示效果好 | 稍大 |
| **Noto Sans CJK** | ~100MB | Google出品、全面 | 很大 |
| **Droid Fallback** | ~3MB | 小巧 | 字形一般 |

**推荐**：文泉驿正黑（wqy-zenhei）

---

## 🐳 Docker环境

如果在Docker中运行，需要在Dockerfile中添加：

```dockerfile
# Ubuntu/Debian基础镜像
RUN apt-get update && \
    apt-get install -y fonts-wqy-zenhei && \
    rm -rf /var/lib/apt/lists/*

# CentOS/RHEL基础镜像
RUN yum install -y wqy-zenhei-fonts && \
    yum clean all
```

---

## 🔍 故障排查

### 问题1：安装后仍无法显示

**检查字体是否安装成功：**
```bash
fc-list :lang=zh | grep -i wqy
```

应该看到类似输出：
```
/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc: WenQuanYi Zen Hei:style=Regular
```

**更新字体缓存：**
```bash
sudo fc-cache -fv
```

### 问题2：权限问题

**确保字体文件可读：**
```bash
sudo chmod 644 /usr/share/fonts/truetype/wqy/*.ttc
```

### 问题3：路径不匹配

**查找实际字体路径：**
```bash
find /usr -name "*wqy*" -type f 2>/dev/null
```

**修改脚本中的字体路径：**
编辑 `morning_report_publisher.py` 和 `market_report_publisher.py`，在字体路径列表中添加实际路径。

---

## 📝 完整测试脚本

创建测试脚本 `test_font.py`：

```python
from PIL import Image, ImageDraw, ImageFont

# 创建测试图片
img = Image.new('RGB', (800, 400), color='white')
draw = ImageDraw.Draw(img)

# 尝试加载字体
font_paths = [
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

font = None
for path in font_paths:
    try:
        font = ImageFont.truetype(path, 60)
        print(f"✓ 成功加载字体: {path}")
        break
    except Exception as e:
        print(f"✗ 加载失败: {path} - {e}")

if font is None:
    print("⚠ 使用默认字体")
    font = ImageFont.load_default()

# 绘制测试文字
draw.text((50, 150), "行情早报", font=font, fill='black')
draw.text((50, 250), "2026年02月13日", font=font, fill='black')

# 保存测试图片
img.save('test_font.jpg')
print("✓ 测试图片已保存: test_font.jpg")
```

运行测试：
```bash
python3 test_font.py
xdg-open test_font.jpg
```

---

## 🚀 快速修复（推荐）

### Ubuntu/Debian一键安装
```bash
sudo apt-get update && sudo apt-get install -y fonts-wqy-zenhei && fc-cache -fv
```

### CentOS/RHEL一键安装
```bash
sudo yum install -y wqy-zenhei-fonts && fc-cache -fv
```

### 验证
```bash
cd /path/to/Market-Intelligence-Publisher
python3 morning_report_publisher.py
```

---

## 📚 相关资源

- **文泉驿项目**: http://wenq.org/
- **Noto字体**: https://www.google.com/get/noto/
- **PIL文档**: https://pillow.readthedocs.io/
- **Linux字体配置**: https://wiki.archlinux.org/title/Fonts

---

## ✅ 检查清单

安装字体后，确认：

- [ ] 字体包已安装
- [ ] 字体缓存已更新（`fc-cache -fv`）
- [ ] 字体可被系统识别（`fc-list :lang=zh`）
- [ ] 脚本运行时显示"成功加载字体"
- [ ] 生成的图片包含中文文字
- [ ] 生成的图片包含日期

---

**最后更新**: 2026年02月13日  
**适用版本**: Market Intelligence Publisher v1.0+

---
name: financial-report-publisher
description: 自动生成并发布金融行情简报到微信公众号。当用户需要：(1) 生成A股、美股、期货收盘行情简报，(2) 自动发布金融市场数据到微信公众号草稿箱，(3) 创建带有专业封面的金融晚报，(4) 定期发布市场行情汇总时使用此技能。支持自动获取行情数据、AI生成封面图片、格式化HTML内容、微信公众号API集成。
---

# Financial Report Publisher

自动化金融行情简报生成与发布系统。

## 功能概述

本技能提供完整的金融行情简报自动化工作流：

1. **数据获取** - 自动获取A股、美股、期货市场收盘数据
2. **封面生成** - 使用PIL库生成专业金融风格封面图片
3. **内容生成** - 格式化HTML格式的行情简报
4. **自动发布** - 通过微信公众号API发布到草稿箱

## 快速开始

### 前置要求

1. 微信公众号（已认证的服务号或订阅号）
2. 阿里云账号（可选，用于AI生成封面）
3. Python 3.7+ 环境

### 配置文件

在工作目录创建 `config.json`：

```json
{
  "wechat": {
    "appid": "YOUR_WECHAT_APPID",
    "secret": "YOUR_WECHAT_SECRET"
  },
  "aliyun": {
    "api_key": "YOUR_ALIYUN_API_KEY"
  }
}
```

**获取微信公众号凭证：**
- 登录 https://mp.weixin.qq.com
- 进入"开发" → "基本配置"
- 复制 AppID 和 AppSecret

**获取阿里云API Key（可选）：**
- 登录阿里云百炼平台 https://bailian.console.aliyun.com
- 进入"API-KEY管理"
- 创建并复制API Key

### 执行发布

运行主脚本：

```bash
python scripts/market_report_publisher.py
```

或使用配置文件路径：

```bash
python scripts/market_report_publisher.py /path/to/config.json
```

## 工作流程

### 步骤1：获取Access Token

自动调用微信API获取access_token，用于后续操作。

### 步骤2：生成封面图片

使用PIL库本地生成封面，包含：
- 深蓝到金色渐变背景
- "行情晚报"金色大标题
- 当前日期（白色）
- 金色装饰元素
- 绿色上涨箭头

**技术细节：**
- 图片尺寸：1280x720 (16:9)
- 字体：优先使用微软雅黑粗体，回退到黑体
- 输出格式：JPEG，质量95%

### 步骤3：上传封面

将生成的封面图片上传到微信公众号素材库，获取media_id。

### 步骤4：生成简报内容

自动生成HTML格式的行情简报，包含：

**A股市场：**
- 上证指数、深证成指、创业板指
- 成交额数据
- 领涨/领跌板块（前4名）
- 主力资金流向

**美股市场：**
- 道琼斯指数
- 标普500指数
- 纳斯达克指数

**商品期货：**
- 贵金属（黄金、白银）
- 能源（原油）
- 工业金属（铜、螺纹钢）

### 步骤5：创建草稿

调用微信公众号草稿API，创建包含封面和内容的草稿。

## 数据来源

简报数据需要手动更新或通过API获取。当前脚本包含示例数据结构，可以：

1. **手动更新** - 修改 `generate_market_report()` 方法中的数据
2. **API集成** - 集成金融数据API（如东方财富、新浪财经等）
3. **网络爬取** - 使用爬虫获取公开数据

详细的数据获取方案参见 [references/data-sources.md](references/data-sources.md)

## 常见问题

### Q1: 文章内容显示乱码
**A:** 确保使用UTF-8编码发送请求。脚本已配置 `ensure_ascii=False` 和正确的Content-Type头。

### Q2: 封面图片文字不清晰
**A:** 检查系统是否安装了中文字体（微软雅黑或黑体）。脚本会自动回退到可用字体。

### Q3: access_token获取失败
**A:** 检查config.json中的appid和secret是否正确，确保公众号已认证。

### Q4: 草稿创建失败（errcode 45003）
**A:** 标题超过64字符限制。脚本已优化标题长度。

### Q5: 草稿创建失败（errcode 45110）
**A:** 作者名称超过限制。脚本已设置为"小跃"。

## 定时任务

### Windows任务计划程序

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器（如每天15:30）
4. 操作选择"启动程序"
5. 程序：`python.exe`
6. 参数：`E:\jieyue_data\financial-report-publisher\scripts\market_report_publisher.py`

### Linux Cron

```bash
# 每天15:30执行
30 15 * * * /usr/bin/python3 /path/to/scripts/market_report_publisher.py
```

## 扩展功能

### 添加新数据源

在 `generate_market_report()` 方法中添加新的数据板块：

```python
# 添加港股数据
<h3>🇭🇰 港股市场</h3>
<ul>
<li>恒生指数：{hsi_value}点，{hsi_change}%</li>
</ul>
```

### 自定义封面样式

修改 `generate_cover_image()` 方法中的：
- 背景颜色渐变
- 字体大小和颜色
- 装饰元素位置

### 多公众号发布

复制配置文件，为每个公众号创建独立配置：

```python
publisher1 = MarketReportPublisher('config_account1.json')
publisher2 = MarketReportPublisher('config_account2.json')
```

## 技术栈

- **Python 3.7+**
- **requests** - HTTP请求
- **Pillow (PIL)** - 图像生成
- **微信公众号API** - 草稿发布
- **阿里云通义万相** - AI图像生成（可选）

## 文件结构

```
financial-report-publisher/
├── SKILL.md                          # 本文件
├── scripts/
│   └── market_report_publisher.py    # 主程序
├── references/
│   ├── data-sources.md               # 数据源集成指南
│   └── wechat-api.md                 # 微信API参考
└── config.json.example               # 配置文件示例
```

## 许可与免责

本技能仅供学习交流使用。市场数据仅供参考，投资需谨慎。使用前请确保：

1. 遵守微信公众平台运营规范
2. 遵守金融信息发布相关法规
3. 数据来源合法合规
4. 不构成投资建议

## 更新日志

**v1.0** (2026-02-13)
- 初始版本发布
- 支持A股、美股、期货数据
- PIL本地生成封面
- 微信公众号草稿发布
- UTF-8编码修复

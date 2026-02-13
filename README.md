# Market Intelligence Publisher

金融行情智能发布系统 - 自动化早报+晚报发布到微信公众号

---

## 📁 目录结构

```
Market-Intelligence-Publisher/
├── 📄 核心脚本
│   ├── morning_report_publisher.py      # 早报主程序（7:00执行）
│   ├── market_report_publisher.py       # 晚报主程序（15:30执行）
│   └── config.json                      # 配置文件（微信+阿里云）
│
├── 🎨 封面图片
│   ├── morning_cover_*.jpg              # 早报封面（橙黄渐变+太阳）
│   └── cover_*.jpg                      # 晚报封面（深蓝金色+箭头）
│
├── ⚙️ 定时任务
│   ├── 一键配置定时任务.ps1             # PowerShell一键配置脚本
│   ├── 定时任务完整配置指南.md          # 详细配置文档
│   ├── run_report.bat                   # 简易运行脚本
│   ├── 启动程序.bat                     # 启动脚本
│   └── 运行行情简报发布.bat             # 晚报运行脚本
│
├── 📦 技能包
│   ├── financial-report-publisher/      # 晚报技能包目录
│   │   ├── SKILL.md                     # 技能说明
│   │   ├── scripts/
│   │   │   └── market_report_publisher.py
│   │   └── references/
│   │       ├── data-sources.md          # 数据源集成指南
│   │       └── wechat-api.md            # 微信API参考
│   ├── financial-report-publisher.skill # 打包的技能文件
│   └── package_skill.py                 # 技能打包脚本
│
├── 📚 文档
│   ├── 早报晚报系统说明.md              # 系统总览文档
│   ├── INSTALLATION_GUIDE.md            # 安装使用指南
│   └── README.md                        # 本文件
│
├── 🗂️ 历史文件
│   ├── 2026年2月13日_A股美股期货收盘行情简报.md
│   ├── 2026年2月13日_金融市场收盘简报.md
│   └── 2026年2月13日_简报_微信格式.txt
│
└── 🔧 工具脚本
    ├── send_to_wechat.py                # 微信发送工具
    └── wechat_config.json               # 微信配置（旧版）
```

---

## 🚀 快速开始

### 1️⃣ 配置密钥

编辑 `config.json`，填入：
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

### 2️⃣ 测试运行

**测试早报：**
```cmd
python morning_report_publisher.py
```

**测试晚报：**
```cmd
python market_report_publisher.py
```

### 3️⃣ 配置定时任务

右键运行 `一键配置定时任务.ps1`，自动创建：
- 早报任务：每天 7:00
- 晚报任务：每天 15:30

---

## 📊 功能对比

| 项目 | 早报 | 晚报 |
|------|------|------|
| **发布时间** | 每天 7:00 | 每天 15:30 |
| **封面风格** | 橙黄渐变+太阳 | 深蓝金色+箭头 |
| **主要内容** | 隔夜美股收盘 | A股收盘行情 |
| **次要内容** | 亚太市场、要闻 | 美股、期货 |
| **内容长度** | ~2450字符 | ~1750字符 |

---

## 📖 详细文档

- **系统说明**：`早报晚报系统说明.md`
- **安装指南**：`INSTALLATION_GUIDE.md`
- **定时任务**：`定时任务完整配置指南.md`
- **数据源集成**：`financial-report-publisher/references/data-sources.md`
- **微信API**：`financial-report-publisher/references/wechat-api.md`

---

## 🎯 使用场景

### 工作日模式
- **7:00 早报** → 通勤路上阅读（美股+要闻）
- **15:30 晚报** → 收盘后总结（A股+期货）

### 周末模式
- 可禁用晚报（A股不开盘）
- 保留早报（美股要闻）

---

## 🔧 技术栈

- **Python 3.7+**
- **Pillow** - 封面图片生成
- **Requests** - HTTP请求
- **微信公众号API** - 草稿发布
- **Windows任务计划程序** - 定时执行

---

## 📝 版本历史

**v1.4** (2026-02-13)
- ✅ 早报系统完成
- ✅ 晚报系统优化
- ✅ 封面图片本地生成
- ✅ UTF-8编码修复
- ✅ 标题层级优化
- ✅ 作者改为yuaner

---

## 📧 联系方式

如有问题，请查看文档或检查配置文件。

---

**风险提示**：市场有风险，投资需谨慎。本系统仅供学习交流使用。

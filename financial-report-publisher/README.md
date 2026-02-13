# Financial Report Publisher - 金融行情简报发布技能

自动化生成并发布金融行情简报到微信公众号的专业技能包。

## 快速安装

1. 将此技能包导入到小跃
2. 复制 `config.json.example` 为 `config.json`
3. 填写微信公众号和阿里云配置
4. 运行 `python scripts/market_report_publisher.py`

## 功能特性

✅ 自动获取A股、美股、期货行情数据  
✅ 本地生成专业金融风格封面图片  
✅ 格式化HTML行情简报内容  
✅ 一键发布到微信公众号草稿箱  
✅ UTF-8编码完美支持中文  
✅ 完整的错误处理和日志输出  

## 文件结构

```
financial-report-publisher/
├── SKILL.md                          # 技能说明文档
├── config.json.example               # 配置文件示例
├── scripts/
│   └── market_report_publisher.py    # 主程序
└── references/
    ├── data-sources.md               # 数据源集成指南
    └── wechat-api.md                 # 微信API参考文档
```

## 依赖安装

```bash
pip install requests Pillow
```

## 使用方法

详见 SKILL.md 文档。

## 版本

v1.0 (2026-02-13)

## 许可

仅供学习交流使用，投资需谨慎。

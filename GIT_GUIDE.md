# Git 版本控制指南

## 📦 仓库信息

- **项目名称**: Market Intelligence Publisher
- **版本**: v1.0
- **初始提交**: f7b076e
- **仓库路径**: `E:\jieyue_data\Market-Intelligence-Publisher`

---

## 📁 版本控制的文件

### ✅ 已纳入版本控制

#### 核心脚本
- `morning_report_publisher.py` - 早报主程序
- `market_report_publisher.py` - 晚报主程序
- `package_skill.py` - 技能打包脚本

#### 配置模板
- `config.json.example` - 配置文件模板

#### 批处理脚本
- `run_report.bat` - 运行脚本
- `配置定时任务.bat` - 定时任务配置
- `一键配置定时任务.ps1` - PowerShell配置脚本

#### 文档
- `README.md` - 项目说明
- `INSTALLATION_GUIDE.md` - 安装指南
- `早报晚报系统说明.md` - 系统说明
- `定时任务完整配置指南.md` - 定时任务指南
- `定时任务配置图文指南.md` - 图文配置指南

#### 技能包
- `financial-report-publisher/` - 技能包目录
  - `SKILL.md` - 技能说明
  - `scripts/` - 脚本目录
  - `references/` - 参考文档

### ❌ 已忽略的文件（.gitignore）

#### 敏感信息
- `config.json` - 包含API密钥
- `wechat_config.json` - 微信配置

#### 生成文件
- `*.jpg` - 封面图片
- `*.png` - 图片文件
- `*.log` - 日志文件

#### 临时文件
- `__pycache__/` - Python缓存
- `*.pyc` - 编译文件
- `*.tmp` - 临时文件

#### 技能包
- `*.skill` - 打包后的技能文件

---

## 🔧 常用Git命令

### 查看状态

```bash
cd /d "E:\jieyue_data\Market-Intelligence-Publisher"
git status
```

### 查看提交历史

```bash
git log
git log --oneline
git log --graph --oneline --all
```

### 添加文件

```bash
# 添加单个文件
git add morning_report_publisher.py

# 添加所有修改
git add .

# 添加指定类型文件
git add *.py
```

### 提交更改

```bash
git commit -m "描述你的修改"

# 示例
git commit -m "feat: 添加数据源集成功能"
git commit -m "fix: 修复封面图片生成bug"
git commit -m "docs: 更新README文档"
```

### 查看差异

```bash
# 查看未暂存的修改
git diff

# 查看已暂存的修改
git diff --staged

# 查看指定文件的修改
git diff morning_report_publisher.py
```

### 撤销修改

```bash
# 撤销工作区的修改
git checkout -- morning_report_publisher.py

# 撤销暂存区的修改
git reset HEAD morning_report_publisher.py

# 回退到上一个提交
git reset --hard HEAD^
```

### 分支管理

```bash
# 查看分支
git branch

# 创建新分支
git branch feature-new-data-source

# 切换分支
git checkout feature-new-data-source

# 创建并切换分支
git checkout -b feature-new-data-source

# 合并分支
git checkout master
git merge feature-new-data-source

# 删除分支
git branch -d feature-new-data-source
```

---

## 📝 提交规范

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- **feat**: 新功能
- **fix**: 修复bug
- **docs**: 文档更新
- **style**: 代码格式（不影响功能）
- **refactor**: 重构代码
- **test**: 测试相关
- **chore**: 构建过程或辅助工具的变动

### 示例

```bash
# 新功能
git commit -m "feat: 添加实时数据API集成"

# 修复bug
git commit -m "fix: 修复早报封面日期显示错误"

# 文档更新
git commit -m "docs: 更新安装指南，添加依赖说明"

# 代码重构
git commit -m "refactor: 优化封面生成代码结构"

# 配置变更
git commit -m "chore: 更新.gitignore，忽略日志文件"
```

---

## 🌿 分支策略

### 主分支

- **master** - 主分支，稳定版本

### 功能分支

- **feature/xxx** - 新功能开发
- **fix/xxx** - bug修复
- **docs/xxx** - 文档更新

### 工作流程

```bash
# 1. 创建功能分支
git checkout -b feature/real-time-data

# 2. 开发并提交
git add .
git commit -m "feat: 添加实时数据获取功能"

# 3. 切回主分支
git checkout master

# 4. 合并功能分支
git merge feature/real-time-data

# 5. 删除功能分支
git branch -d feature/real-time-data
```

---

## 🔄 日常工作流

### 每次修改代码后

```bash
# 1. 查看修改了什么
git status
git diff

# 2. 添加修改的文件
git add morning_report_publisher.py

# 3. 提交修改
git commit -m "fix: 修复早报时间格式问题"

# 4. 查看提交历史
git log --oneline
```

### 定期备份

```bash
# 查看所有提交
git log

# 创建标签（版本标记）
git tag v1.1 -m "版本1.1：添加实时数据功能"

# 查看标签
git tag
```

---

## 📊 版本管理

### 创建版本标签

```bash
# 创建轻量标签
git tag v1.0

# 创建附注标签
git tag -a v1.1 -m "版本1.1：优化封面生成"

# 查看标签
git tag

# 查看标签详情
git show v1.1

# 删除标签
git tag -d v1.0
```

### 版本回退

```bash
# 查看提交历史
git log --oneline

# 回退到指定版本
git reset --hard <commit-id>

# 回退到上一个版本
git reset --hard HEAD^

# 回退到上上个版本
git reset --hard HEAD^^
```

---

## 🔍 查看历史

### 查看文件修改历史

```bash
# 查看文件的提交历史
git log morning_report_publisher.py

# 查看文件的每次修改内容
git log -p morning_report_publisher.py

# 查看文件的简要修改统计
git log --stat morning_report_publisher.py
```

### 查看某次提交的详情

```bash
git show <commit-id>
git show HEAD
git show HEAD^
```

---

## 🚀 远程仓库（可选）

### 添加远程仓库

```bash
# 添加GitHub远程仓库
git remote add origin https://github.com/username/market-intelligence-publisher.git

# 查看远程仓库
git remote -v

# 推送到远程仓库
git push -u origin master

# 推送标签
git push origin --tags
```

### 从远程仓库拉取

```bash
# 拉取更新
git pull origin master

# 克隆仓库
git clone https://github.com/username/market-intelligence-publisher.git
```

---

## 📋 .gitignore 说明

当前忽略的文件类型：

```gitignore
# 配置文件（敏感信息）
config.json
wechat_config.json

# 生成的图片
*.jpg
*.png

# Python缓存
__pycache__/
*.pyc

# 日志文件
logs/
*.log

# 技能包
*.skill
```

---

## 🎯 最佳实践

### 1. 频繁提交
- 每完成一个小功能就提交
- 提交信息要清晰明确

### 2. 使用分支
- 开发新功能时创建新分支
- 测试通过后再合并到主分支

### 3. 写好提交信息
- 使用规范的提交格式
- 说明修改的原因和内容

### 4. 定期打标签
- 重要版本打标签
- 方便版本回退和追踪

### 5. 保护敏感信息
- 永远不要提交config.json
- 使用.example文件作为模板

---

## 🔧 常见问题

### Q1: 不小心提交了敏感文件怎么办？

```bash
# 从Git历史中删除文件
git rm --cached config.json
git commit -m "chore: 移除敏感配置文件"

# 添加到.gitignore
echo "config.json" >> .gitignore
git add .gitignore
git commit -m "chore: 更新.gitignore"
```

### Q2: 如何查看某个文件的修改历史？

```bash
git log -p morning_report_publisher.py
```

### Q3: 如何恢复误删的文件？

```bash
git checkout HEAD -- morning_report_publisher.py
```

### Q4: 如何比较两个版本的差异？

```bash
git diff v1.0 v1.1
```

---

## 📚 学习资源

- **Git官方文档**: https://git-scm.com/doc
- **Pro Git书籍**: https://git-scm.com/book/zh/v2
- **Git速查表**: https://training.github.com/downloads/zh_CN/github-git-cheat-sheet/

---

## ✅ 当前仓库状态

```
仓库: Market-Intelligence-Publisher
分支: master
提交: f7b076e - Initial commit: Market Intelligence Publisher v1.0
文件: 21个文件已纳入版本控制
状态: 干净的工作区
```

---

**最后更新**: 2026年02月13日

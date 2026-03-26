# 📚 Z-Library to Kindle — Claude Code 技能

[English](README.md) | [中文](README_CN.md)

> 一句话搞定：从 Z-Library 下载电子书并发送到 Kindle。例如："帮我下载《挽救计划》epub 格式，发到我的 Kindle"——搞定。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

---

## ⚠️ 免责声明

本工具仅用于教育、研究和技术演示目的。请遵守 Z-Library 的服务条款及当地版权法律。作者不对任何滥用行为负责。

---

## ✨ 功能特点

- **一句话操作** — 告诉 Claude 书名和格式就行
- **无需浏览器** — 使用 Z-Library eAPI（JSON 接口），无 Cloudflare 验证问题
- **自动发送到 Kindle** — 下载后自动通过邮件发送到 Kindle
- **多语言搜索** — 支持中文、英文等任意语言搜索
- **多格式支持** — EPUB、PDF、MOBI 等
- **一次配置，永久使用** — 配置一次凭据即可
- **依赖极少** — 仅需 `requests`，其余均为 Python 标准库

---

## 🛠️ 安装配置

### 前置准备（只需配置一次）

你需要准备：

| 项目 | 获取方式 |
|------|---------|
| **Z-Library 账号** | 在 [z-lib.sk](https://z-lib.sk) 注册（域名经常变动，可查看 [Wikipedia](https://en.wikipedia.org/wiki/Z-Library) 获取最新地址） |
| **Kindle 邮箱** | Amazon → [管理我的内容和设备](https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment) → 首选项 → 个人文档设置 |
| **Gmail + 应用专用密码** | [生成应用专用密码](https://myaccount.google.com/apppasswords)（不是 Gmail 登录密码！） |

> **为什么要用应用专用密码？** Gmail 默认阻止第三方应用登录。应用专用密码是 16 位令牌，允许 SMTP 访问而不会泄露主密码。也可以使用 Outlook 或 QQ 邮箱。

### 第一步：安装技能

```bash
# 克隆到 Claude Code 技能目录
git clone https://github.com/YOUR_USERNAME/zlib-to-kindle.git ~/.claude/skills/zlib-to-kindle
```

### 第二步：安装依赖

```bash
pip install requests
```

### 第三步：直接使用 — 自动引导配置

直接让 Claude Code 下载书籍即可。首次使用时，Claude 会自动询问你的凭据并保存到 `~/.zlib-kindle/config.json`（chmod 600，仅所有者可读写），无需手动配置。

也可以手动运行配置：

```bash
cd ~/.claude/skills/zlib-to-kindle && python3 scripts/setup.py
```

### 第四步：将发件邮箱添加到亚马逊的认可列表

这一步**必须完成**，否则亚马逊会拒收邮件：

1. 打开 [管理我的内容和设备](https://www.amazon.com/hz/mycd/myx#/home/settings) → 首选项
2. 找到 **已认可的个人文档电子邮件列表**
3. 添加你的 Gmail 地址（如 `your@gmail.com`）

---

## 📖 使用示例

### 基本用法 — 一句话搞定

```
帮我下载《挽救计划》epub 格式，发到 Kindle
```

### 先搜索，再选择

```
帮我搜一下"人类简史"有哪些版本
```

Claude 会以表格形式展示搜索结果，你可以选择要下载的版本。

---

## 📁 项目结构

```
zlib-to-kindle/
├── SKILL.md                  # Claude Code 技能定义（触发规则 + 工作流）
├── README.md                 # 英文文档
├── README_CN.md              # 本文件
├── .gitignore
└── scripts/
    ├── setup.py              # 可选的手动配置脚本（交互式 CLI）
    └── quick_send.py         # 一体化脚本：搜索 → 下载 → 发送
```

### 凭据存储

```
~/.zlib-kindle/
└── config.json    # chmod 600，不会提交到 git
```

包含：Z-Library 凭据、Kindle 邮箱、SMTP 凭据。存储在本地，仅所有者可访问。

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开 Pull Request

---

## 🙏 致谢

- [Z-Library](https://z-lib.sk) — 全球最大的数字图书馆
- [zlibrary-to-notebooklm](https://github.com/zstmfhy/zlibrary-to-notebooklm) — README 参考

---

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE)。

# 📚 Z-Library to Kindle — Claude Code Skill

[English](README.md) | [中文](README_CN.md)

> One command to get books from Z-Library to your Kindle. Example: "Send *Project Hail Mary* in EPUB to my Kindle" — done.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet.svg)](https://docs.anthropic.com/en/docs/claude-code)

---

## ⚠️ Disclaimer

This tool is intended for educational, research, and technical demonstration purposes only. Please comply with Z-Library's terms of service and your local copyright laws. The authors are not responsible for any misuse.

---

## ✨ Features

- **One-sentence operation** — just tell Claude the book name and format, done
- **No browser needed** — uses Z-Library's eAPI (JSON API), no Cloudflare issues
- **Auto send to Kindle** — downloads and emails to your Kindle in one step
- **Multi-language support** — search in Chinese, English, or any language
- **Multi-format support** — EPUB, PDF, MOBI, and more
- **One-time setup** — configure once, use forever
- **Minimal dependencies** — only `requests`, everything else is Python stdlib

---

## 🛠️ Setup

### Prerequisites (Configure once, use forever)

You need to prepare:

| Item | Where to get it |
|------|----------------|
| **Z-Library account** | Register at [z-lib.sk](https://z-lib.sk) (domains change often — check [Wikipedia](https://en.wikipedia.org/wiki/Z-Library) for the latest) |
| **Kindle email** | Amazon → [Manage Your Content and Devices](https://www.amazon.com/hz/mycd/preferences/myx#/home/settings/payment) → Preferences → Personal Document Settings |
| **Gmail + App Password** | [Generate App Password](https://myaccount.google.com/apppasswords) (not your Gmail login password!) |

> **Why App Password?** Gmail blocks less-secure apps by default. App Passwords are 16-character tokens that allow SMTP access without compromising your main password. You can also use Outlook or QQ Mail.

### Step 1: Install the Skill

```bash
# Clone to Claude Code skills directory
git clone https://github.com/YOUR_USERNAME/zlib-to-kindle.git ~/.claude/skills/zlib-to-kindle
```

### Step 2: Install dependency

```bash
pip install requests
```

### Step 3: Use it — setup is automatic

Just ask Claude Code to download a book. On first use, Claude will ask for your credentials and save them to `~/.zlib-kindle/config.json` (chmod 600, owner-only access). No manual setup needed.

Alternatively, you can run setup manually:

```bash
cd ~/.claude/skills/zlib-to-kindle && python3 scripts/setup.py
```

### Step 4: Add sender to Amazon's approved list

This is **required** or Amazon will reject the email:

1. Go to [Manage Your Content and Devices](https://www.amazon.com/hz/mycd/myx#/home/settings) → Preferences
2. Scroll to **Approved Personal Document E-mail List**
3. Add your Gmail address (e.g. `your@gmail.com`)

---

## 📖 Usage Examples

### Basic — just say it

```
Download "Project Hail Mary" as epub and send to my Kindle
```

### Search first, then choose

```
Search for "Sapiens" and show me all available editions
```

Claude will display results in a table, and you can pick which one to download.

---

## 📁 Project Structure

```
zlib-to-kindle/
├── SKILL.md                  # Claude Code skill definition (trigger rules + workflow)
├── README.md                 # This file
├── README_CN.md              # 中文文档
├── .gitignore
└── scripts/
    ├── setup.py              # Optional manual setup (interactive CLI)
    └── quick_send.py         # All-in-one: search → download → send (main script)
```

### Credentials storage

```
~/.zlib-kindle/
└── config.json    # chmod 600, never committed to git
```

Contains: Z-Library credentials, Kindle email, SMTP credentials. Stored locally with owner-only permissions.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- [Z-Library](https://z-lib.sk) — World's largest digital library
- [zlibrary-to-notebooklm](https://github.com/zstmfhy/zlibrary-to-notebooklm) — README inspiration

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

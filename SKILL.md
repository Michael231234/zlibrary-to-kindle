---
name: zlib-to-kindle
description: Search and download ebooks from Z-Library, optionally send to Kindle via email. Triggers on: book downloads, ebook search, send to Kindle, Z-Library queries, and Chinese equivalents like "下载书", "找书", "发到Kindle", "电子书".
---

# Z-Library to Kindle

Search and download ebooks from Z-Library, then optionally send them to Kindle via email.

Requires `pip install requests`. No browser automation — uses Z-Library's eAPI directly.

## First-time Setup (auto)

Before running `quick_send.py`, check if `~/.zlib-kindle/config.json` exists. If not, ask the user for the following and write the config directly:

1. **Z-Library email & password** — register at https://z-lib.sk (domains change often, check https://en.wikipedia.org/wiki/Z-Library for the latest)
2. **Kindle email** — find at Amazon → Manage Your Content and Devices → Preferences → Personal Document Settings
3. **Sender email & app password** — for Gmail, generate at https://myaccount.google.com/apppasswords
4. **SMTP preset** — gmail, outlook, or qq (default: gmail)

Then write `~/.zlib-kindle/config.json` (create dir if needed, chmod 600):

```json
{
  "zlib_email": "...",
  "zlib_password": "...",
  "kindle_email": "...@kindle.com",
  "sender_email": "...@gmail.com",
  "sender_password": "...",
  "smtp_preset": "gmail",
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 587,
    "use_tls": true
  }
}
```

SMTP presets: gmail → `smtp.gmail.com:587`, outlook → `smtp-mail.outlook.com:587`, qq → `smtp.qq.com:587`. All use TLS.

Remind the user to add their sender email to Amazon's approved senders list.

## Usage

### Auto-send (default)

When the user asks to find/download a book (e.g. "帮我下载《挽救计划》发到 Kindle"):

1. Parse the request for **title** (required), **author**, **format** (default: epub), **language**.
2. Run:

```bash
cd ~/.claude/skills/zlib-to-kindle && python3 scripts/quick_send.py --title "Book Title" --format epub --pick 1
```

This logs in, searches, picks the first result, downloads, and sends to Kindle in one step.

3. Report: success with book name, format, size, Kindle email — or failure with actionable fix.

### Manual selection

Omit `--pick` to return a JSON array of results. Show a table, let the user choose, then re-run with `--pick N`.

```bash
cd ~/.claude/skills/zlib-to-kindle && python3 scripts/quick_send.py --title "Book Title" --format epub
```

### All options

```bash
python3 scripts/quick_send.py \
  --title "Book Title" \
  --author "Author Name" \
  --format epub \
  --lang chinese \
  --pick 1
```

## Error Handling

| Error | Fix |
|-------|-----|
| Config not found | Ask user for credentials and write config (see setup above) |
| Login failed | Credentials may be wrong — ask user to re-enter, update config |
| No results | Broaden search terms, try different spelling or remove format filter |
| Download limit reached | Z-Library daily limit; try again tomorrow |
| SMTP auth failed | Generate a Gmail App Password at https://myaccount.google.com/apppasswords |
| Kindle email rejected | Add sender to Amazon's approved senders list |
| File too large (>50MB) | Try a different format or edition |

## Format Guide

- **EPUB** (recommended) — best formatting, auto-converted by Amazon
- **PDF** — preserves layout, poor reflow; use for textbooks only
- **MOBI** — legacy Kindle format, works but EPUB is preferred
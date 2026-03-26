#!/usr/bin/env python3
"""
Interactive setup for zlib-to-kindle.
Saves credentials to ~/.zlib-kindle/config.json
"""

import json
import os
import sys
import getpass
from pathlib import Path

CONFIG_DIR = Path.home() / ".zlib-kindle"
CONFIG_FILE = CONFIG_DIR / "config.json"

GMAIL_SMTP = {
    "host": "smtp.gmail.com",
    "port": 587,
    "use_tls": True,
}

OUTLOOK_SMTP = {
    "host": "smtp-mail.outlook.com",
    "port": 587,
    "use_tls": True,
}

QQ_SMTP = {
    "host": "smtp.qq.com",
    "port": 587,
    "use_tls": True,
}

SMTP_PRESETS = {
    "gmail": GMAIL_SMTP,
    "outlook": OUTLOOK_SMTP,
    "qq": QQ_SMTP,
}


def load_existing_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def setup():
    print("=" * 60)
    print("  Z-Library to Kindle — Setup")
    print("=" * 60)
    print()

    existing = load_existing_config()

    # Z-Library credentials
    print("[1/4] Z-Library Account")
    print("  You need a singlelogin account: https://singlelogin.re")
    zlib_email = input(f"  Email [{existing.get('zlib_email', '')}]: ").strip()
    if not zlib_email:
        zlib_email = existing.get("zlib_email", "")
    if not zlib_email:
        print("  ❌ Z-Library email is required.")
        sys.exit(1)

    zlib_password = getpass.getpass("  Password (hidden): ").strip()
    if not zlib_password:
        zlib_password = existing.get("zlib_password", "")
    if not zlib_password:
        print("  ❌ Z-Library password is required.")
        sys.exit(1)
    print()

    # Kindle email
    print("[2/4] Kindle Email")
    print("  Find it at: Amazon → Manage Your Content and Devices → Preferences → Personal Document Settings")
    kindle_email = input(f"  Kindle email [{existing.get('kindle_email', '')}]: ").strip()
    if not kindle_email:
        kindle_email = existing.get("kindle_email", "")
    if not kindle_email:
        print("  ❌ Kindle email is required.")
        sys.exit(1)
    print()

    # Sender email
    print("[3/4] Sender Email (for SMTP)")
    print("  This email will send books to your Kindle.")
    print("  For Gmail: use an App Password, not your regular password.")
    print("  Generate at: https://myaccount.google.com/apppasswords")
    sender_email = input(f"  Sender email [{existing.get('sender_email', '')}]: ").strip()
    if not sender_email:
        sender_email = existing.get("sender_email", "")
    if not sender_email:
        print("  ❌ Sender email is required.")
        sys.exit(1)

    sender_password = getpass.getpass("  Sender password / App Password (hidden): ").strip()
    if not sender_password:
        sender_password = existing.get("sender_password", "")
    if not sender_password:
        print("  ❌ Sender password is required.")
        sys.exit(1)
    print()

    # SMTP settings
    print("[4/4] SMTP Settings")
    print("  Presets: gmail, outlook, qq")
    print("  Or type 'custom' to enter manually.")
    smtp_choice = input(f"  SMTP preset [{existing.get('smtp_preset', 'gmail')}]: ").strip().lower()
    if not smtp_choice:
        smtp_choice = existing.get("smtp_preset", "gmail")

    if smtp_choice in SMTP_PRESETS:
        smtp = SMTP_PRESETS[smtp_choice].copy()
        smtp_preset = smtp_choice
    elif smtp_choice == "custom":
        smtp_host = input("  SMTP host: ").strip()
        try:
            smtp_port = int(input("  SMTP port [587]: ").strip() or "587")
        except ValueError:
            print("  Invalid port, using 587.")
            smtp_port = 587
        smtp_tls = input("  Use TLS? [y/n, default y]: ").strip().lower() != "n"
        smtp = {"host": smtp_host, "port": smtp_port, "use_tls": smtp_tls}
        smtp_preset = "custom"
    else:
        print(f"  Unknown preset '{smtp_choice}', using Gmail defaults.")
        smtp = GMAIL_SMTP.copy()
        smtp_preset = "gmail"
    print()

    # Save config
    config = {
        "zlib_email": zlib_email,
        "zlib_password": zlib_password,
        "kindle_email": kindle_email,
        "sender_email": sender_email,
        "sender_password": sender_password,
        "smtp_preset": smtp_preset,
        "smtp": smtp,
    }

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)  # owner read/write only

    print("=" * 60)
    print("  ✅ Configuration saved to ~/.zlib-kindle/config.json")
    print()
    print("  ⚠️  IMPORTANT: Add your sender email to Amazon's approved list:")
    print("  https://www.amazon.com/hz/mycd/myx#/home/settings/payment")
    print("  → Personal Document Settings → Approved Personal Document E-mail List")
    print(f"  → Add: {sender_email}")
    print("=" * 60)


if __name__ == "__main__":
    setup()

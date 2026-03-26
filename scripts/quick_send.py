#!/usr/bin/env python3
"""
All-in-one: search -> pick best match -> download -> send to Kindle.
Uses Z-Library eAPI (JSON) directly - no HTML scraping.

Usage:
  python3 quick_send.py --title "Book Title" [--author "Author"] [--format epub] [--lang chinese] [--pick 1]
  --pick N: auto-select the Nth result (1-indexed). If omitted, prints results for manual selection.

Output: JSON with full pipeline status.
"""

import argparse
import json
import os
import smtplib
import sys
import tempfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

CONFIG_FILE = Path.home() / ".zlib-kindle" / "config.json"
MAX_ATTACHMENT_SIZE_MB = 50
EAPI_DOMAIN = "1lib.sk"
REQUEST_TIMEOUT = 30
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
POST_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "user-agent": UA,
}
GET_HEADERS = {
    "user-agent": UA,
}


def load_config():
    if not CONFIG_FILE.exists():
        print(json.dumps({"error": "Config not found. Run 'python3 scripts/setup.py' first.", "success": False}))
        sys.exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def eapi_login(config):
    """Login via eAPI, return cookies dict."""
    resp = requests.post(
        f"https://{EAPI_DOMAIN}/eapi/user/login",
        data={"email": config["zlib_email"], "password": config["zlib_password"]},
        headers=POST_HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    data = resp.json()
    if not data.get("success"):
        return None, data.get("error", "Login failed")
    user = data["user"]
    cookies = {
        "remix_userid": str(user["id"]),
        "remix_userkey": user["remix_userkey"],
        "siteLanguageV2": "en",
    }
    return cookies, None


def eapi_search(cookies, title, author=None, fmt=None, lang=None, limit=10):
    """Search books via eAPI."""
    data = {"message": title, "limit": limit}
    if author:
        data["message"] = f"{title} {author}"
    if fmt:
        data["extensions[]"] = fmt.lower()
    if lang:
        data["languages[]"] = lang.capitalize()

    resp = requests.post(
        f"https://{EAPI_DOMAIN}/eapi/book/search",
        data=data,
        cookies=cookies,
        headers=POST_HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    result = resp.json()
    if not result.get("success"):
        return None, result.get("error", "Search failed")
    return result.get("books", []), None


def eapi_get_download_link(cookies, book_id, book_hash):
    """Get download link for a book."""
    resp = requests.get(
        f"https://{EAPI_DOMAIN}/eapi/book/{book_id}/{book_hash}/file",
        cookies=cookies,
        headers=GET_HEADERS,
        timeout=REQUEST_TIMEOUT,
    )
    data = resp.json()
    if not data.get("success"):
        return None, data.get("error", "Failed to get download link")
    file_info = data.get("file", {})
    if not file_info.get("downloadLink"):
        return None, "No download link available"
    if not file_info.get("allowDownload", True):
        return None, "Download not allowed for this book"
    return file_info, None


def download_file(download_link, filename, tmpdir, cookies=None):
    """Download file from URL to tmpdir."""
    filepath = os.path.join(tmpdir, filename)
    headers = GET_HEADERS.copy()
    headers["authority"] = download_link.split("/")[2]
    resp = requests.get(download_link, headers=headers, cookies=cookies, stream=True, timeout=120)
    if resp.status_code != 200:
        return None, f"Download failed: HTTP {resp.status_code}"
    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return filepath, None


def send_to_kindle(filepath, filename, config):
    """Send an ebook file to Kindle via SMTP email."""
    file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
    if file_size_mb > MAX_ATTACHMENT_SIZE_MB:
        return {"success": False, "error": f"File too large ({file_size_mb:.1f}MB > {MAX_ATTACHMENT_SIZE_MB}MB limit)"}

    msg = MIMEMultipart()
    msg["From"] = config["sender_email"]
    msg["To"] = config["kindle_email"]
    msg["Subject"] = "convert"

    msg.attach(MIMEText("Sent via zlib-to-kindle skill.", "plain"))

    with open(filepath, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename=("utf-8", "", filename))
    msg.attach(part)

    smtp_config = config["smtp"]
    try:
        server = smtplib.SMTP(smtp_config["host"], smtp_config["port"], timeout=30)
        if smtp_config.get("use_tls", True):
            server.starttls()
        server.login(config["sender_email"], config["sender_password"])
        server.sendmail(config["sender_email"], config["kindle_email"], msg.as_string())
        server.quit()
        return {"success": True}
    except smtplib.SMTPAuthenticationError:
        return {"success": False, "error": "SMTP auth failed. Use App Password for Gmail."}
    except Exception as e:
        return {"success": False, "error": f"SMTP error: {str(e)}"}


def run_pipeline(title, author=None, fmt=None, lang=None, pick=None):
    config = load_config()

    # Step 1: Login
    print(json.dumps({"step": "login", "status": "starting"}), file=sys.stderr)
    cookies, err = eapi_login(config)
    if err:
        print(json.dumps({"success": False, "error": f"Login failed: {err}"}))
        return

    # Step 2: Search
    print(json.dumps({"step": "search", "status": "starting", "query": title}), file=sys.stderr)
    books, err = eapi_search(cookies, title, author=author, fmt=fmt, lang=lang)
    if err:
        print(json.dumps({"success": False, "error": f"Search failed: {err}"}))
        return

    if not books:
        print(json.dumps({"success": False, "error": "No results found.", "step": "search"}))
        return

    # Format results
    results_list = []
    for i, book in enumerate(books):
        results_list.append({
            "index": i + 1,
            "id": book.get("id", ""),
            "hash": book.get("hash", ""),
            "name": book.get("title", ""),
            "authors": book.get("author", ""),
            "year": book.get("year", ""),
            "language": book.get("language", ""),
            "extension": book.get("extension", ""),
            "size": book.get("filesizeString", ""),
        })

    # If no auto-pick, return search results
    if pick is None:
        print(json.dumps({
            "step": "search_complete",
            "success": True,
            "results": results_list,
            "message": "Use --pick N to select a result.",
        }, ensure_ascii=False, indent=2))
        return

    # Step 3: Select and download
    pick_index = pick - 1
    if pick_index < 0 or pick_index >= len(books):
        print(json.dumps({"success": False, "error": f"Invalid pick index {pick}. Available: 1-{len(books)}"}))
        return

    selected = books[pick_index]
    selected_info = results_list[pick_index]
    book_id = selected["id"]
    book_hash = selected["hash"]

    print(json.dumps({"step": "download", "status": "getting_link", "book": selected_info["name"]}), file=sys.stderr)

    file_info, err = eapi_get_download_link(cookies, book_id, book_hash)
    if err:
        print(json.dumps({"success": False, "error": f"Download link failed: {err}"}))
        return

    download_link = file_info["downloadLink"]
    extension = file_info.get("extension", "epub").lower()
    description = file_info.get("description", selected_info["name"])
    safe_name = "".join(c for c in description if c.isalnum() or c in " ._-()").strip() or "book"
    filename = f"{safe_name}.{extension}"

    tmpdir = tempfile.mkdtemp(prefix="zlib-kindle-")
    print(json.dumps({"step": "download", "status": "downloading"}), file=sys.stderr)

    filepath, err = download_file(download_link, filename, tmpdir, cookies=cookies)
    if err:
        print(json.dumps({"success": False, "error": err}))
        return

    file_size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
    print(json.dumps({"step": "download", "status": "complete", "size_mb": file_size_mb}), file=sys.stderr)

    # Step 4: Send to Kindle
    print(json.dumps({"step": "send", "status": "starting"}), file=sys.stderr)
    result = send_to_kindle(filepath, filename, config)

    # Cleanup
    try:
        os.remove(filepath)
        os.rmdir(tmpdir)
    except OSError:
        pass

    # Final output
    output = {
        "success": result["success"],
        "book_name": selected_info["name"],
        "authors": selected_info["authors"],
        "format": extension.upper(),
        "size_mb": file_size_mb,
        "kindle_email": config["kindle_email"],
    }
    if not result["success"]:
        output["error"] = result.get("error", "")

    print(json.dumps(output, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Search + Download + Send to Kindle (via eAPI)")
    parser.add_argument("--title", required=True, help="Book title")
    parser.add_argument("--author", default=None, help="Author name")
    parser.add_argument("--format", dest="fmt", default=None, help="Format: epub, pdf, mobi")
    parser.add_argument("--lang", default=None, help="Language: english, chinese, etc.")
    parser.add_argument("--pick", type=int, default=None, help="Auto-select Nth result (1-indexed)")
    args = parser.parse_args()

    run_pipeline(
        title=args.title,
        author=args.author,
        fmt=args.fmt,
        lang=args.lang,
        pick=args.pick,
    )


if __name__ == "__main__":
    main()

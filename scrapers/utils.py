"""
scrapers/utils.py
-----------------
Shared helpers used by all department scrapers.
"""

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Mimic a real browser to avoid 403 blocks from Princeton servers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

JSON_HEADERS = {
    **HEADERS,
    "Accept": "application/json, application/vnd.api+json",
}

TIMEOUT = 20  # seconds


def fetch(url: str) -> BeautifulSoup:
    """GET a page and return a BeautifulSoup object."""
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def fetch_json(url: str, params: dict = None) -> dict | list:
    """GET a JSON API endpoint and return parsed data."""
    resp = requests.get(url, headers=JSON_HEADERS, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def clean(text: str) -> str:
    """Strip and collapse whitespace."""
    return re.sub(r"\s+", " ", (text or "").strip())


def parse_date(raw: str) -> str:
    """
    Try common date formats and return ISO 8601 (YYYY-MM-DD).
    Returns the original string unchanged if no format matches.
    """
    raw = clean(raw)
    if "T" in raw:
        raw = raw.split("T")[0]
    formats = [
        "%Y-%m-%d",        # 2026-04-10  (API format — try first)
        "%B %d, %Y",       # April 10, 2026
        "%b %d, %Y",       # Apr 10, 2026
        "%B %d %Y",        # April 10 2026
        "%m/%d/%Y",        # 04/10/2026
        "%A, %B %d, %Y",   # Friday, April 10, 2026
        "%A, %b %d, %Y",   # Fri, Apr 10, 2026
    ]
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw


def parse_time(raw: str) -> str:
    """Normalise time strings to H:MM AM/PM."""
    raw = clean(raw)
    if "T" in raw:
        raw = raw.split("T")[1][:5]
    for fmt in ["%I:%M %p", "%I:%M%p", "%H:%M", "%I %p"]:
        try:
            return datetime.strptime(raw.upper(), fmt).strftime("%I:%M %p").lstrip("0")
        except ValueError:
            continue
    return raw


def absolute_url(base: str, href: str) -> str:
    """Turn a relative href into an absolute URL."""
    if not href:
        return ""
    if href.startswith("http"):
        return href
    from urllib.parse import urljoin
    return urljoin(base, href)


def strip_html(text: str) -> str:
    """Remove HTML tags from a string."""
    return clean(BeautifulSoup(text or "", "html.parser").get_text())

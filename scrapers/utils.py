"""
scrapers/utils.py
-----------------
Shared helpers used by all department scrapers.
"""

import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; GEC-Princeton-EventBot/1.0; "
        "+https://github.com/gecseas/princeton-events)"
    )
}
TIMEOUT = 15  # seconds


def fetch(url: str) -> BeautifulSoup:
    """GET a page and return a BeautifulSoup object. Raises on HTTP errors."""
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def clean(text: str) -> str:
    """Strip and collapse whitespace."""
    return re.sub(r"\s+", " ", (text or "").strip())


def parse_date(raw: str) -> str:
    """
    Try common date formats and return ISO 8601 (YYYY-MM-DD).
    Returns the original string unchanged if no format matches.
    """
    raw = clean(raw)
    formats = [
        "%B %d, %Y",       # April 10, 2026
        "%b %d, %Y",       # Apr 10, 2026
        "%B %d %Y",        # April 10 2026
        "%m/%d/%Y",        # 04/10/2026
        "%Y-%m-%d",        # 2026-04-10
        "%A, %B %d, %Y",   # Friday, April 10, 2026
        "%A, %b %d, %Y",   # Fri, Apr 10, 2026
    ]
    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw  # return as-is if nothing matches


def parse_time(raw: str) -> str:
    """Normalise time strings to HH:MM AM/PM. Returns raw string on failure."""
    raw = clean(raw)
    for fmt in ["%I:%M %p", "%I:%M%p", "%H:%M", "%I %p"]:
        try:
            return datetime.strptime(raw.upper(), fmt).strftime("%I:%M %p").lstrip("0")
        except ValueError:
            continue
    return raw


def absolute_url(base: str, href: str) -> str:
    """Turn a relative href into an absolute URL."""
    if href.startswith("http"):
        return href
    from urllib.parse import urljoin
    return urljoin(base, href)

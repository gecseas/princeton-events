"""
scrapers/decenter.py  —  Princeton Center for the Decentralization of Power Through Blockchain
URL: https://decenter.princeton.edu/events/
Structure: WordPress site; events listed with title, date, and description.
"""

from .utils import fetch, clean, parse_date, parse_time, absolute_url
import re

BASE = "https://decenter.princeton.edu"
EVENTS_URL = f"{BASE}/events/"
DEPARTMENT = "DeCenter (Center for Decentralization of Power Through Blockchain)"
TAGS = ["Blockchain", "Tech Policy", "Computer Science", "Financial Engineering"]


def scrape() -> list[dict]:
    soup = fetch(EVENTS_URL)
    events = []

    # WordPress/custom theme — try common event listing patterns
    items = soup.select(
        "article[class*='event'], .event, .tribe-events-calendar-list__event, "
        ".views-row, article"
    )

    for item in items:
        title_el = item.select_one(
            "h2 a, h3 a, h4 a, .tribe-events-calendar-list__event-title a, "
            ".entry-title a, a[href*='/events/']"
        )
        if not title_el:
            continue

        title = clean(title_el.get_text())
        link = absolute_url(BASE, title_el["href"])

        # Date: try tribe plugin first, then generic selectors
        date_el = item.select_one(
            ".tribe-event-date-start, time, .date, [class*='date'], [class*='time']"
        )
        date_raw = ""
        if date_el:
            date_raw = clean(date_el.get("datetime") or date_el.get_text())

        time_match = re.search(r"(\d{1,2}:\d{2}\s*[ap]m)", date_raw, re.IGNORECASE)
        time = parse_time(time_match.group(1)) if time_match else ""
        date_clean = re.sub(r"\d{1,2}:\d{2}\s*[ap]m.*", "", date_raw, flags=re.IGNORECASE).strip(" ,–-@")
        date = parse_date(date_clean) if date_clean else ""

        loc_el = item.select_one(".tribe-venue, .location, [class*='location'], [class*='venue']")
        location = clean(loc_el.get_text()) if loc_el else ""

        desc_el = item.select_one(
            ".tribe-events-calendar-list__event-description, .entry-summary, .description, p"
        )
        description = clean(desc_el.get_text()) if desc_el else ""

        events.append({
            "title": title,
            "date": date,
            "time": time,
            "location": location,
            "link": link,
            "department": DEPARTMENT,
            "tags": TAGS,
            "speaker": "",
            "description": description,
        })

    return events

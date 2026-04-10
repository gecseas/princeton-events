"""
scrapers/citp.py  —  Center for Information Technology Policy
URL: https://citp.princeton.edu/events/
Structure: WordPress/custom; events in list items with date, title, and description.
"""

from .utils import fetch, clean, parse_date, parse_time, absolute_url

BASE = "https://citp.princeton.edu"
EVENTS_URL = f"{BASE}/events/"
DEPARTMENT = "Center for Information Technology Policy (CITP)"
TAGS = ["Tech Policy", "AI / ML", "Privacy", "Internet", "Computer Science"]


def scrape() -> list[dict]:
    soup = fetch(EVENTS_URL)
    events = []

    # CITP uses a custom events listing — each event is in a <div class="event"> or similar
    items = soup.select(".event, .views-row, article[class*='event'], li[class*='event']")

    if not items:
        # Generic fallback: look for headings that link to event detail pages
        items = soup.select("article, .entry, .post")

    for item in items:
        title_el = item.select_one("h2 a, h3 a, h4 a, .event-title a, a[href*='/events/']")
        if not title_el:
            continue

        title = clean(title_el.get_text())
        link = absolute_url(BASE, title_el["href"])

        date_el = item.select_one("time, .date, .event-date, [class*='date']")
        date_raw = clean(date_el.get("datetime") or date_el.get_text()) if date_el else ""
        date = parse_date(date_raw.split("@")[0].strip()) if date_raw else ""
        time_raw = date_raw.split("@")[1].strip() if "@" in date_raw else ""
        time = parse_time(time_raw) if time_raw else ""

        loc_el = item.select_one(".location, .venue, [class*='location']")
        location = clean(loc_el.get_text()) if loc_el else ""

        desc_el = item.select_one(".description, .summary, p")
        description = clean(desc_el.get_text()) if desc_el else ""

        # CITP often lists speaker in the title or subtitle
        speaker_el = item.select_one(".speaker, .presenter, .subtitle")
        speaker = clean(speaker_el.get_text()) if speaker_el else ""

        events.append({
            "title": title,
            "date": date,
            "time": time,
            "location": location,
            "link": link,
            "department": DEPARTMENT,
            "tags": TAGS,
            "speaker": speaker,
            "description": description,
        })

    return events

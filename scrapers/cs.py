"""
scrapers/cs.py  —  Department of Computer Science
URL: https://www.cs.princeton.edu/events
Structure: Drupal-based; events listed with date, title, speaker, and description.
"""

from .utils import fetch, clean, parse_date, parse_time, absolute_url

BASE = "https://www.cs.princeton.edu"
EVENTS_URL = f"{BASE}/events"
DEPARTMENT = "Department of Computer Science"
TAGS = ["Computer Science", "AI / ML", "Theory", "Systems"]


def scrape() -> list[dict]:
    soup = fetch(EVENTS_URL)
    events = []

    # CS Princeton uses Drupal views; events are in <div class="view-content"> rows
    rows = soup.select(".view-content .views-row, .views-row, article[class*='event']")

    if not rows:
        rows = soup.select("article, li[class*='event'], .event-item")

    for row in rows:
        title_el = row.select_one("h2 a, h3 a, .views-field-title a, span.field-content a")
        if not title_el:
            continue

        title = clean(title_el.get_text())
        link = absolute_url(BASE, title_el["href"])

        # Date: Drupal often uses <span class="date-display-single"> or <time>
        date_el = row.select_one(
            ".date-display-single, time, .views-field-field-event-date, [class*='date']"
        )
        date_raw = ""
        if date_el:
            date_raw = clean(date_el.get("datetime") or date_el.get_text())

        # Try to split date and time on common separators
        import re
        time_match = re.search(r"(\d{1,2}:\d{2}\s*[ap]m)", date_raw, re.IGNORECASE)
        time = parse_time(time_match.group(1)) if time_match else ""
        date_clean = re.sub(r"\d{1,2}:\d{2}\s*[ap]m.*", "", date_raw, flags=re.IGNORECASE).strip(" ,–-")
        date = parse_date(date_clean) if date_clean else ""

        loc_el = row.select_one(".views-field-field-location, .location, [class*='room'], [class*='location']")
        location = clean(loc_el.get_text()) if loc_el else ""

        speaker_el = row.select_one(".views-field-field-speaker, .speaker, [class*='speaker']")
        speaker = clean(speaker_el.get_text()) if speaker_el else ""

        desc_el = row.select_one(".views-field-body, .description, p")
        description = clean(desc_el.get_text()) if desc_el else ""

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

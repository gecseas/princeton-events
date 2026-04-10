"""
scrapers/acee.py  —  Andlinger Center for Energy and the Environment
URL: https://acee.princeton.edu/events/
Structure: WordPress site; events in <article> tags with class "tribe-events-calendar-list__event"
"""

from .utils import fetch, clean, parse_date, parse_time, absolute_url

BASE = "https://acee.princeton.edu"
EVENTS_URL = f"{BASE}/events/"
DEPARTMENT = "Andlinger Center for Energy and the Environment"
TAGS = ["Energy", "Environment", "Climate", "Engineering"]


def scrape() -> list[dict]:
    soup = fetch(EVENTS_URL)
    events = []

    # The Events Calendar (tribe) plugin structures each event as an <article>
    articles = soup.select("article.type-tribe_events, article[class*='tribe-events']")

    # Fallback: generic article tags with event-like links
    if not articles:
        articles = soup.select("article")

    for article in articles:
        title_el = article.select_one("h2, h3, .tribe-events-calendar-list__event-title a")
        if not title_el:
            continue

        link_el = title_el.find("a") or article.select_one("a[href*='acee.princeton.edu']")
        title = clean(title_el.get_text())
        link = absolute_url(BASE, link_el["href"]) if link_el else ""

        date_el = article.select_one(
            ".tribe-event-date-start, time, [class*='date']"
        )
        date_raw = clean(date_el.get_text()) if date_el else ""
        date = parse_date(date_raw.split("@")[0].strip()) if date_raw else ""
        time_raw = date_raw.split("@")[1].strip() if "@" in date_raw else ""
        time = parse_time(time_raw) if time_raw else ""

        loc_el = article.select_one(".tribe-venue, [class*='location'], [class*='venue']")
        location = clean(loc_el.get_text()) if loc_el else ""

        desc_el = article.select_one(".tribe-events-calendar-list__event-description, p")
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

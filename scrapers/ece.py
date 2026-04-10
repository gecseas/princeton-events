"""
scrapers/ece.py  —  Electrical and Computer Engineering
URL: https://ece.princeton.edu/events
"""
from .utils import fetch, clean, parse_date, parse_time, absolute_url
import re

BASE = "https://ece.princeton.edu"
EVENTS_URL = f"{BASE}/events"
DEPARTMENT = "Electrical and Computer Engineering (ECE)"
TAGS = ["Electrical Engineering", "Computer Engineering", "Engineering", "AI / ML"]

def scrape() -> list[dict]:
    soup = fetch(EVENTS_URL)
    rows = soup.select(".view-content .views-row, .views-row, article")
    events = []
    for row in rows:
        title_el = row.select_one("h2 a, h3 a, .views-field-title a, a[href*='/events/']")
        if not title_el:
            continue
        title = clean(title_el.get_text())
        link = absolute_url(BASE, title_el["href"])
        date_el = row.select_one(".date-display-single, time, [class*='date']")
        date_raw = clean(date_el.get("datetime") or date_el.get_text()) if date_el else ""
        time_match = re.search(r"(\d{1,2}:\d{2}\s*[ap]m)", date_raw, re.IGNORECASE)
        time = parse_time(time_match.group(1)) if time_match else ""
        date_clean = re.sub(r"\d{1,2}:\d{2}\s*[ap]m.*", "", date_raw, flags=re.IGNORECASE).strip(" ,–-")
        date = parse_date(date_clean) if date_clean else ""
        loc_el = row.select_one(".location, [class*='location']")
        location = clean(loc_el.get_text()) if loc_el else ""
        speaker_el = row.select_one(".speaker, [class*='speaker']")
        speaker = clean(speaker_el.get_text()) if speaker_el else ""
        desc_el = row.select_one(".views-field-body, p")
        description = clean(desc_el.get_text()) if desc_el else ""
        events.append({"title": title, "date": date, "time": time, "location": location,
                       "link": link, "department": DEPARTMENT, "tags": TAGS,
                       "speaker": speaker, "description": description})
    return events

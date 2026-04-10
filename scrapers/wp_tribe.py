"""
scrapers/wp_tribe.py
--------------------
Helper for WordPress sites using The Events Calendar (Tribe) plugin.
These sites expose a REST API at /wp-json/tribe/events/v1/events
that returns structured JSON — far more reliable than scraping HTML.
"""

from .utils import fetch_json, clean, parse_date, parse_time, strip_html
from datetime import date


def scrape_tribe(base_url: str, department: str, tags: list[str]) -> list[dict]:
    """
    Fetch upcoming events from a Tribe Events REST API endpoint.
    Returns a list of normalised event dicts.
    """
    api_url = f"{base_url.rstrip('/')}/wp-json/tribe/events/v1/events"
    today = date.today().isoformat()

    params = {
        "start_date": today,
        "per_page": 50,
        "status": "publish",
    }

    data = fetch_json(api_url, params=params)
    events_raw = data.get("events", [])
    events = []

    for ev in events_raw:
        title = clean(ev.get("title", ""))
        if not title:
            continue

        link = ev.get("url", "")
        start = ev.get("start_date", "")          # "2026-04-10 15:00:00"
        date_str = parse_date(start.split(" ")[0]) if start else ""
        time_str = parse_time(start.split(" ")[1]) if start and " " in start else ""

        # Venue
        venue = ev.get("venue", {})
        location_parts = [
            venue.get("venue", ""),
            venue.get("address", ""),
        ]
        location = clean(", ".join(p for p in location_parts if p))

        # Description — strip HTML tags
        description = strip_html(ev.get("description", ""))[:400]

        # Organizer as speaker proxy
        organizers = ev.get("organizer", [])
        speaker = clean(organizers[0].get("organizer", "")) if organizers else ""

        events.append({
            "title": title,
            "date": date_str,
            "time": time_str,
            "location": location,
            "link": link,
            "department": department,
            "tags": tags,
            "speaker": speaker,
            "description": description,
        })

    return events

"""
scrapers/drupal_api.py
----------------------
Helper for Princeton's Drupal-based department sites.
These sites expose a JSON:API at /jsonapi/node/event
that returns structured data without triggering 403 blocks.
"""

from .utils import fetch_json, clean, parse_date, parse_time, strip_html, absolute_url
from datetime import date, timezone
import datetime as dt


def scrape_drupal(base_url: str, department: str, tags: list[str]) -> list[dict]:
    """
    Fetch upcoming events from a Drupal JSON:API endpoint.
    Returns a list of normalised event dicts.
    """
    base = base_url.rstrip("/")
    api_url = f"{base}/jsonapi/node/event"
    today = dt.date.today().isoformat()

    params = {
        # Filter to only upcoming events
        "filter[field_event_date][condition][path]": "field_event_date",
        "filter[field_event_date][condition][operator]": ">=",
        "filter[field_event_date][condition][value]": f"{today}T00:00:00Z",
        # Sort ascending by date
        "sort": "field_event_date",
        # Limit results
        "page[limit]": 50,
    }

    data = fetch_json(api_url, params=params)
    items = data.get("data", [])
    events = []

    for item in items:
        attrs = item.get("attributes", {})

        title = clean(attrs.get("title", ""))
        if not title:
            continue

        # Build event URL from slug
        path = attrs.get("path", {}).get("alias", "")
        link = absolute_url(base, path) if path else ""

        # Date/time — Drupal stores as ISO 8601
        start_raw = attrs.get("field_event_date", "") or attrs.get("field_date", "")
        if isinstance(start_raw, dict):
            start_raw = start_raw.get("value", "")
        date_str = parse_date(str(start_raw)) if start_raw else ""
        time_str = ""
        if start_raw and "T" in str(start_raw):
            time_str = parse_time(str(start_raw))

        # Location
        location = clean(
            attrs.get("field_location", "") or
            attrs.get("field_room", "") or
            attrs.get("field_building", "") or ""
        )

        # Description
        body = attrs.get("body", {})
        if isinstance(body, dict):
            body = body.get("value", "") or body.get("processed", "")
        description = strip_html(str(body))[:400]

        # Speaker
        speaker = clean(attrs.get("field_speaker", "") or "")

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

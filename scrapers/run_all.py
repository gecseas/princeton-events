"""
run_all.py
----------
Runs every department scraper and writes the merged output to data/events.json.
To add a new department: create scrapers/my_dept.py with a scrape() function
that returns a list of event dicts, then import and add it to SCRAPERS below.
"""

import json
import os
import traceback
from datetime import datetime, timezone

# --- Import one module per source ---
# wp_tribe.py and drupal_api.py are shared helpers, not scrapers themselves
from scrapers import (
    acee,       # WordPress/Tribe → Andlinger Center
    citp,       # WordPress/Tribe → Center for Information Technology Policy
    cbe,        # Drupal JSON:API → Chemical and Biological Engineering
    cee,        # Drupal JSON:API → Civil and Environmental Engineering
    cs,         # Drupal JSON:API → Computer Science
    decenter,   # WordPress/Tribe → DeCenter (Blockchain)
    ece,        # Drupal JSON:API → Electrical and Computer Engineering
    mae,        # Drupal JSON:API → Mechanical and Aerospace Engineering
    odbi,       # WordPress/Tribe → Omenn-Darling Bioengineering Institute
    orfe,       # Drupal JSON:API → Operations Research and Financial Engineering
    pmi,        # Drupal JSON:API → Princeton Materials Institute (materials.princeton.edu)
)

SCRAPERS = [
    acee, citp, cbe, cee, cs,
    decenter, ece, mae, odbi, orfe, pmi,
]

EVENT_KEYS = ["title", "date", "time", "location", "link", "department", "tags", "speaker", "description"]


def validate(event: dict) -> bool:
    """Reject events missing the minimum required fields."""
    return bool(event.get("title") and event.get("date") and event.get("link"))


def run():
    all_events = []
    failures = []

    for module in SCRAPERS:
        name = module.__name__.split(".")[-1].upper()
        print(f"  Scraping {name}...", end=" ")
        try:
            events = module.scrape()
            valid = [e for e in events if validate(e)]
            # Normalise: fill in missing keys with empty strings
            for e in valid:
                for k in EVENT_KEYS:
                    e.setdefault(k, "")
            all_events.extend(valid)
            print(f"✓  {len(valid)} events")
        except Exception:
            failures.append(name)
            print(f"✗  FAILED")
            traceback.print_exc()

    # Sort chronologically (events with no date fall to the end)
    all_events.sort(key=lambda e: e.get("date") or "9999-99-99")

    output = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "failures": failures,
        "count": len(all_events),
        "events": all_events,
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "events.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone. {len(all_events)} events written to data/events.json")
    if failures:
        print(f"WARNING: {len(failures)} scraper(s) failed: {', '.join(failures)}")
        raise SystemExit(1)   # Causes GitHub Actions to mark the run as failed → triggers alert email


if __name__ == "__main__":
    run()

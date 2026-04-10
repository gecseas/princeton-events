"""
scrapers/citp.py  —  Center for Information Technology Policy
Uses: WordPress + Tribe Events REST API
API: https://citp.princeton.edu/wp-json/tribe/events/v1/events
"""

from .wp_tribe import scrape_tribe

BASE = "https://citp.princeton.edu"
DEPARTMENT = "Center for Information Technology Policy (CITP)"
TAGS = ["Tech Policy", "AI / ML", "Privacy", "Internet", "Computer Science"]


def scrape() -> list[dict]:
    return scrape_tribe(BASE, DEPARTMENT, TAGS)

"""
scrapers/odbi.py  —  Omenn-Darling Bioengineering Institute
Uses: WordPress + Tribe Events REST API
API: https://bioengineering.princeton.edu/wp-json/tribe/events/v1/events
"""

from .wp_tribe import scrape_tribe

BASE = "https://bioengineering.princeton.edu"
DEPARTMENT = "Omenn-Darling Bioengineering Institute"
TAGS = ["Bioengineering", "Biology", "Engineering", "AI / ML"]


def scrape() -> list[dict]:
    return scrape_tribe(BASE, DEPARTMENT, TAGS)

"""
scrapers/acee.py  —  Andlinger Center for Energy and the Environment
Uses: WordPress + Tribe Events REST API
API: https://acee.princeton.edu/wp-json/tribe/events/v1/events
"""

from .wp_tribe import scrape_tribe

BASE = "https://acee.princeton.edu"
DEPARTMENT = "Andlinger Center for Energy and the Environment"
TAGS = ["Energy", "Environment", "Climate", "Engineering"]


def scrape() -> list[dict]:
    return scrape_tribe(BASE, DEPARTMENT, TAGS)
